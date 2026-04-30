import logging
import sys

from app.database import SessionLocal, init_db
from app.factor.convert_value import calculate_convert_value
from app.factor.premium_rate import calculate_premium_rate
from app.factor.double_low import calculate_double_low
from app.factor.remain_years import calculate_remain_years
from app.factor.ytm import calculate_ytm
from app.logging import setup_logging

logger = logging.getLogger(__name__)


def run_factor_calculation():
    """Run all factor calculations in sequence."""
    setup_logging()
    init_db()
    db = SessionLocal()

    try:
        logger.info("Starting factor calculation...")

        # 1. Calculate remain years (needed for YTM)
        count = calculate_remain_years(db)
        logger.info("Remain years: %d updated", count)

        # 2. Calculate convert value
        count = calculate_convert_value(db)
        logger.info("Convert value: %d updated", count)

        # 3. Calculate premium rate (needs convert value)
        count = calculate_premium_rate(db)
        logger.info("Premium rate: %d updated", count)

        # 4. Calculate double low (needs premium rate)
        count = calculate_double_low(db)
        logger.info("Double low: %d updated", count)

        # 5. Calculate YTM
        count = calculate_ytm(db)
        logger.info("YTM: %d updated", count)

        logger.info("Factor calculation complete!")

    except Exception as e:
        logger.error("Factor calculation failed: %s", e)
        sys.exit(1)
    finally:
        db.close()


if __name__ == "__main__":
    run_factor_calculation()
