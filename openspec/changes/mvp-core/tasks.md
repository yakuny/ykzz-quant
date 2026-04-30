## 1. 项目初始化与基础设施

- [x] 1.1 创建 Python 项目结构（app/ 目录，含 data/factor/strategy/backtest/api/ui 子模块）
- [x] 1.2 初始化 SQLite 数据库，配置 SQLAlchemy ORM 模型
- [x] 1.3 添加项目依赖（akshare、tushare、fastapi、sqlalchemy、pandas、streamlit、uvicorn）
- [x] 1.4 创建配置管理模块（Pydantic BaseSettings，支持环境变量和 .env 文件）
- [x] 1.5 创建日志配置模块

## 2. 数据采集层（data-layer）

- [x] 2.1 实现 bond_snapshot 表的 ORM 模型
- [x] 2.2 实现 convert_price_history 表的 ORM 模型
- [x] 2.3 实现 bond_basic 表的 ORM 模型（存储转债基本信息）
- [x] 2.4 实现 stock_daily 表的 ORM 模型（存储正股行情）
- [x] 2.5 实现集思录数据采集器（bond_cb_jsl 接口调用，含 cookie 配置）
- [x] 2.6 实现 Tushare 历史行情采集器（cb_daily 接口，含频率限制控制）
- [x] 2.7 实现正股信息采集器
- [x] 2.8 实现转股价历史采集器（bond_cb_adj_logs_jsl 接口）
- [x] 2.9 创建数据采集主脚本，整合所有采集器

## 3. 因子计算层（factor-layer）

- [x] 3.1 实现转股价值计算模块
- [x] 3.2 实现转股溢价率计算模块
- [x] 3.3 实现双低值计算模块
- [x] 3.4 实现剩余期限计算模块
- [x] 3.5 实现到期收益率（YTM）计算模块
- [x] 3.6 创建因子计算主脚本，串联所有因子计算并更新数据库

## 4. 策略筛选层（strategy-layer）

- [x] 4.1 定义策略参数 Pydantic 模型（持仓数量、过滤阈值等）
- [x] 4.2 实现风险过滤模块（规模、成交额、强赎、ST、临近到期过滤）
- [x] 4.3 实现双低策略筛选器（按双低值升序排序）
- [x] 4.4 实现低溢价策略筛选器（按溢价率升序排序）
- [x] 4.5 创建策略运行主脚本

## 5. 回测引擎（backtest-layer）

- [x] 5.1 定义回测参数 Pydantic 模型（起止日期、策略类型、调仓频率等）
- [x] 5.2 实现历史数据加载模块（从数据库加载因子和行情数据）
- [x] 5.3 实现周频调仓逻辑（调仓日重新构建组合）
- [x] 5.4 实现手续费和滑点计算
- [x] 5.5 实现停牌处理逻辑
- [x] 5.6 实现绩效指标计算（累计收益、年化收益、最大回撤、夏普、胜率、换手率）
- [x] 5.7 实现净值曲线和回撤曲线可视化
- [x] 5.8 创建回测运行主脚本

## 6. API 接口层（api-layer）

- [x] 6.1 创建 FastAPI 应用入口
- [x] 6.2 实现策略推荐接口（GET /api/strategy/recommend）
- [x] 6.3 实现单债详情接口（GET /api/bond/{ts_code}）
- [x] 6.4 实现回测结果查询接口（GET /api/backtest/result）
- [x] 6.5 配置 CORS 和 Swagger UI 文档

## 7. Streamlit 展示层（ui-layer）

- [x] 7.1 创建 Streamlit 应用入口和页面导航
- [x] 7.2 实现今日推荐页面（双低和低溢价策略推荐列表）
- [x] 7.3 实现排名页面（多维度排序和筛选）
- [x] 7.4 实现风险预警页面（强赎、流动性、到期风险展示）
- [x] 7.5 实现单债详情页面

## 8. 日更调度与集成

- [x] 8.1 创建日更 shell 脚本（数据采集 → 因子计算 → 策略运行）
- [x] 8.2 编写项目 README 文档（安装、配置、使用说明）
- [x] 8.3 端到端测试：验证完整数据流（采集 → 因子 → 策略 → 展示）
