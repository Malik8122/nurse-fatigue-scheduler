# pages/fatigue.py
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
from engine.fatigue_model import get_fatigue_label

def fatigue_page():
    st.title("Nurse Fatigue Scores")
    if "fatigue" not in st.session_state:
        st.warning("Go to Upload page and generate a schedule first.")
        return

    fatigue = st.session_state["fatigue"]
    df = pd.DataFrame([
        {"Nurse": nid, "Score": score, "Risk": get_fatigue_label(score)[0]}
        for nid, score in fatigue.items()
    ])

    # Summary metrics
    col1, col2, col3 = st.columns(3)
    col1.metric("High Risk (60-100)",   len(df[df.Risk == "High Risk"]),  delta_color="inverse")
    col2.metric("Moderate Risk (30-60)", len(df[df.Risk == "Moderate"]))
    col3.metric("Low Risk (0-30)",       len(df[df.Risk == "Low"]))

    # Bar chart
    fig = px.bar(
        df.sort_values("Score", ascending=False),
        x="Nurse", y="Score", color="Risk",
        color_discrete_map={"Low": "#10B981", "Moderate": "#F59E0B", "High Risk": "#EF4444"},
        title="Fatigue score per nurse (hospital regulation thresholds)",
        labels={"Score": "Fatigue Score (0-100)"}
    )
    fig.add_hline(y=60, line_dash="dash", line_color="red",
                  annotation_text="High Risk threshold (NHS)")
    fig.add_hline(y=30, line_dash="dash", line_color="orange",
                  annotation_text="Moderate threshold")
    st.plotly_chart(fig, use_container_width=True)

    # Gauge for selected nurse
    st.subheader("Individual Nurse Fatigue Gauge")
    selected_nurse = st.selectbox("Select nurse", df["Nurse"].tolist())
    score = fatigue[selected_nurse]
    label, color = get_fatigue_label(score)

    fig2 = go.Figure(go.Indicator(
        mode="gauge+number",
        value=score,
        title={"text": f"{selected_nurse} — {label}"},
        gauge={
            "axis": {"range": [0, 100]},
            "bar":  {"color": "#EF4444" if score >= 60 else "#F59E0B" if score >= 30 else "#10B981"},
            "steps": [
                {"range": [0,  30], "color": "#D1FAE5"},
                {"range": [30, 60], "color": "#FEF3C7"},
                {"range": [60,100], "color": "#FEE2E2"},
            ],
            "threshold": {
                "line":  {"color": "red", "width": 4},
                "thickness": 0.75, "value": 60
            }
        }
    ))
    st.plotly_chart(fig2, use_container_width=True)
    st.dataframe(df, use_container_width=True)