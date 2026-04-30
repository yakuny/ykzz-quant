import logging
from datetime import date

from sqlalchemy.orm import Session

from app.data.models import BondSnapshot, BondBasic

logger = logging.getLogger(__name__)


def calculate_remain_years(db: Session) -> int:
    """Calculate remaining years for all bonds.
    
    剩余年限 = (到期日期 - 当前日期) / 365
    """
    snapshots = db.query(BondSnapshot).all()
    if not snapshots:
        logger.warning("No bond snapshots found")
        return 0

    today = date.today()
    count = 0

    for snap in snapshots:
        basic = db.query(BondBasic).filter(BondBasic.ts_code == snap.ts_code).first()
        if basic and basic.maturity_date:
            delta = (basic.maturity_date - today).days
            snap.remain_years = round(delta / 365.0, 2)
            count += 1

    db.commit()
    logger.info("Calculated remain years for %d bonds", count)
    return count
