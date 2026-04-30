import logging
from datetime import date

from sqlalchemy.orm import Session

from app.data.models import BondSnapshot, BondBasic

logger = logging.getLogger(__name__)


def calculate_ytm(db: Session) -> int:
    """Calculate yield to maturity for all bonds.
    
    Simplified YTM calculation:
    YTM ≈ (票面利率 + (面值 - 转债价格) / 剩余年限) / 转债价格 × 100
    """
    snapshots = db.query(BondSnapshot).filter(
        BondSnapshot.bond_price.isnot(None),
        BondSnapshot.remain_years.isnot(None),
    ).all()
    if not snapshots:
        logger.warning("No bond snapshots with price and remain years found")
        return 0

    today = date.today()
    count = 0

    for snap in snapshots:
        basic = db.query(BondBasic).filter(BondBasic.ts_code == snap.ts_code).first()
        if basic and basic.maturity_rate and basic.coupon_rate and snap.remain_years:
            if snap.remain_years > 0 and snap.bond_price > 0:
                # Simplified YTM calculation
                annual_coupon = basic.par * basic.coupon_rate / 100
                capital_gain = (basic.maturity_rate - snap.bond_price) / snap.remain_years
                snap.ytm = round((annual_coupon + capital_gain) / snap.bond_price * 100, 2)
                count += 1

    db.commit()
    logger.info("Calculated YTM for %d bonds", count)
    return count
