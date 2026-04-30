# YKZZ Quant - A股可转债策略研究工具

A股可转债（convertible bond）策略研究工具，支持数据采集、因子计算、策略筛选、回测分析。

## 功能特性

- **数据采集**: 集思录实时快照 + Tushare 历史行情
- **因子计算**: 转股价值、溢价率、双低值、剩余期限、YTM
- **策略筛选**: 双低策略、低溢价策略
- **风险过滤**: 规模、成交额、强赎、ST、临近到期
- **回测引擎**: 周频调仓向量化回测
- **Web 界面**: Streamlit 展示页面
- **API 接口**: FastAPI RESTful API

## 快速开始

### 安装

```bash
# 克隆项目
git clone <repo-url>
cd ykzz-quant

# 安装依赖
pip install -e .
```

### 配置

创建 `.env` 文件:

```bash
# 数据库 (默认 SQLite)
DATABASE_URL=sqlite:///./ykzz_quant.db

# 集思录 Cookie (可选，不配置只返回前30条数据)
JSL_COOKIE=your_jsl_cookie_here

# Tushare Token (可选，用于历史数据)
TUSHARE_TOKEN=your_tushare_token_here
```

### 获取集思录 Cookie

1. 访问 [集思录](https://www.jisilu.cn/) 并登录
2. 按 F12 打开开发者工具
3. 切换到 Network 标签
4. 刷新页面
5. 复制任意请求的 Cookie 头

### 获取 Tushare Token

1. 注册 [Tushare](https://tushare.pro/) 账号
2. 获取 API Token (需要 2000+ 积分)

## 使用方法

### 数据采集

```bash
python -m app.data.collect
```

### 因子计算

```bash
python -m app.factor.calculate
```

### 运行策略

```bash
# 双低策略
python -m app.strategy.run --strategy double_low --top-n 10

# 低溢价策略
python -m app.strategy.run --strategy low_premium --top-n 10
```

### 运行回测

```bash
python -m app.backtest.run --start 2024-01-01 --end 2024-12-31 --strategy double_low
```

### 启动 API 服务

```bash
uvicorn app.api.app:app --reload --port 8000
```

API 文档: http://localhost:8000/docs

### 启动 Web 界面

```bash
streamlit run app/ui/app.py
```

### 日更脚本

```bash
./scripts/daily_update.sh
```

## 项目结构

```
ykzz-quant/
├── app/
│   ├── api/           # FastAPI 接口
│   ├── backtest/      # 回测引擎
│   ├── data/          # 数据采集
│   ├── factor/        # 因子计算
│   ├── strategy/      # 策略筛选
│   ├── ui/            # Streamlit 界面
│   ├── config.py      # 配置管理
│   └── database.py    # 数据库连接
├── scripts/           # 脚本工具
├── tests/             # 测试代码
├── .env               # 环境变量
└── pyproject.toml     # 项目配置
```

## 技术栈

- Python 3.10+
- FastAPI + Uvicorn
- SQLAlchemy + SQLite
- Pandas + NumPy
- AkShare + Tushare
- Streamlit
- Matplotlib

## License

MIT
