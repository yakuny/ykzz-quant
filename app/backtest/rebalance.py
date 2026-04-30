import logging
from datetime import date, timedelta

import pandas as pd

from app.backtest.params import BacktestParams, RebalanceFreq

logger = logging.getLogger(__name__)


def get_rebalance_dates(start_date: date, end_date: date, freq: RebalanceFreq) -> list[date]:
    """Generate list of rebalance dates based on frequency."""
    dates = []
    current = start_date

    if freq == RebalanceFreq.WEEKLY:
        # Rebalance every Monday
        while current <= end_date:
            if current.weekday() == 0:  # Monday
                dates.append(current)
            current += timedelta(days=1)
    elif freq == RebalanceFreq.BIWEEKLY:
        # Rebalance every other Monday
        while current <= end_date:
            if current.weekday() == 0:
                dates.append(current)
            current += timedelta(days=1)
        dates = dates[::2]  # Take every other Monday
    elif freq == RebalanceFreq.MONTHLY:
        # Rebalance first trading day of month
        seen_months = set()
        while current <= end_date:
            month_key = (current.year, current.month)
            if month_key not in seen_months and current.weekday() < 5:
                dates.append(current)
                seen_months.add(month_key)
            current += timedelta(days=1)

    return dates


def select_portfolio(df: pd.DataFrame, params: BacktestParams) -> pd.DataFrame:
    """Select portfolio based on strategy type."""
    if df.empty:
        return df

    if params.strategy_type.value == "double_low":
        df = df.sort_values("double_low", ascending=True)
    elif params.strategy_type.value == "low_premium":
        df = df.sort_values("premium_rate", ascending=True)

    return df.head(params.top_n)
