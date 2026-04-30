import logging
from typing import List

import pandas as pd

logger = logging.getLogger(__name__)


def handle_suspended_bonds(
    current_portfolio: List[str],
    available_bonds: pd.DataFrame,
) -> List[str]:
    """Handle suspended bonds during rebalancing.
    
    If a bond in the current portfolio is not available (suspended),
    keep it in the portfolio until it becomes available again.
    
    Args:
        current_portfolio: List of ts_codes in current portfolio
        available_bonds: DataFrame of bonds available for trading
    
    Returns:
        List of ts_codes that are still tradeable
    """
    if not current_portfolio:
        return []

    available_codes = set(available_bonds["ts_code"].tolist())
    tradeable = [code for code in current_portfolio if code in available_codes]
    suspended = [code for code in current_portfolio if code not in available_codes]

    if suspended:
        logger.info("Suspended bonds (keeping): %s", suspended)

    return tradeable
