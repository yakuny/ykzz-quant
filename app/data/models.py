from datetime import datetime, date

from sqlalchemy import Column, String, Float, DateTime, Date, Integer

from app.database import Base


class BondSnapshot(Base):
    __tablename__ = "bond_snapshot"

    ts_code = Column(String(20), primary_key=True, comment="转债代码")
    name = Column(String(50), comment="转债名称")
    bond_price = Column(Float, comment="转债价格")
    convert_value = Column(Float, comment="转股价值")
    premium_rate = Column(Float, comment="转股溢价率(%)")
    double_low = Column(Float, comment="双低值")
    ytm = Column(Float, comment="到期收益率(%)")
    remain_years = Column(Float, comment="剩余年限")
    remain_scale = Column(Float, comment="剩余规模(亿元)")
    stock_code = Column(String(20), comment="正股代码")
    stock_name = Column(String(50), comment="正股名称")
    update_time = Column(DateTime, default=datetime.utcnow, comment="更新时间")


class ConvertPriceHistory(Base):
    __tablename__ = "convert_price_history"

    id = Column(Integer, primary_key=True, autoincrement=True)
    ts_code = Column(String(20), nullable=False, comment="转债代码")
    adjust_date = Column(Date, nullable=False, comment="调整日期")
    convert_price = Column(Float, nullable=False, comment="转股价")
    reason = Column(String(100), comment="调整原因")
    create_time = Column(DateTime, default=datetime.utcnow, comment="创建时间")


class BondBasic(Base):
    __tablename__ = "bond_basic"

    ts_code = Column(String(20), primary_key=True, comment="转债代码")
    name = Column(String(50), comment="转债名称")
    stock_code = Column(String(20), comment="正股代码")
    stock_name = Column(String(50), comment="正股名称")
    list_date = Column(Date, comment="上市日期")
    delist_date = Column(Date, comment="退市日期")
    maturity_date = Column(Date, comment="到期日期")
    par = Column(Float, default=100.0, comment="面值")
    issue_price = Column(Float, comment="发行价格")
    convert_price = Column(Float, comment="最新转股价")
    coupon_rate = Column(Float, comment="票面利率(%)")
    maturity_rate = Column(Float, comment="到期赎回价")
    create_time = Column(DateTime, default=datetime.utcnow, comment="创建时间")
    update_time = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, comment="更新时间")


class StockDaily(Base):
    __tablename__ = "stock_daily"

    id = Column(Integer, primary_key=True, autoincrement=True)
    stock_code = Column(String(20), nullable=False, comment="股票代码")
    trade_date = Column(Date, nullable=False, comment="交易日期")
    open = Column(Float, comment="开盘价")
    high = Column(Float, comment="最高价")
    low = Column(Float, comment="最低价")
    close = Column(Float, comment="收盘价")
    volume = Column(Float, comment="成交量")
    amount = Column(Float, comment="成交额")
    create_time = Column(DateTime, default=datetime.utcnow, comment="创建时间")
