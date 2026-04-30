import logging
from datetime import date

import pandas as pd
from sqlalchemy.orm import Session

from app.data.models import BondSnapshot, BondBasic

logger = logging.getLogger(__name__)


def load_historical_data(db: Session, start_date: date, end_date: date) -> pd.DataFrame:
    """Load historical bond data for backtesting.
    
    Returns DataFrame with columns:
    - ts_code, trade_date, bond_price, convert_value, premium_rate, double_low, 
      ytm, remain_years, remain_scale, stock_code
    """
    # For MVP, we use current snapshot as proxy
    # In production, this would query historical snapshot table
    snapshots = db.query(BondSnapshot).all()
    if not snapshots:
        logger.warning("No bond snapshots found")
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

    # Filter out rows with missing key data
    df = df.dropna(subset=["bond_price", "double_low"])

    logger.info("Loaded %d bond records for backtesting", len(df))
    return df
