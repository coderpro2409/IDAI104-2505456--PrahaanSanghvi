import streamlit as st
import pandas as pd
import plotly.express as px
import seaborn as sns
import matplotlib.pyplot as plt

# -----------------------------
# PAGE CONFIG
# -----------------------------
st.set_page_config(
    page_title="Space Mission Dashboard",
    layout="wide"
)

st.title("🚀 Space Mission Analytics Dashboard")
st.write("Interactive dashboard exploring rocket missions, payloads, costs, and mission outcomes.")

# -----------------------------
# LOAD DATA
# -----------------------------
df = pd.read_csv("space_missions_dataset.csv")

# Convert launch date
df["Launch Date"] = pd.to_datetime(df["Launch Date"])

# Clean dataset
df = df.dropna()
df = df.drop_duplicates()

# -----------------------------
# SIDEBAR FILTERS
# -----------------------------
st.sidebar.header("Filter Missions")

vehicle = st.sidebar.selectbox(
    "Select Launch Vehicle",
    df["Launch Vehicle"].unique()
)

mission_type = st.sidebar.selectbox(
    "Select Mission Type",
    df["Mission Type"].unique()
)

filtered = df[
    (df["Launch Vehicle"] == vehicle) &
    (df["Mission Type"] == mission_type)
]

# -----------------------------
# DATA PREVIEW
# -----------------------------
st.subheader("Dataset Preview")

st.dataframe(filtered.head())

# -----------------------------
# CORRELATION HEATMAP
# -----------------------------
st.subheader("Correlation Heatmap")

numeric_cols = [
"Distance from Earth (light-years)",
"Mission Duration (years)",
"Mission Cost (billion USD)",
"Scientific Yield (points)",
"Crew Size",
"Mission Success (%)",
"Fuel Consumption (tons)",
"Payload Weight (tons)"
]

fig_heat, ax = plt.subplots(figsize=(8,6))
sns.heatmap(filtered[numeric_cols].corr(), annot=True, cmap="coolwarm", ax=ax)

st.pyplot(fig_heat)

# -----------------------------
# PAYLOAD VS FUEL
# -----------------------------
st.subheader("Payload Weight vs Fuel Consumption")

fig1 = px.scatter(
    filtered,
    x="Payload Weight (tons)",
    y="Fuel Consumption (tons)",
    color="Mission Type",
    hover_data=[
        "Mission Name",
        "Launch Vehicle",
        "Mission Cost (billion USD)"
    ],
    title="Payload Weight vs Fuel Consumption"
)

st.plotly_chart(fig1, use_container_width=True)

# -----------------------------
# MISSION COST VS SUCCESS
# -----------------------------
st.subheader("Mission Cost vs Mission Success")

filtered["Success Category"] = filtered["Mission Success (%)"] > 50

cost_data = filtered.groupby("Success Category")["Mission Cost (billion USD)"].mean().reset_index()

fig2 = px.bar(
    cost_data,
    x="Success Category",
    y="Mission Cost (billion USD)",
    color="Success Category",
    title="Average Mission Cost for Successful vs Failed Missions"
)

st.plotly_chart(fig2, use_container_width=True)

# -----------------------------
# DISTANCE VS DURATION
# -----------------------------
st.subheader("Mission Duration vs Distance from Earth")

fig3 = px.line(
    filtered.sort_values("Distance from Earth (light-years)"),
    x="Distance from Earth (light-years)",
    y="Mission Duration (years)",
    hover_data=["Mission Name", "Launch Vehicle"],
    title="Mission Duration vs Distance"
)

st.plotly_chart(fig3, use_container_width=True)

# -----------------------------
# CREW SIZE VS SUCCESS
# -----------------------------
st.subheader("Crew Size vs Mission Success")

fig4 = px.box(
    filtered,
    x="Crew Size",
    y="Mission Success (%)",
    color="Mission Type",
    hover_data=["Mission Name"],
    title="Crew Size vs Mission Success"
)

st.plotly_chart(fig4, use_container_width=True)

# -----------------------------
# SCIENTIFIC YIELD VS COST
# -----------------------------
st.subheader("Scientific Yield vs Mission Cost")

fig5 = px.scatter(
    filtered,
    x="Mission Cost (billion USD)",
    y="Scientific Yield (points)",
    color="Mission Type",
    hover_data=["Mission Name", "Launch Vehicle"],
    title="Scientific Yield vs Mission Cost"
)

st.plotly_chart(fig5, use_container_width=True)
