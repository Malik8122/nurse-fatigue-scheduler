# pages/schedule.py
import streamlit as st
import pandas as pd
import plotly.express as px

SHIFT_COLOR = {
    "Early": "#3B82F6", "Day": "#10B981",
    "Late":  "#F59E0B", "Night": "#6366F1", "Off": "#E5E7EB"
}
DAYS = ["Mon","Tue","Wed","Thu","Fri","Sat","Sun"] * 4

def schedule_page():
    st.title("Shift Schedule Calendar")
    if "schedule" not in st.session_state:
        st.warning("Go to Upload page and generate a schedule first.")
        return

    schedule = st.session_state["schedule"]

    # Filter by nurse
    nurse_ids = list(schedule.keys())
    selected = st.multiselect("Filter nurses", nurse_ids, default=nurse_ids[:10])
    if not selected:
        selected = nurse_ids[:10]

    # Build calendar table
    rows = []
    for nid in selected:
        shifts = schedule[nid]
        for d, shift in enumerate(shifts):
            rows.append({
                "Nurse": nid,
                "Day":   f"W{d//7+1}-{DAYS[d]}",
                "Shift": shift
            })

    df = pd.DataFrame(rows)
    pivot = df.pivot(index="Nurse", columns="Day", values="Shift")
    st.dataframe(pivot, use_container_width=True)

    # Shift distribution chart
    st.subheader("Shift Distribution")
    all_shifts = [s for shifts in schedule.values() for s in shifts]
    dist = pd.Series(all_shifts).value_counts().reset_index()
    dist.columns = ["Shift", "Count"]
    fig = px.bar(dist, x="Shift", y="Count",
                 color="Shift",
                 color_discrete_map=SHIFT_COLOR)
    st.plotly_chart(fig, use_container_width=True)

    # Violations
    st.subheader("Constraint Violations")
    violations = []
    for nid, shifts in schedule.items():
        for i in range(len(shifts) - 1):
            if shifts[i] == "Night" and shifts[i+1] in ["Early", "Day"]:
                violations.append({
                    "Nurse": nid,
                    "Issue": f"Night → {shifts[i+1]}",
                    "Day":   f"Day {i+1} → {i+2}"
                })
        consec = streak = 0
        for s in shifts:
            streak = streak + 1 if s != "Off" else 0
            consec = max(consec, streak)
        if consec > 6:
            violations.append({
                "Nurse": nid,
                "Issue": f"{consec} consecutive working days",
                "Day":   "Multiple days"
            })

    if violations:
        st.dataframe(pd.DataFrame(violations), use_container_width=True)
    else:
        st.success("No hard constraint violations found!")