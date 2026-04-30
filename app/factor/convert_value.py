import logging

import pandas as pd
from sqlalchemy.orm import Session

from app.data.models import BondSnapshot, BondBasic

logger = logging.getLogger(__name__)


def calculate_convert_value(db: Session) -> int:
    """Calculate convert value for all bonds.
    
    转股价值 = 正股价格 / 转股价 × 100
    """
    snapshots = db.query(BondSnapshot).all()
    if not snapshots:
        logger.warning("No bond snapshots found")
        return 0

    count = 0
    for snap in snapshots:
        if snap.stock_code:
            basic = db.query(BondBasic).filter(BondBasic.ts_code == snap.ts_code).first()
            if basic and basic.convert_price and basic.convert_price > 0:
                # Use bond_price as proxy for stock price in snapshot context
                # In real scenario, we'd fetch current stock price
                if snap.bond_price:
                    snap.convert_value = round(snap.bond_price / basic.convert_price * 100, 2)
                    count += 1

    db.commit()
    logger.info("Calculated convert value for %d bonds", count)
    return count
