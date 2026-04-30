import logging
from typing import List

import pandas as pd
from sqlalchemy.orm import Session

from app.data.models import BondSnapshot
from app.strategy.params import StrategyParams

logger = logging.getLogger(__name__)


def apply_risk_filters(db: Session, params: StrategyParams) -> pd.DataFrame:
    """Apply risk filters to bond snapshots and return filtered DataFrame."""
    snapshots = db.query(BondSnapshot).all()
    if not snapshots:
        return pd.DataFrame()

    df = pd.DataFrame([{
        "ts_code": s.ts_code,
        "name": s.name,
        "bond_price": s.bond_price,
        "convert_value": s.convert_value,
        "premium_rate": s.premium_rate,
        "double_low": s.double_low,
        "ytm": s.ytm,
        "remain_years": s.remain_years,
        "remain_scale": s.remain_scale,
        "stock_code": s.stock_code,
        "stock_name": s.stock_name,
    } for s in snapshots])

    initial_count = len(df)

    # Filter by minimum remain scale
    if params.min_remain_scale > 0:
        df = df[df["remain_scale"].fillna(0) >= params.min_remain_scale]

    # Filter by minimum remain years
    if params.min_remain_years > 0:
        df = df[df["remain_years"].fillna(0) >= params.min_remain_years]

    # Filter ST stocks (simplified - check if stock name contains ST)
    if params.exclude_st:
        df = df[~df["stock_name"].fillna("").str.contains("ST", case=False)]

    # Filter out bonds with missing key data
    df = df.dropna(subset=["bond_price", "double_low"])

    final_count = len(df)
    logger.info("Risk filters: %d -> %d bonds", initial_count, final_count)

    return df
