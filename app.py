# app.py
import streamlit as st

st.set_page_config(page_title="Nurse Fatigue System", layout="wide", page_icon="🏥")

from pages.login import login_page
from pages.upload import upload_page
from pages.schedule import schedule_page
from pages.fatigue import fatigue_page
from pages.burnout import burnout_page

if "user" not in st.session_state:
    login_page()
else:
    role = st.session_state["role"]
    st.sidebar.title(f"Logged in: {st.session_state['user']} ({role})")
    if st.sidebar.button("Logout"):
        st.session_state.clear()
        st.rerun()

    pages = {
        "Upload & Schedule": upload_page,
        "Schedule View":     schedule_page,
        "Fatigue Scores":    fatigue_page,
        "Burnout Forecast":  burnout_page
    }

    if role == "Nurse":
        pages = {
            "Fatigue Scores":   fatigue_page,
            "Burnout Forecast": burnout_page
        }

    choice = st.sidebar.radio("Navigate", list(pages.keys()))
    pages[choice]()