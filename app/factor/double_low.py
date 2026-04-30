import logging

from sqlalchemy.orm import Session

from app.data.models import BondSnapshot

logger = logging.getLogger(__name__)


def calculate_double_low(db: Session) -> int:
    """Calculate double-low value for all bonds.
    
    双低值 = 转债价格 + 100 × 转股溢价率(%)
    """
    snapshots = db.query(BondSnapshot).filter(
        BondSnapshot.bond_price.isnot(None),
        BondSnapshot.premium_rate.isnot(None),
    ).all()
    if not snapshots:
        logger.warning("No bond snapshots with price and premium rate found")
        return 0

    count = 0
    for snap in snapshots:
        if snap.bond_price is not None and snap.premium_rate is not None:
            snap.double_low = round(snap.bond_price + 100 * snap.premium_rate, 2)
            count += 1

    db.commit()
    logger.info("Calculated double low for %d bonds", count)
    return count
