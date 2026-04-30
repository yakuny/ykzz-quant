import logging

from app.backtest.params import BacktestParams

logger = logging.getLogger(__name__)


def calculate_transaction_cost(
    trade_amount: float,
    params: BacktestParams,
) -> float:
    """Calculate transaction cost including commission and slippage.
    
    Args:
        trade_amount: Absolute value of trade amount
        params: Backtest parameters with commission and slippage rates
    
    Returns:
        Total transaction cost
    """
    commission = trade_amount * params.commission_rate
    slippage = trade_amount * params.slippage_rate
    total_cost = commission + slippage

    logger.debug(
        "Transaction cost: amount=%.2f, commission=%.2f, slippage=%.2f, total=%.2f",
        trade_amount, commission, slippage, total_cost,
    )
    return total_cost
