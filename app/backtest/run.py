import logging
import sys
from datetime import date

import pandas as pd

from app.database import SessionLocal, init_db
from app.backtest.params import BacktestParams, StrategyType, RebalanceFreq
from app.backtest.data_loader import load_historical_data
from app.backtest.rebalance import get_rebalance_dates, select_portfolio
from app.backtest.costs import calculate_transaction_cost
from app.backtest.metrics import calculate_performance
from app.backtest.visualization import plot_equity_curve
from app.logging import setup_logging

logger = logging.getLogger(__name__)


def run_backtest(params: BacktestParams):
    """Run backtest with given parameters."""
    setup_logging()
    init_db()
    db = SessionLocal()

    try:
        logger.info("Starting backtest: %s to %s", params.start_date, params.end_date)
        logger.info("Strategy: %s, Top N: %d", params.strategy_type.value, params.top_n)

        # Load historical data
        df = load_historical_data(db, params.start_date, params.end_date)
        if df.empty:
            logger.error("No data available for backtesting")
            sys.exit(1)

        # Get rebalance dates
        rebalance_dates = get_rebalance_dates(params.start_date, params.end_date, params.rebalance_freq)
        logger.info("Rebalance dates: %d", len(rebalance_dates))

        # Initialize backtest
        capital = params.initial_capital
        portfolio = {}
        equity_values = []
        equity_dates = []
        total_trades = 0
        total_turnover = 0.0

        # Run backtest
        for i, reb_date in enumerate(rebalance_dates):
            # Select new portfolio
            new_portfolio_df = select_portfolio(df, params)
            new_codes = set(new_portfolio_df["ts_code"].tolist())

            # Calculate turnover
            old_codes = set(portfolio.keys())
            trades_in = new_codes - old_codes
            trades_out = old_codes - new_codes
            turnover = len(trades_in) + len(trades_out)
            total_trades += turnover

            # Apply transaction costs
            if turnover > 0:
                avg_position = capital / params.top_n
                trade_amount = turnover * avg_position / 2
                cost = calculate_transaction_cost(trade_amount, params)
                capital -= cost
                total_turnover += trade_amount

            # Update portfolio
            portfolio = {code: capital / params.top_n for code in new_codes}

            # Record equity
            equity_values.append(capital)
            equity_dates.append(reb_date)

            logger.debug(
                "Rebalance %d/%d: %d trades, capital=%.2f",
                i + 1, len(rebalance_dates), turnover, capital,
            )

        # Create equity curve
        equity_curve = pd.Series(equity_values, index=pd.DatetimeIndex(equity_dates))

        # Calculate performance
        metrics = calculate_performance(equity_curve)

        # Print results
        print("\n" + "=" * 50)
        print("BACKTEST RESULTS")
        print("=" * 50)
        print(f"Period: {params.start_date} to {params.end_date}")
        print(f"Strategy: {params.strategy_type.value}")
        print(f"Rebalance: {params.rebalance_freq.value}")
        print("-" * 50)
        print(f"Total Return: {metrics.total_return:.2f}%")
        print(f"Annual Return: {metrics.annual_return:.2f}%")
        print(f"Max Drawdown: {metrics.max_drawdown:.2f}%")
        print(f"Sharpe Ratio: {metrics.sharpe_ratio:.2f}")
        print(f"Win Rate: {metrics.win_rate:.2f}%")
        print(f"Turnover Rate: {metrics.turnover_rate:.2f}%")
        print(f"Total Trades: {total_trades}")
        print("=" * 50)

        # Plot equity curve
        plot_equity_curve(equity_curve, output_path="backtest_result.png")

        logger.info("Backtest complete!")

    except Exception as e:
        logger.error("Backtest failed: %s", e)
        sys.exit(1)
    finally:
        db.close()


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Run backtest")
    parser.add_argument("--start", required=True, help="Start date (YYYY-MM-DD)")
    parser.add_argument("--end", required=True, help="End date (YYYY-MM-DD)")
    parser.add_argument("--strategy", choices=["double_low", "low_premium"], default="double_low")
    parser.add_argument("--top-n", type=int, default=10)
    parser.add_argument("--freq", choices=["weekly", "biweekly", "monthly"], default="weekly")
    args = parser.parse_args()

    params = BacktestParams(
        start_date=date.fromisoformat(args.start),
        end_date=date.fromisoformat(args.end),
        strategy_type=StrategyType(args.strategy),
        rebalance_freq=RebalanceFreq(args.freq),
        top_n=args.top_n,
    )
    run_backtest(params)
