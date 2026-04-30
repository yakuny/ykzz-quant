import logging

from sqlalchemy.orm import Session

from app.data.models import BondSnapshot

logger = logging.getLogger(__name__)


def calculate_premium_rate(db: Session) -> int:
    """Calculate premium rate for all bonds.
    
    转股溢价率(%) = (转债价格 - 转股价值) / 转股价值 × 100
    """
    snapshots = db.query(BondSnapshot).filter(BondSnapshot.convert_value.isnot(None)).all()
    if not snapshots:
        logger.warning("No bond snapshots with convert value found")
        return 0

    count = 0
    for snap in snapshots:
        if snap.bond_price and snap.convert_value and snap.convert_value > 0:
            snap.premium_rate = round(
                (snap.bond_price - snap.convert_value) / snap.convert_value * 100, 2
            )
            count += 1

    db.commit()
    logger.info("Calculated premium rate for %d bonds", count)
    return count
