# pages/schedule.py
import streamlit as st

def schedule_page():
    st.title("Schedule Page")

    st.write("This page is working!")

    if st.button("Generate Schedule"):
        st.success("Schedule generated!")