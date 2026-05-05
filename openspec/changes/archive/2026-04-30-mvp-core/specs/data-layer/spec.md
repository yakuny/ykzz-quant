## ADDED Requirements

### Requirement: 集思录实时数据采集
系统 SHALL 通过 AkShare 的 `bond_cb_jsl` 接口采集全市场可转债实时快照数据，并落库到 SQLite。

#### Scenario: 成功采集全量数据
- **WHEN** 系统调用 `bond_cb_jsl` 且集思录 cookie 有效
- **THEN** 系统获取全部约 560 条可转债数据并写入 `bond_snapshot` 表

#### Scenario: Cookie 失效处理
- **WHEN** 系统调用 `bond_cb_jsl` 且 cookie 无效或过期
- **THEN** 系统返回前 30 条数据并记录警告日志，提示用户更新 cookie

### Requirement: Tushare 历史行情采集
系统 SHALL 通过 Tushare `cb_daily` 接口补齐可转债历史行情数据，用于回测。

#### Scenario: 增量更新历史行情
- **WHEN** 系统执行日更任务
- **THEN** 系统仅采集缺失日期的行情数据，避免重复调用

#### Scenario: 频率限制控制
- **WHEN** Tushare API 调用频率接近限制（200次/分钟）
- **THEN** 系统自动 sleep 等待，不触发限流错误

### Requirement: 正股信息采集
系统 SHALL 采集可转债对应的正股代码、名称、行业等基本信息。

#### Scenario: 关联正股数据
- **WHEN** 系统采集可转债数据
- **THEN** 系统自动关联并存储对应的正股代码和名称

### Requirement: 转股价历史记录
系统 SHALL 维护每只可转债的转股价调整历史表 `convert_price_history`。

#### Scenario: 记录转股价变更
- **WHEN** 检测到转股价下修或调整事件
- **THEN** 系统在 `convert_price_history` 表中插入新记录，包含调整日期和新转股价

### Requirement: 数据存储规范
系统 SHALL 使用 SQLAlchemy ORM 定义数据模型，支持 SQLite（MVP）并可无成本迁移到 PostgreSQL。

#### Schema: bond_snapshot
- ts_code: 转债代码（主键）
- name: 转债名称
- bond_price: 转债价格
- convert_value: 转股价值
- premium_rate: 转股溢价率
- double_low: 双低值
- ytm: 到期收益率
- remain_years: 剩余年限
- remain_scale: 剩余规模（亿元）
- stock_code: 正股代码
- stock_name: 正股名称
- update_time: 更新时间

#### Scenario: ORM 模型定义
- **WHEN** 系统启动
- **THEN** SQLAlchemy 自动创建所有数据表（如不存在）
