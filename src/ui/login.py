import streamlit as st
from auth.auth_utils import authenticate_admin

# Login UI components

def login_page():
    st.header("Login")
    tab1, tab2 = st.tabs(["Admin Login", "Guest Login"])
    with tab1:
        username = st.text_input("Username", key="admin_username")
        password = st.text_input("Password", type="password", key="admin_password")
        if st.button("Login", key="admin_login_btn"):
            if authenticate_admin(username, password):
                st.session_state['logged_in'] = True
                st.session_state['role'] = 'admin'
                st.session_state['username'] = username
                st.success("Login successful! Redirecting to admin dashboard...")
                st.rerun()
            else:
                st.error("Invalid username or password")
    with tab2:
        if st.button("Login as Guest", key="guest_login_btn"):
            st.session_state['logged_in'] = True
            st.session_state['role'] = 'guest'
            st.session_state['username'] = 'guest'
            st.success("Logged in as Guest. Redirecting to dashboard...")
            st.rerun()
