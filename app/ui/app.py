import streamlit as st
import requests

API_BASE = "http://localhost:8000/api"

st.set_page_config(
    page_title="YKZZ Quant - 可转债策略工具",
    page_icon="📊",
    layout="wide",
)

st.title("📊 YKZZ Quant - A股可转债策略研究工具")

# Sidebar navigation
page = st.sidebar.selectbox(
    "导航",
    ["今日推荐", "全市场排名", "风险预警", "单债详情", "回测分析"],
)

if page == "今日推荐":
    st.header("今日策略推荐")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("双低策略")
        try:
            resp = requests.get(f"{API_BASE}/strategy/recommend", params={"strategy_type": "double_low", "top_n": 10})
            if resp.status_code == 200:
                data = resp.json()
                if data.get("data"):
                    st.dataframe(data["data"])
                else:
                    st.info("暂无推荐")
            else:
                st.error("获取数据失败")
        except Exception as e:
            st.error(f"API 连接失败: {e}")
    
    with col2:
        st.subheader("低溢价策略")
        try:
            resp = requests.get(f"{API_BASE}/strategy/recommend", params={"strategy_type": "low_premium", "top_n": 10})
            if resp.status_code == 200:
                data = resp.json()
                if data.get("data"):
                    st.dataframe(data["data"])
                else:
                    st.info("暂无推荐")
            else:
                st.error("获取数据失败")
        except Exception as e:
            st.error(f"API 连接失败: {e}")

elif page == "全市场排名":
    st.header("全市场可转债排名")
    st.info("功能开发中...")

elif page == "风险预警":
    st.header("风险预警")
    st.info("功能开发中...")

elif page == "单债详情":
    st.header("单债详情")
    ts_code = st.text_input("输入转债代码 (如 123456.SZ)")
    if ts_code:
        try:
            resp = requests.get(f"{API_BASE}/bond/{ts_code}")
            if resp.status_code == 200:
                data = resp.json()
                st.json(data)
            else:
                st.error("未找到该转债")
        except Exception as e:
            st.error(f"API 连接失败: {e}")

elif page == "回测分析":
    st.header("回测分析")
    st.info("功能开发中...")
