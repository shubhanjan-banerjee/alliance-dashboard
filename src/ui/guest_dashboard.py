import streamlit as st
import pandas as pd
from db.database_operations import get_sqlite_connection

# Guest dashboard UI components
def guest_dashboard():
    from db.database_operations import get_all_performance_data
    df_perf = get_all_performance_data()
    if df_perf is None or df_perf.empty:
        st.info("No data available. Please contact an admin to upload an Excel file in the Data Management tab.")
        return

    st.info(f"Welcome, Guest!")
    tabs = st.tabs(["Dashboard Overview", "BU Wise Report", "Alliance Wise Report", "Cost Savings"])
    # Dashboard Overview
    with tabs[0]:
        st.header("Key Performance Highlights (Read-Only)")
        from ui.reports import certifications_by_alliance_chart, certifications_by_bu_chart, certifications_by_geo_chart, monthly_trend_chart
        certifications_by_alliance_chart()
        certifications_by_bu_chart()
        certifications_by_geo_chart()
        monthly_trend_chart()
    # BU Wise Report
    with tabs[1]:
        st.header("BU Wise Report (Read-Only)")
        st.write("[BU metrics table and charts]")
    # Alliance Wise Report
    with tabs[2]:
        st.header("Alliance Wise Report (Read-Only)")
        st.write("[Alliance metrics table and charts]")
    # Cost Savings
    with tabs[3]:
        st.header("Cost Savings (Read-Only)")
        st.write("[Cost savings table and charts]")
    if st.button("Logout", key="guest_logout"):
        st.session_state['logged_in'] = False
        st.session_state['role'] = None
        st.session_state['username'] = None
        st.rerun()
