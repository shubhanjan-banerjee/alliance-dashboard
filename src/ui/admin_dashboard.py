import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
from db.database_operations import get_all_performance_data, add_performance_record, update_performance_record, delete_performance_record

def plot_cert_by_alliance(df):
    chart = px.bar(df.groupby('alliance_type').size().reset_index(name='Certifications'),
                   x='alliance_type', y='Certifications',
                   color='Certifications', color_continuous_scale=px.colors.sequential.Teal,
                   title='Certifications by Alliance Type')
    chart.update_layout(xaxis_title='', yaxis_title='Count', plot_bgcolor='#f8f9fa',
                       font_family='Open Sans', bargap=0.3, title_font_size=18)
    return chart

def plot_cert_by_bu(df):
    chart = px.bar(df.groupby('business_unit').size().reset_index(name='Certifications'),
                   x='business_unit', y='Certifications',
                   color='Certifications', color_continuous_scale=px.colors.sequential.Blues,
                   title='Certifications by Business Unit')
    chart.update_layout(xaxis_title='', yaxis_title='Count', plot_bgcolor='#f8f9fa',
                       font_family='Open Sans', bargap=0.3, title_font_size=18)
    return chart

def plot_cert_by_geo(df):
    chart = px.pie(df, names='geo', title='Certifications by Geographical Region',
                  hole=0.3, color_discrete_sequence=px.colors.sequential.RdBu)
    chart.update_traces(textinfo='percent+label', pull=[0.05]*len(df['geo'].unique()))
    chart.update_layout(font_family='Open Sans', plot_bgcolor='#f8f9fa')
    return chart

def plot_monthly_trend(df):
    df['Month'] = pd.to_datetime(df['completion_date']).dt.to_period('M').astype(str)
    chart = px.line(df.groupby('Month').size().reset_index(name='Certifications'),
                    x='Month', y='Certifications', markers=True,
                    title='Monthly Certification Completion Trend')
    chart.update_layout(xaxis_title='Month', yaxis_title='Certifications',
                       font_family='Open Sans', plot_bgcolor='#f8f9fa', title_font_size=18)
    return chart

