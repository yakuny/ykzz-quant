## ADDED Requirements

### Requirement: 双低策略筛选
系统 SHALL 实现双低策略，按双低值升序排列并筛选候选标的。

#### Scenario: 执行双低策略
- **WHEN** 用户运行双低策略
- **THEN** 系统按双低值升序排列，返回前 N 只可转债作为候选

#### Scenario: 参数配置
- **WHEN** 用户配置策略参数（如持仓数量、过滤条件）
- **THEN** 系统使用 Pydantic BaseModel 校验并应用参数

### Requirement: 低溢价策略筛选
系统 SHALL 实现低溢价策略，按转股溢价率升序排列并筛选候选标的。

#### Scenario: 执行低溢价策略
- **WHEN** 用户运行低溢价策略
- **THEN** 系统按转股溢价率升序排列，返回前 N 只可转债作为候选

### Requirement: 风险过滤模块
系统 SHALL 提供多维度风险过滤功能，自动排除高风险标的。

#### Scenario: 过滤剩余规模过小
- **WHEN** 可转债剩余规模低于阈值（如 1 亿元）
- **THEN** 系统将其从候选列表中排除

#### Scenario: 过滤成交额过低
- **WHEN** 可转债日均成交额低于阈值（如 500 万元）
- **THEN** 系统将其从候选列表中排除

#### Scenario: 过滤强赎高风险
- **WHEN** 可转债触发强赎条件或临近强赎触发价
- **THEN** 系统将其标记为高风险并可选择性排除

#### Scenario: 过滤正股 ST
- **WHEN** 可转债对应的正股被标记为 ST
- **THEN** 系统将其从候选列表中排除

#### Scenario: 过滤临近到期
- **WHEN** 可转债剩余期限低于阈值（如 0.5 年）
- **THEN** 系统将其从候选列表中排除

### Requirement: 策略参数化配置
系统 SHALL 使用 Pydantic BaseModel 定义策略参数，支持 JSON/YAML 配置文件加载。

#### Scenario: 加载配置文件
- **WHEN** 用户提供 JSON 或 YAML 配置文件
- **THEN** 系统解析并校验参数，应用到策略执行

#### Scenario: 默认参数
- **WHEN** 用户未提供配置文件
- **THEN** 系统使用预设的默认参数执行策略
