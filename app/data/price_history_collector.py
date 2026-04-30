import logging
from datetime import datetime

import akshare as ak
import pandas as pd
from sqlalchemy.orm import Session

from app.config import settings
from app.data.models import ConvertPriceHistory

logger = logging.getLogger(__name__)


def fetch_convert_price_history(db: Session) -> int:
    """Fetch convertible price adjustment history from JSL."""
    try:
        df = ak.bond_cb_adj_logs_jsl(cookie=settings.JSL_COOKIE)
        if df is None or df.empty:
            logger.warning("JSL convert price logs returned empty data")
            return 0

        count = 0
        for _, row in df.iterrows():
            ts_code = str(row.get("转债代码", ""))
            if not ts_code:
                continue

            adjust_date = _parse_date(row.get("调整日期"))
            if adjust_date is None:
                continue

            convert_price = _safe_float(row.get("转股价"))
            if convert_price is None:
                continue

            record = ConvertPriceHistory(
                ts_code=ts_code,
                adjust_date=adjust_date,
                convert_price=convert_price,
                reason=str(row.get("调整原因", "")),
            )
            db.merge(record)
            count += 1

        db.commit()
        logger.info("Saved %d convert price history records", count)
        return count
    except Exception as e:
        logger.error("Failed to fetch convert price history: %s", e)
        db.rollback()
        return 0


def _parse_date(val) -> datetime.date | None:
    """Parse date value to date object."""
    if val is None or pd.isna(val):
        return None
    try:
        if isinstance(val, str):
            return datetime.strptime(val, "%Y-%m-%d").date()
        if isinstance(val, datetime):
            return val.date()
        return val
    except (ValueError, TypeError):
        return None


def _safe_float(val) -> float | None:
    """Safely convert value to float."""
    if val is None or pd.isna(val):
        return None
    try:
        return float(val)
    except (ValueError, TypeError):
        return None
