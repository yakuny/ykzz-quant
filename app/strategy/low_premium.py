import logging

import pandas as pd
from sqlalchemy.orm import Session

from app.strategy.filters import apply_risk_filters
from app.strategy.params import LowPremiumParams

logger = logging.getLogger(__name__)


def run_low_premium_strategy(db: Session, params: LowPremiumParams | None = None) -> pd.DataFrame:
    """Run low-premium strategy and return top candidates.
    
    Strategy: Sort by premium_rate ascending, take top N.
    """
    if params is None:
        params = LowPremiumParams()

    df = apply_risk_filters(db, params)
    if df.empty:
        logger.warning("No bonds after risk filtering")
        return df

    # Sort by premium_rate ascending (lower is better)
    df = df.sort_values("premium_rate", ascending=True)

    # Take top N
    df = df.head(params.top_n)

    logger.info("Low-premium strategy: selected %d bonds", len(df))
    return df
