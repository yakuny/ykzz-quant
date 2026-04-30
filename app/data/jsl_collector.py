import logging
from datetime import datetime

import akshare as ak
import pandas as pd
from sqlalchemy.orm import Session

from app.config import settings
from app.data.models import BondSnapshot

logger = logging.getLogger(__name__)


def fetch_jsl_snapshot(db: Session) -> pd.DataFrame:
    """Fetch convertible bond snapshot from JSL (集思录) via AkShare."""
    try:
        df = ak.bond_cb_jsl(cookie=settings.JSL_COOKIE)
        if df is None or df.empty:
            logger.warning("JSL returned empty data")
            return pd.DataFrame()

        if len(df) <= 30:
            logger.warning(
                "JSL returned only %d rows - cookie may be invalid. "
                "Please update JSL_COOKIE in .env",
                len(df),
            )

        return df
    except Exception as e:
        logger.error("Failed to fetch JSL data: %s", e)
        return pd.DataFrame()


def save_snapshot(db: Session, df: pd.DataFrame) -> int:
    """Save JSL snapshot data to database."""
    if df.empty:
        return 0

    now = datetime.utcnow()
    count = 0

    for _, row in df.iterrows():
        ts_code = str(row.get("转债代码", ""))
        if not ts_code:
            continue

        snapshot = db.merge(
            BondSnapshot(
                ts_code=ts_code,
                name=str(row.get("转债名称", "")),
                bond_price=_safe_float(row.get("转债价格")),
                convert_value=_safe_float(row.get("转股价值")),
                premium_rate=_safe_float(row.get("转股溢价率")),
                double_low=_safe_float(row.get("双低值")),
                ytm=_safe_float(row.get("到期收益率")),
                remain_years=_safe_float(row.get("剩余年限")),
                remain_scale=_safe_float(row.get("剩余规模")),
                stock_code=str(row.get("正股代码", "")),
                stock_name=str(row.get("正股名称", "")),
                update_time=now,
            )
        )
        count += 1

    db.commit()
    logger.info("Saved %d bond snapshots", count)
    return count


def _safe_float(val) -> float | None:
    """Safely convert value to float."""
    if val is None or pd.isna(val):
        return None
    try:
        return float(val)
    except (ValueError, TypeError):
        return None
