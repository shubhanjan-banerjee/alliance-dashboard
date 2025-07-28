# Reports UI components

import streamlit as st
import pandas as pd
import plotly.express as px
from db.database_operations import get_all_performance_data

def apply_filters(df):
    filters = st.session_state.get('filters', {})
    if not filters or df is None:
        return df
    if filters.get('alliance_type') and filters['alliance_type'] != 'All':
        df = df[df['alliance_type'] == filters['alliance_type']]
    if filters.get('business_unit') and filters['business_unit'] != 'All':
        df = df[df['business_unit'] == filters['business_unit']]
    if filters.get('geo') and filters['geo'] != 'All':
        df = df[df['geo'] == filters['geo']]
    if filters.get('date_range') and len(filters['date_range']) == 2:
        start, end = filters['date_range']
        df = df[(pd.to_datetime(df['completion_date']) >= pd.to_datetime(start)) & (pd.to_datetime(df['completion_date']) <= pd.to_datetime(end))]
    return df

def certifications_by_alliance_chart():
    df = get_all_performance_data()
    df = apply_filters(df)
    if df is not None and not df.empty:
        chart = px.bar(df, x='alliance_type', title='Certifications by Alliance Type')
        st.plotly_chart(chart, use_container_width=True)

def certifications_by_bu_chart():
    df = get_all_performance_data()
    df = apply_filters(df)
    if df is not None and not df.empty:
        chart = px.bar(df, x='business_unit', title='Certifications by Business Unit')
        st.plotly_chart(chart, use_container_width=True)

def certifications_by_geo_chart():
    df = get_all_performance_data()
    df = apply_filters(df)
    if df is not None and not df.empty:
        chart = px.pie(df, names='geo', title='Certifications by Geographical Region')
        st.plotly_chart(chart, use_container_width=True)

def monthly_trend_chart():
    df = get_all_performance_data()
    if df is None or df.empty:
        st.info("No data available. Please upload an Excel file to view the monthly trend chart.")
        return
    df = apply_filters(df)
    if df is not None and not df.empty:
        df['month'] = pd.to_datetime(df['completion_date']).dt.to_period('M').astype(str)
        chart = px.line(df.groupby('month').size().reset_index(name='count'), x='month', y='count', markers=True, title='Monthly Certification Completion Trend')
        st.plotly_chart(chart, use_container_width=True)

def export_dataframe(df, filename_prefix):
    import io
    st.download_button(
        label="Export to CSV",
        data=df.to_csv(index=False).encode('utf-8'),
        file_name=f"{filename_prefix}.csv",
        mime='text/csv'
    )
    # Fix: Use an in-memory BytesIO buffer for Excel export
    excel_buffer = io.BytesIO()
    df.to_excel(excel_buffer, index=False, engine='xlsxwriter')
    excel_buffer.seek(0)
    st.download_button(
        label="Export to Excel",
        data=excel_buffer,
        file_name=f"{filename_prefix}.xlsx",
        mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )
