import streamlit as st
import pandas as pd
from db.database_operations import get_all_performance_data, add_performance_record, update_performance_record, delete_performance_record
from utils.excel_parser import parse_performance_data
from st_aggrid import AgGrid, GridOptionsBuilder, GridUpdateMode

def render_dashboard_summary(df):
    import streamlit as st
    import plotly.express as px
    # Fallback: use emoji directly in metric labels, no emoji_icon import
    def emoji_icon(e):
        return e
    st.markdown("## 🏆 Dashboard Summary")
    col1, col2, col3, col4, col5 = st.columns(5)
    # Best Alliance
    best_alliance = df['alliance_type'].mode()[0] if not df.empty else '-'
    # Best BU
    best_bu = df['business_unit'].mode()[0] if not df.empty else '-'
    # Best Geo
    best_geo = df['geo'].mode()[0] if not df.empty else '-'
    # Best Associate
    best_associate = df['associate_name'].value_counts().idxmax() if not df.empty else '-'
    best_associate_count = df['associate_name'].value_counts().max() if not df.empty else 0
    # Metrics
    col1.metric(label=f"{emoji_icon('🤝')} Best Alliance", value=best_alliance)
    col2.metric(label=f"{emoji_icon('🏢')} Best BU", value=best_bu)
    col3.metric(label=f"{emoji_icon('🌍')} Best Geo", value=best_geo)
    col4.metric(label=f"{emoji_icon('👤')} Top Associate", value=best_associate)
    col5.metric(label=f"{emoji_icon('📜')} Most Certifications", value=best_associate_count)
    st.markdown("---")
    # Tiles/Cards for counts
    t1, t2, t3, t4 = st.columns(4)
    t1.metric(f"🎓 Total Certifications", len(df))
    t2.metric(f"👥 Unique Associates", df['associate_id'].nunique() if 'associate_id' in df.columns else df['associate_name'].nunique())
    t3.metric(f"📚 Unique Activities", df['activity_code'].nunique() if 'activity_code' in df.columns else 0)
    t4.metric(f"🤝 Unique Alliances", df['alliance_type'].nunique())
    st.markdown("---")
    # Monthly Report Dashboard
    st.markdown("### 📅 Monthly Certification Trend")
    if not df.empty:
        df['Month'] = pd.to_datetime(df['completion_date']).dt.to_period('M').astype(str)
        monthly = df.groupby('Month').size().reset_index(name='Certifications')
        fig = px.bar(monthly, x='Month', y='Certifications', color='Certifications', color_continuous_scale=px.colors.sequential.Blues, title='Monthly Certifications')
        fig.update_layout(xaxis_title='Month', yaxis_title='Certifications', plot_bgcolor='#f8f9fa', font_family='Open Sans', title_font_size=18)
        st.plotly_chart(fig, use_container_width=True)
    st.markdown("---")
    # Summary Details
    st.markdown("### 📊 Summary Details")
    st.dataframe(df.describe(include='all').T, use_container_width=True)
    st.markdown("---")
    # Rain effect for best associate (remove if streamlit_extras not available)
    # if best_associate != '-' and best_associate_count > 0:
    #     rain(emoji="🎉", font_size=32, falling_speed=5, animation_length="infinite")

