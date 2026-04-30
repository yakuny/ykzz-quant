from pydantic import BaseModel, Field


class StrategyParams(BaseModel):
    """Base strategy parameters."""

    top_n: int = Field(default=10, ge=1, le=100, description="持仓数量")
    min_remain_scale: float = Field(default=1.0, ge=0, description="最小剩余规模(亿元)")
    min_amount: float = Field(default=500.0, ge=0, description="最小日均成交额(万元)")
    min_remain_years: float = Field(default=0.5, ge=0, description="最小剩余年限(年)")
    exclude_st: bool = Field(default=True, description="排除ST正股")
    exclude_forced_redeem: bool = Field(default=True, description="排除强赎标的")


class DoubleLowParams(StrategyParams):
    """Double-low strategy parameters."""

    strategy_type: str = Field(default="double_low", description="策略类型")


class LowPremiumParams(StrategyParams):
    """Low premium strategy parameters."""

    strategy_type: str = Field(default="low_premium", description="策略类型")
