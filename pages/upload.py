# pages/upload.py
import streamlit as st
import pandas as pd
from engine.parser import load_all
from engine.nsga2 import run_nsga2
from engine.fatigue_model import compute_all_fatigue
from ml.burnout_model import train_burnout_model, get_model_stats

def upload_page():
    st.title("Upload Nurse Data & Generate Schedule")

    # Show dataset stats
    stats = get_model_stats()
    st.subheader("Training Dataset Status")
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("NSPLib files",      stats["nsplib_files"])
    col2.metric("Benchmark-24",      stats["benchmark24"])
    col3.metric("Benchmark-225",     stats["benchmark225"])
    col4.metric("Validation (ORTEC)", stats["validation_files"])

    # Train model button
    if not stats["model_trained"]:
        st.warning("Burnout model not trained yet.")
        if st.button("Train Burnout Model on All Datasets"):
            with st.spinner("Training on NSPLib + benchmarks... this takes 1-2 mins"):
                train_burnout_model()
            st.success("Model trained and saved!")
            st.rerun()
    else:
        st.success("Burnout model is trained and ready.")
        if st.button("Retrain Model"):
            with st.spinner("Retraining..."):
                train_burnout_model()
            st.success("Model retrained!")

    st.divider()

    # CSV Upload
    st.subheader("Upload Nurse Roster CSV")
    uploaded = st.file_uploader("Upload nurse CSV", type="csv")
    if uploaded:
        df = pd.read_csv(uploaded)
        st.dataframe(df)
        st.session_state["nurse_df"] = df

    st.divider()

    # GA Scheduler
    st.subheader("Generate Optimal Schedule via NSGA-II")
    col1, col2 = st.columns(2)
    generations = col1.slider("Generations", 10, 200, 50)
    pop_size    = col2.slider("Population size", 10, 100, 30)

    if st.button("Generate Optimal Schedule"):
        with st.spinner("Running NSGA-II — optimising fatigue + constraint violations..."):
            sc, weeks, hist = load_all(
                "data/inrc2", "Sc-n030w4.txt",
                [f"WD-n030w4-{i}.txt" for i in range(4)],
                "H0-n030w4-0.txt"
            )
            best, objectives = run_nsga2(
                sc, weeks, total_days=28,
                pop_size=pop_size, generations=generations
            )
            fatigue = compute_all_fatigue(best)
            st.session_state["schedule"]  = best
            st.session_state["fatigue"]   = fatigue
            st.session_state["scenario"]  = sc

        avg_f = sum(fatigue.values()) / len(fatigue)
        high  = sum(1 for v in fatigue.values() if v >= 60)
        st.success("Schedule generated successfully!")
        col1, col2, col3 = st.columns(3)
        col1.metric("Avg Fatigue Score", f"{avg_f:.1f}/100")
        col2.metric("High Risk Nurses",  high)
        col3.metric("Nurses Scheduled",  len(fatigue))