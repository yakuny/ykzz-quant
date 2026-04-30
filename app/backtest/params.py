from datetime import date
from enum import Enum

from pydantic import BaseModel, Field


class StrategyType(str, Enum):
    DOUBLE_LOW = "double_low"
    LOW_PREMIUM = "low_premium"


class RebalanceFreq(str, Enum):
    WEEKLY = "weekly"
    BIWEEKLY = "biweekly"
    MONTHLY = "monthly"


class BacktestParams(BaseModel):
    """Backtest parameters."""

    start_date: date = Field(description="回测开始日期")
    end_date: date = Field(description="回测结束日期")
    strategy_type: StrategyType = Field(default=StrategyType.DOUBLE_LOW, description="策略类型")
    rebalance_freq: RebalanceFreq = Field(default=RebalanceFreq.WEEKLY, description="调仓频率")
    top_n: int = Field(default=10, ge=1, le=100, description="持仓数量")
    commission_rate: float = Field(default=0.0003, ge=0, description="手续费率")
    slippage_rate: float = Field(default=0.001, ge=0, description="滑点率")
    initial_capital: float = Field(default=1000000.0, gt=0, description="初始资金")
