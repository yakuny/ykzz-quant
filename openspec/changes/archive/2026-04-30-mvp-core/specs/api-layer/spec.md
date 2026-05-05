## ADDED Requirements

### Requirement: 策略推荐接口
系统 SHALL 提供 FastAPI 接口，返回当前策略推荐的可转债列表。

#### Endpoint: GET /api/strategy/recommend
- **参数**: strategy_type (str), top_n (int, 默认 10)
- **返回**: 可转债列表，包含代码、名称、双低值、溢价率等

#### Scenario: 获取双低推荐
- **WHEN** 用户请求 `/api/strategy/recommend?strategy_type=double_low&top_n=10`
- **THEN** 系统返回双低值最低的前 10 只可转债

### Requirement: 单债详情接口
系统 SHALL 提供单只可转债的详细信息查询接口。

#### Endpoint: GET /api/bond/{ts_code}
- **参数**: ts_code (str)
- **返回**: 转债基本信息、当前因子值、正股信息

#### Scenario: 查询单债详情
- **WHEN** 用户请求 `/api/bond/123456.SZ`
- **THEN** 系统返回该转债的详细信息

### Requirement: 回测结果查询接口
系统 SHALL 提供回测结果查询接口，返回历史回测绩效数据。

#### Endpoint: GET /api/backtest/result
- **参数**: strategy_type (str), start_date (str), end_date (str)
- **返回**: 回测绩效指标和净值序列

#### Scenario: 查询回测结果
- **WHEN** 用户请求 `/api/backtest/result?strategy_type=double_low&start_date=2024-01-01&end_date=2024-12-31`
- **THEN** 系统返回该时间段的回测绩效数据

### Requirement: 接口文档自动生成
系统 SHALL 自动生成 OpenAPI 文档，支持 Swagger UI 访问。

#### Scenario: 访问 Swagger UI
- **WHEN** 用户访问 `/docs`
- **THEN** 系统展示完整的 API 文档和交互式测试界面
