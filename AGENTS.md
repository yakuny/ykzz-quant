# AGENTS.md

## Project Overview

A股可转债（convertible bond）策略研究工具。MVP 目标：数据采集 → 因子计算 → 策略筛选 → 回测 → 展示。

## Current State

No application code yet. All planning lives in `openspec/changes/mvp-core/`:
- `proposal.md` — what & why
- `design.md` — how, key technical decisions
- `specs/` — capability specs (being created)
- `tasks.md` — implementation tasks (pending)

Use `openspec status --change mvp-core --json` to check progress.

## Planned Tech Stack

Python / FastAPI / SQLAlchemy / pandas / SQLite (MVP) / Streamlit

Data sources: 集思录 (AkShare `bond_cb_jsl`, requires cookie) + Tushare (history, 2000+ points)

## Openspec Workflow

This repo uses OpenSpec for change management. Key commands:
- `openspec new change "<name>"` — create a change
- `openspec status --change "<name>" --json` — check artifact status
- `openspec instructions <artifact> --change "<name>" --json` — get build instructions

Skills in `.opencode/skills/`:
- `openspec-propose` — create change with all artifacts
- `openspec-apply-change` — implement tasks from a change
- `openspec-explore` — think through ideas before committing
- `openspec-archive-change` — archive completed changes

## Key Decisions (from design.md)

- **数据源**: 集思录实时快照为主力因子来源，Tushare 历史行情补齐回测数据
- **数据库**: SQLite for MVP（全市场 ~600 只，数据量小），SQLAlchemy ORM 可无成本迁移 PostgreSQL
- **回测**: pandas 向量化，不做事件驱动框架（Backtrader 不适配多标的轮动）
- **双低公式**: `双低值 = 转债价格 + 100 × 转股溢价率(%)`，注意口径统一
- **纯债价值**: 推迟到 Change 2，MVP 不做低价防守策略

## Data Source Gotchas

- `bond_cb_jsl` 无集思录 cookie 只返回前 30 条（全量 ~560 条）
- 集思录 cookie 需手动获取：登录 → F12 → Network → 复制 Cookie
- AkShare 接口因网站改版频繁 break，版本更新时检查 changelog
- Tushare 调用有频率限制（2000 积分: 200次/分钟），历史回补需控制节奏
