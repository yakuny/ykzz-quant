from datetime import date

from fastapi import APIRouter, Depends, Query, HTTPException
from sqlalchemy.orm import Session
import pandas as pd

from app.database import get_db
from app.data.models import BondSnapshot, BondBasic
from app.strategy.double_low import run_double_low_strategy
from app.strategy.low_premium import run_low_premium_strategy
from app.strategy.params import DoubleLowParams, LowPremiumParams
from app.backtest.params import BacktestParams, StrategyType, RebalanceFreq
from app.backtest.run import run_backtest

router = APIRouter()


@router.get("/strategy/recommend")
async def get_strategy_recommend(
    strategy_type: str = Query("double_low", description="策略类型: double_low 或 low_premium"),
    top_n: int = Query(10, ge=1, le=100, description="返回数量"),
    db: Session = Depends(get_db),
):
    """获取策略推荐的可转债列表."""
    if strategy_type == "double_low":
        params = DoubleLowParams(top_n=top_n)
        df = run_double_low_strategy(db, params)
    elif strategy_type == "low_premium":
        params = LowPremiumParams(top_n=top_n)
        df = run_low_premium_strategy(db, params)
    else:
        return {"error": f"Unknown strategy type: {strategy_type}"}

    if df.empty:
        return {"data": [], "message": "No bonds selected"}

    result = df.to_dict(orient="records")
    return {"data": result, "count": len(result)}


@router.get("/bond/{ts_code}")
async def get_bond_detail(ts_code: str, db: Session = Depends(get_db)):
    """获取单只可转债详情."""
    snapshot = db.query(BondSnapshot).filter(BondSnapshot.ts_code == ts_code).first()
    if not snapshot:
        raise HTTPException(status_code=404, detail=f"Bond {ts_code} not found")

    basic = db.query(BondBasic).filter(BondBasic.ts_code == ts_code).first()

    result = {
        "ts_code": snapshot.ts_code,
        "name": snapshot.name,
        "bond_price": snapshot.bond_price,
        "convert_value": snapshot.convert_value,
        "premium_rate": snapshot.premium_rate,
        "double_low": snapshot.double_low,
        "ytm": snapshot.ytm,
        "remain_years": snapshot.remain_years,
        "remain_scale": snapshot.remain_scale,
        "stock_code": snapshot.stock_code,
        "stock_name": snapshot.stock_name,
    }

    if basic:
        result.update({
            "list_date": basic.list_date.isoformat() if basic.list_date else None,
            "maturity_date": basic.maturity_date.isoformat() if basic.maturity_date else None,
            "convert_price": basic.convert_price,
            "coupon_rate": basic.coupon_rate,
            "maturity_rate": basic.maturity_rate,
        })

    return result


@router.get("/backtest/result")
async def get_backtest_result(
    strategy_type: str = Query("double_low", description="策略类型"),
    start_date: str = Query(..., description="开始日期 (YYYY-MM-DD)"),
    end_date: str = Query(..., description="结束日期 (YYYY-MM-DD)"),
    top_n: int = Query(10, ge=1, le=100, description="持仓数量"),
    freq: str = Query("weekly", description="调仓频率"),
    db: Session = Depends(get_db),
):
    """获取回测结果."""
    try:
        params = BacktestParams(
            start_date=date.fromisoformat(start_date),
            end_date=date.fromisoformat(end_date),
            strategy_type=StrategyType(strategy_type),
            rebalance_freq=RebalanceFreq(freq),
            top_n=top_n,
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    # Run backtest and return results
    from app.backtest.data_loader import load_historical_data
    from app.backtest.rebalance import get_rebalance_dates, select_portfolio
    from app.backtest.costs import calculate_transaction_cost
    from app.backtest.metrics import calculate_performance

    df = load_historical_data(db, params.start_date, params.end_date)
    if df.empty:
        return {"error": "No data available for backtesting"}

    rebalance_dates = get_rebalance_dates(params.start_date, params.end_date, params.rebalance_freq)
    capital = params.initial_capital
    portfolio = {}
    equity_values = []
    equity_dates = []

    for reb_date in rebalance_dates:
        new_portfolio_df = select_portfolio(df, params)
        new_codes = set(new_portfolio_df["ts_code"].tolist())
        old_codes = set(portfolio.keys())
        trades_in = new_codes - old_codes
        trades_out = old_codes - new_codes
        turnover = len(trades_in) + len(trades_out)

        if turnover > 0:
            avg_position = capital / params.top_n
            trade_amount = turnover * avg_position / 2
            cost = calculate_transaction_cost(trade_amount, params)
            capital -= cost

        portfolio = {code: capital / params.top_n for code in new_codes}
        equity_values.append(capital)
        equity_dates.append(reb_date)

    equity_curve = pd.Series(equity_values, index=pd.DatetimeIndex(equity_dates))
    metrics = calculate_performance(equity_curve)

    return {
        "params": {
            "strategy_type": strategy_type,
            "start_date": start_date,
            "end_date": end_date,
            "top_n": top_n,
            "freq": freq,
        },
        "metrics": {
            "total_return": metrics.total_return,
            "annual_return": metrics.annual_return,
            "max_drawdown": metrics.max_drawdown,
            "sharpe_ratio": metrics.sharpe_ratio,
            "win_rate": metrics.win_rate,
            "turnover_rate": metrics.turnover_rate,
        },
        "equity_curve": {
            "dates": [d.isoformat() for d in equity_dates],
            "values": equity_values,
        },
    }
