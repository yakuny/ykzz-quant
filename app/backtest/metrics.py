import logging
from dataclasses import dataclass

import numpy as np
import pandas as pd

logger = logging.getLogger(__name__)


@dataclass
class PerformanceMetrics:
    """Backtest performance metrics."""

    total_return: float = 0.0
    annual_return: float = 0.0
    max_drawdown: float = 0.0
    sharpe_ratio: float = 0.0
    win_rate: float = 0.0
    turnover_rate: float = 0.0


def calculate_performance(
    equity_curve: pd.Series,
    trades: pd.DataFrame | None = None,
    risk_free_rate: float = 0.03,
) -> PerformanceMetrics:
    """Calculate performance metrics from equity curve.
    
    Args:
        equity_curve: Series of portfolio values indexed by date
        trades: DataFrame of trades (optional, for win rate and turnover)
        risk_free_rate: Annual risk-free rate for Sharpe calculation
    """
    if equity_curve.empty or len(equity_curve) < 2:
        return PerformanceMetrics()

    # Total return
    total_return = (equity_curve.iloc[-1] / equity_curve.iloc[0]) - 1

    # Annualized return
    days = (equity_curve.index[-1] - equity_curve.index[0]).days
    if days > 0:
        annual_return = (1 + total_return) ** (365 / days) - 1
    else:
        annual_return = 0.0

    # Maximum drawdown
    rolling_max = equity_curve.expanding().max()
    drawdown = (equity_curve - rolling_max) / rolling_max
    max_drawdown = drawdown.min()

    # Sharpe ratio (daily returns)
    daily_returns = equity_curve.pct_change().dropna()
    if len(daily_returns) > 0:
        excess_returns = daily_returns - risk_free_rate / 252
        if excess_returns.std() > 0:
            sharpe_ratio = np.sqrt(252) * excess_returns.mean() / excess_returns.std()
        else:
            sharpe_ratio = 0.0
    else:
        sharpe_ratio = 0.0

    # Win rate (from trades if available)
    win_rate = 0.0
    if trades is not None and not trades.empty:
        profitable_trades = len(trades[trades["pnl"] > 0])
        total_trades = len(trades)
        if total_trades > 0:
            win_rate = profitable_trades / total_trades

    # Turnover rate (simplified)
    turnover_rate = 0.0
    if trades is not None and not trades.empty:
        total_traded = trades["amount"].sum()
        avg_portfolio = equity_curve.mean()
        if avg_portfolio > 0 and days > 0:
            turnover_rate = (total_traded / avg_portfolio) * (365 / days)

    return PerformanceMetrics(
        total_return=round(total_return * 100, 2),
        annual_return=round(annual_return * 100, 2),
        max_drawdown=round(max_drawdown * 100, 2),
        sharpe_ratio=round(sharpe_ratio, 2),
        win_rate=round(win_rate * 100, 2),
        turnover_rate=round(turnover_rate * 100, 2),
    )
