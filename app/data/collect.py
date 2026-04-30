import logging
import sys

from app.config import settings
from app.database import SessionLocal, init_db
from app.data.jsl_collector import fetch_jsl_snapshot, save_snapshot
from app.data.tushare_collector import fetch_bond_basic
from app.data.price_history_collector import fetch_convert_price_history
from app.logging import setup_logging

logger = logging.getLogger(__name__)


def run_collection():
    """Run all data collectors."""
    setup_logging()
    init_db()
    db = SessionLocal()

    try:
        logger.info("Starting data collection...")

        # 1. Fetch JSL snapshot
        logger.info("Fetching JSL snapshot...")
        df = fetch_jsl_snapshot(db)
        if not df.empty:
            save_snapshot(db, df)
            logger.info("JSL snapshot saved: %d records", len(df))

        # 2. Fetch bond basic info from Tushare
        if settings.TUSHARE_TOKEN:
            logger.info("Fetching bond basic info...")
            count = fetch_bond_basic(db)
            logger.info("Bond basic saved: %d records", count)

            # 3. Fetch convert price history
            logger.info("Fetching convert price history...")
            count = fetch_convert_price_history(db)
            logger.info("Convert price history saved: %d records", count)
        else:
            logger.warning("TUSHARE_TOKEN not set, skipping Tushare collectors")

        logger.info("Data collection complete!")

    except Exception as e:
        logger.error("Data collection failed: %s", e)
        sys.exit(1)
    finally:
        db.close()


if __name__ == "__main__":
    run_collection()
