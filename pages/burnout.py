# pages/burnout.py
import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
from ml.burnout_model import predict_burnout_30days
from fpdf import FPDF
import datetime

def burnout_page():
    st.title("30-Day Burnout Forecast")
    if "schedule" not in st.session_state:
        st.warning("Go to Upload page and generate a schedule first.")
        return

    with st.spinner("Running burnout prediction model..."):
        predictions = predict_burnout_30days(st.session_state["schedule"])

    df = pd.DataFrame([
        {"Nurse": k, "Burnout Risk (%)": v,
         "Risk Level": "High" if v > 70 else "Moderate" if v > 40 else "Low"}
        for k, v in predictions.items()
    ]).sort_values("Burnout Risk (%)", ascending=False)

    # Summary
    col1, col2, col3 = st.columns(3)
    col1.metric("High Burnout Risk (>70%)",    len(df[df["Risk Level"] == "High"]))
    col2.metric("Moderate Risk (40-70%)",       len(df[df["Risk Level"] == "Moderate"]))
    col3.metric("Low Risk (<40%)",              len(df[df["Risk Level"] == "Low"]))

    # Bar chart
    fig = go.Figure(go.Bar(
        x=df["Nurse"],
        y=df["Burnout Risk (%)"],
        marker_color=[
            "#EF4444" if v > 70 else "#F59E0B" if v > 40 else "#10B981"
            for v in df["Burnout Risk (%)"]
        ]
    ))
    fig.update_layout(
        title="Predicted burnout risk — next 30 days",
        yaxis_range=[0, 100],
        xaxis_title="Nurse", yaxis_title="Burnout Risk (%)"
    )
    fig.add_hline(y=70, line_dash="dash", line_color="red",
                  annotation_text="High risk threshold")
    st.plotly_chart(fig, use_container_width=True)

    # Trend forecast line chart
    st.subheader("Risk Trend (simulated 30-day projection)")
    top5 = df.head(5)["Nurse"].tolist()
    days = list(range(1, 31))
    fig2 = go.Figure()
    for nurse in top5:
        base = predictions[nurse]
        trend = [min(100, base + i * 0.3 + (i % 7 == 6) * 2) for i in days]
        fig2.add_trace(go.Scatter(x=days, y=trend, mode="lines", name=nurse))
    fig2.update_layout(title="Top 5 at-risk nurses — 30-day projection",
                       xaxis_title="Day", yaxis_title="Risk (%)")
    st.plotly_chart(fig2, use_container_width=True)

    # Recommendations
    st.subheader("Recommended Actions")
    high_risk = df[df["Risk Level"] == "High"]["Nurse"].tolist()
    if high_risk:
        for nurse in high_risk:
            st.error(f"{nurse}: Recommend immediate schedule adjustment — reduce night shifts")
    moderate = df[df["Risk Level"] == "Moderate"]["Nurse"].tolist()
    if moderate:
        for nurse in moderate[:3]:
            st.warning(f"{nurse}: Monitor closely — consider adding a rest day")

    st.divider()

    # Export PDF
    if st.button("Export Full Report as PDF"):
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Helvetica", "B", 16)
        pdf.cell(0, 10, "Nurse Burnout Forecast Report", ln=True, align="C")
        pdf.set_font("Helvetica", size=10)
        pdf.cell(0, 8, f"Generated: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M')}", ln=True)
        pdf.ln(5)
        pdf.set_font("Helvetica", "B", 12)
        pdf.cell(0, 8, "Burnout Risk Summary", ln=True)
        pdf.set_font("Helvetica", size=10)
        for _, row in df.iterrows():
            level = row["Risk Level"]
            pdf.cell(0, 7,
                     f"{row['Nurse']}: {row['Burnout Risk (%)']:.1f}% — {level}",
                     ln=True)
        pdf.output("burnout_report.pdf")
        with open("burnout_report.pdf", "rb") as f:
            st.download_button("Download PDF", f,
                               file_name="burnout_report.pdf",
                               mime="application/pdf")
burnout_page()