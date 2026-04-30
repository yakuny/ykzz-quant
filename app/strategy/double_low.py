import logging

import pandas as pd
from sqlalchemy.orm import Session

from app.strategy.filters import apply_risk_filters
from app.strategy.params import DoubleLowParams

logger = logging.getLogger(__name__)


def run_double_low_strategy(db: Session, params: DoubleLowParams | None = None) -> pd.DataFrame:
    """Run double-low strategy and return top candidates.
    
    双低值 = 转债价格 + 100 × 转股溢价率(%)
    Strategy: Sort by double_low ascending, take top N.
    """
    if params is None:
        params = DoubleLowParams()

    df = apply_risk_filters(db, params)
    if df.empty:
        logger.warning("No bonds after risk filtering")
        return df

    # Sort by double_low ascending (lower is better)
    df = df.sort_values("double_low", ascending=True)

    # Take top N
    df = df.head(params.top_n)

    logger.info("Double-low strategy: selected %d bonds", len(df))
    return df
