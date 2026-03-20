# pages/login.py
import streamlit as st

USERS = {
    "admin":   {"password": "admin123",  "role": "Admin"},
    "nurse1":  {"password": "nurse123",  "role": "Nurse"},
    "manager": {"password": "manager123","role": "Manager"},
}

def login_page():
    st.title("Nurse Fatigue Management System")
    st.subheader("Login")

    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        if st.button("Login", use_container_width=True):
            if username in USERS and USERS[username]["password"] == password:
                st.session_state["user"] = username
                st.session_state["role"] = USERS[username]["role"]
                st.success(f"Welcome {username}!")
                st.rerun()
            else:
                st.error("Invalid username or password")

        st.divider()
        st.caption("Demo credentials — Admin: admin/admin123 | Nurse: nurse1/nurse123 | Manager: manager/manager123")