def admin_dashboard():
    st.set_page_config(page_title="Global Alliances Dashboard", page_icon="🌐", layout="wide")
    st.markdown("""
        <style>
        html, body, [class*="css"]  { font-family: 'Open Sans', sans-serif; }
        .stTabs [data-baseweb="tab"] { border-radius: 12px 12px 0 0; }
        .stButton>button { border-radius: 8px; }
        .stTextInput>div>div>input { border-radius: 8px; }
        .stDataFrame { border-radius: 12px; }
        /* Add tooltips for help icons */
        .help-icon { cursor: pointer; color: #888; margin-left: 4px; }
        @media (max-width: 768px) {
            .stTabs [data-baseweb="tab"] { font-size: 14px; }
            .stDataFrame { font-size: 12px; }
            .block-container { padding: 0.5rem; }
        }
        </style>
    """, unsafe_allow_html=True)
    st.success(f"Welcome, {st.session_state['username']} (Admin)")
    tabs = st.tabs([
        "Dashboard Overview",
        "BU Wise Report",
        "Alliance Wise Report",
        "Data Management",
        "Profile / Settings"
    ])
    df_perf = get_all_performance_data()

    # --- Global Filters ---
    st.sidebar.header("Global Filters")
    alliance_types = ['All'] + sorted(df_perf['alliance_type'].dropna().unique().tolist())
    business_units = ['All'] + sorted(df_perf['business_unit'].dropna().unique().tolist())
    geos = ['All'] + sorted(df_perf['geo'].dropna().unique().tolist())
    selected_alliance = st.sidebar.selectbox("Alliance Type", alliance_types)
    selected_bu = st.sidebar.selectbox("Business Unit", business_units)
    selected_geo = st.sidebar.selectbox("Geo", geos)
    date_range = st.sidebar.date_input("Completion Date Range", [])
    # Apply filters
    filtered = df_perf.copy()
    if selected_alliance != 'All':
        filtered = filtered[filtered['alliance_type'] == selected_alliance]
    if selected_bu != 'All':
        filtered = filtered[filtered['business_unit'] == selected_bu]
    if selected_geo != 'All':
        filtered = filtered[filtered['geo'] == selected_geo]
    if date_range and len(date_range) == 2:
        filtered = filtered[(pd.to_datetime(filtered['completion_date']) >= pd.to_datetime(date_range[0])) &
                            (pd.to_datetime(filtered['completion_date']) <= pd.to_datetime(date_range[1]))]
    # --- Dashboard Overview ---
    # Add more useful graphs/charts for overall progress
    with tabs[0]:
        from ui.data_management import render_dashboard_summary
        render_dashboard_summary(filtered)
        st.plotly_chart(plot_cert_by_alliance(filtered), use_container_width=True, key="alliance_chart")
        st.plotly_chart(plot_cert_by_bu(filtered), use_container_width=True, key="bu_chart")
        st.plotly_chart(plot_cert_by_geo(filtered), use_container_width=True, key="geo_chart")
        st.plotly_chart(plot_monthly_trend(filtered), use_container_width=True, key="monthly_trend_chart")
        # New: Certifications by Month and Alliance
        if 'alliance_type' in filtered.columns:
            month_alliance = filtered.copy()
            month_alliance['Month'] = pd.to_datetime(month_alliance['completion_date']).dt.to_period('M').astype(str)
            # Defensive: Use 'associate_id' if present, else fallback to 'id' or 'associate_name'
            value_col = 'associate_id' if 'associate_id' in month_alliance.columns else (
                'id' if 'id' in month_alliance.columns else 'associate_name')
            pivot = month_alliance.pivot_table(index='Month', columns='alliance_type', values=value_col, aggfunc='count', fill_value=0)
            st.subheader("Monthly Certifications by Alliance Type")
            st.line_chart(pivot)  # Removed key argument, not supported by st.line_chart
        # New: Certifications by BU and Geo
        if 'business_unit' in filtered.columns and 'geo' in filtered.columns:
            bu_geo = filtered.groupby(['business_unit', 'geo']).size().reset_index(name='Certifications')
            st.subheader("Certifications by BU and Geo")
            st.bar_chart(bu_geo.pivot(index='business_unit', columns='geo', values='Certifications').fillna(0))  # Removed key argument
    # --- BU Wise Report ---
    with tabs[1]:
        st.header("BU Wise Report")
        bu_group = filtered.groupby('business_unit').size().reset_index(name='Certifications')
        st.dataframe(bu_group, use_container_width=True)
        st.plotly_chart(plot_cert_by_bu(filtered), use_container_width=True)
    # --- Alliance Wise Report ---
    with tabs[2]:
        st.header("Alliance Wise Report")
        all_group = filtered.groupby('alliance_type').size().reset_index(name='Certifications')
        st.dataframe(all_group, use_container_width=True)
        st.plotly_chart(plot_cert_by_alliance(filtered), use_container_width=True)
    # --- Data Management ---
    with tabs[3]:
        from ui.data_management import data_management_ui
        data_management_ui()
    # --- Profile / Settings ---
    with tabs[4]:
        st.header("Profile / Change Password")
        with st.form("change_password_form"):
            st.write(f"Username: {st.session_state['username']}")
            current_pw = st.text_input("Current Password", type="password")
            new_pw = st.text_input("New Password", type="password")
            confirm_pw = st.text_input("Confirm New Password", type="password")
            submitted = st.form_submit_button("Change Password")
        if submitted:
            if new_pw != confirm_pw:
                st.error("New passwords do not match.")
            elif len(new_pw) < 8:
                st.error("New password must be at least 8 characters.")
            else:
                from auth.auth_utils import change_admin_password
                success, msg = change_admin_password(st.session_state['username'], current_pw, new_pw)
                if success:
                    st.success(msg)
                else:
                    st.error(msg)
    if st.button("Logout", key="admin_logout"):
        st.session_state['logged_in'] = False
        st.session_state['role'] = None
        st.session_state['username'] = None
        st.rerun()
    st.markdown("""
        <footer style='text-align:center; color:gray; font-size:0.9em; margin-top:2em;'>
            Global Strategic Alliances Partner Performance Dashboard &copy; 2025
        </footer>
    """, unsafe_allow_html=True)
