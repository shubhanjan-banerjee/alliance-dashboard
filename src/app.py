# Streamlit app entry point
import streamlit as st
import logging
from ui.login import login_page
from ui.admin_dashboard import admin_dashboard
from ui.guest_dashboard import guest_dashboard
from db.database_operations import create_all_sqlite_tables, ensure_default_admin

logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s %(message)s')

# Ensure tables and default admin exist before any authentication
create_all_sqlite_tables()
ensure_default_admin()

st.title("Global Strategic Alliances Partner Performance Dashboard")

if 'logged_in' not in st.session_state:
    st.session_state['logged_in'] = False
    st.session_state['role'] = None
    st.session_state['username'] = None

if not st.session_state['logged_in']:
    login_page()
else:
    if st.session_state['role'] == 'admin':
        admin_dashboard()
    elif st.session_state['role'] == 'guest':
        guest_dashboard()