def data_management_ui():
    # Always show upload option, even if no data
    st.header("Data Management")
    uploaded_file = st.file_uploader("Upload Performance Excel", type=["xlsx"])
    data_loaded = False
    upload_progress = st.empty()
    if uploaded_file:
        if 'file_uploaded_shown' not in st.session_state:
            with upload_progress:
                st.progress(100, text="File uploaded!")
            st.session_state['file_uploaded_shown'] = True
        df, errors = parse_performance_data(uploaded_file)
        upload_progress.empty()  # Hide upload progress bar after parsing
        if errors:
            st.error("\n".join(errors))
        else:
            load_progress = st.empty()
            if st.button("Load Performance Data"):
                from db.database_operations import get_sqlite_connection
                import os
                import datetime
                # Save uploaded file as backup with timestamp
                backup_dir = os.path.join(os.getcwd(), 'uploaded_backups')
                os.makedirs(backup_dir, exist_ok=True)
                timestamp = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
                backup_path = os.path.join(backup_dir, f'performance_backup_{timestamp}.xlsx')
                with open(backup_path, 'wb') as f:
                    f.write(uploaded_file.getbuffer())
                conn = get_sqlite_connection()
                if conn:
                    cursor = conn.cursor()
                    cursor.execute("DELETE FROM performance_data")
                    conn.commit()
                    cursor.close()
                    import time
                    time.sleep(0.2)
                    conn.close()
                total = len(df)
                to_insert = []
                for i, (_, row) in enumerate(df.iterrows()):
                    from db.database_operations import clean_date
                    raw_date = str(row.get('Completion Date', ''))
                    if ' ' in raw_date:
                        raw_date = raw_date.split(' ')[0]
                    if 'T' in raw_date:
                        raw_date = raw_date.split('T')[0]
                    date_val = clean_date(raw_date)
                    data = {
                        'associate_id': str(row.get('Associate ID', '') or '').strip(),
                        'associate_name': str(row.get('Associate Name', '') or '').strip(),
                        'activity_code': str(row.get('Activity Code', '') or '').strip(),
                        'alliance_type': str(row.get('Alliance Type', '') or '').strip(),
                        'business_unit': str(row.get('BU', '') or '').strip(),
                        'geo': str(row.get('Geo', '') or '').strip(),
                        'certification_name': str(row.get('Activity Name', '') or '').strip(),
                        'completion_date': date_val if date_val else '',
                        'feedback': None
                    }
                    required = ['associate_id','associate_name','activity_code','alliance_type','business_unit','geo','certification_name','completion_date']
                    if all(data[k] for k in required):
                        to_insert.append(data)
                    load_progress.progress(int((i+1)/total*100), text=f"Preparing data... ({i+1}/{total})")
                load_progress.progress(100, text="Inserting data into database...")
                if to_insert:
                    from db.database_operations import get_sqlite_connection
                    conn = get_sqlite_connection()
                    if conn:
                        cursor = conn.cursor()
                        cursor.executemany(
                            """
                            INSERT INTO performance_data (associate_id, associate_name, activity_code, alliance_type, business_unit, geo, certification_name, completion_date, feedback)
                            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                            """,
                            [(
                                d['associate_id'], d['associate_name'], d['activity_code'], d['alliance_type'], d['business_unit'],
                                d['geo'], d['certification_name'], d['completion_date'], d.get('feedback', None)
                            ) for d in to_insert]
                        )
                        conn.commit()
                        cursor.close()
                        conn.close()
                load_progress.empty()
                st.success("Performance data loaded and old data cleared.")
                st.session_state['file_uploader_clear'] = True  # Custom flag to clear uploader
                st.session_state['performance_data_loaded'] = False  # Reset so uploader is always visible
                st.rerun()
        data_loaded = True
    else:
        st.session_state.pop('file_uploaded_shown', None)
    # CRUD Table and Reports only if data exists
    from db.database_operations import get_all_performance_data, get_sqlite_connection
    df_perf = get_all_performance_data()
    # Add Delete All button with confirmation
    if df_perf is not None and not df_perf.empty:
        if st.button('Delete All Records', key='delete_all_btn'):
            st.session_state['show_delete_all_confirm'] = True
        if st.session_state.get('show_delete_all_confirm', False):
            st.warning('Are you sure you want to delete ALL performance records? This action cannot be undone!')
            col_del1, col_del2 = st.columns(2)
            with col_del1:
                if st.button('Confirm Delete All', key='confirm_delete_all'):
                    conn = get_sqlite_connection()
                    if conn:
                        cursor = conn.cursor()
                        cursor.execute('DELETE FROM performance_data')
                        conn.commit()
                        cursor.close()
                        conn.close()
                    st.success('All performance records deleted.')
                    st.session_state['show_delete_all_confirm'] = False
                    st.rerun()
            with col_del2:
                if st.button('Cancel', key='cancel_delete_all'):
                    st.session_state['show_delete_all_confirm'] = False
    else:
        st.info("No data available. Please upload an Excel file to populate the dashboard.")
    # Show Performance Data Table with associate_id and actions, with search, sort, pagination, and filter
    if df_perf is not None and not df_perf.empty:
        display_cols = [col for col in df_perf.columns if col in [
            'associate_id', 'associate_name', 'activity_code', 'certification_name', 'completion_date', 'alliance_type', 'business_unit', 'geo']]
        gb = GridOptionsBuilder.from_dataframe(df_perf[display_cols])
        gb.configure_pagination(paginationAutoPageSize=True)
        gb.configure_default_column(editable=False, groupable=True, filter=True, sortable=True, resizable=True)
        gb.configure_side_bar()
        gb.configure_grid_options(domLayout='normal')
        grid_options = gb.build()
        grid_response = AgGrid(
            df_perf[display_cols],
            gridOptions=grid_options,
            update_mode=GridUpdateMode.NO_UPDATE,
            enable_enterprise_modules=True,
            allow_unsafe_jscode=True,
            theme='streamlit',
            fit_columns_on_grid_load=True,
            height=400,
            width='100%'
        )
    # Add this at the end of the function to clear the uploader if needed
    if 'file_uploader_clear' in st.session_state and st.session_state['file_uploader_clear']:
        st.session_state['file_uploader_clear'] = False
        st.rerun()
