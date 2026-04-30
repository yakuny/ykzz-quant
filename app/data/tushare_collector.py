import logging
import time
from datetime import date, datetime

import pandas as pd
import tushare as ts
from sqlalchemy.orm import Session

from app.config import settings
from app.data.models import BondBasic

logger = logging.getLogger(__name__)

_pro: ts.pro_api | None = None


def _get_pro() -> ts.pro_api:
    """Get Tushare pro API instance."""
    global _pro
    if _pro is None:
        ts.set_token(settings.TUSHARE_TOKEN)
        _pro = ts.pro_api()
    return _pro


def _rate_limit_sleep():
    """Sleep to respect Tushare rate limits."""
    sleep_time = 60.0 / settings.TUSHARE_RATE_LIMIT
    time.sleep(sleep_time)


def fetch_bond_basic(db: Session) -> int:
    """Fetch basic bond info from Tushare."""
    pro = _get_pro()
    try:
        df = pro.cb_basic(fields="ts_code,name,stock_code,stock_name,list_date,delist_date,maturity_date,par,issue_price,convert_price,coupon_rate,maturity_rate")
        if df is None or df.empty:
            logger.warning("Tushare cb_basic returned empty data")
            return 0

        count = 0
        for _, row in df.iterrows():
            ts_code = str(row.get("ts_code", ""))
            if not ts_code:
                continue

            basic = db.merge(
                BondBasic(
                    ts_code=ts_code,
                    name=str(row.get("name", "")),
                    stock_code=str(row.get("stock_code", "")),
                    stock_name=str(row.get("stock_name", "")),
                    list_date=_parse_date(row.get("list_date")),
                    delist_date=_parse_date(row.get("delist_date")),
                    maturity_date=_parse_date(row.get("maturity_date")),
                    par=_safe_float(row.get("par"), default=100.0),
                    issue_price=_safe_float(row.get("issue_price")),
                    convert_price=_safe_float(row.get("convert_price")),
                    coupon_rate=_safe_float(row.get("coupon_rate")),
                    maturity_rate=_safe_float(row.get("maturity_rate")),
                )
            )
            count += 1

        db.commit()
        logger.info("Saved %d bond basic records", count)
        return count
    except Exception as e:
        logger.error("Failed to fetch bond basic: %s", e)
        db.rollback()
        return 0


def fetch_cb_daily(db: Session, ts_code: str, start_date: date, end_date: date) -> pd.DataFrame:
    """Fetch daily convertible bond data from Tushare."""
    pro = _get_pro()
    try:
        _rate_limit_sleep()
        df = pro.cb_daily(
            ts_code=ts_code,
            start_date=start_date.strftime("%Y%m%d"),
            end_date=end_date.strftime("%Y%m%d"),
        )
        return df if df is not None else pd.DataFrame()
    except Exception as e:
        logger.error("Failed to fetch cb_daily for %s: %s", ts_code, e)
        return pd.DataFrame()


def _parse_date(val) -> date | None:
    """Parse date string to date object."""
    if val is None or pd.isna(val):
        return None
    try:
        if isinstance(val, str):
            return datetime.strptime(val, "%Y%m%d").date()
        return val
    except (ValueError, TypeError):
        return None


def _safe_float(val, default: float | None = None) -> float | None:
    """Safely convert value to float."""
    if val is None or pd.isna(val):
        return default
    try:
        return float(val)
    except (ValueError, TypeError):
        return default
