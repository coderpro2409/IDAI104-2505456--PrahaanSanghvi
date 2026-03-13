# 🚀 Space Mission Analytics Dashboard

> Interactive dashboard exploring rocket missions, payloads, costs, and mission outcomes — built with Python and Streamlit.

---

## Introduction

The Space Mission Analytics Dashboard is an interactive, browser-based data visualization application built with Python and Streamlit. It transforms a raw dataset of simulated space missions into a rich, explorable environment. Users can filter missions by launch vehicle and mission type, then examine a series of charts covering fuel usage, mission costs, success rates, crew size, and scientific yield — all updating in real time from a single sidebar.

---

## The Dataset

All visualizations are powered by `space_missions_dataset.csv`, where each row represents one simulated space mission. The dataset includes the following columns:

| Column | Type | Description |
|---|---|---|
| Mission ID | String | Unique identifier (MSN-0001 to MSN-0500) |
| Mission Name | String | Human-readable mission label |
| Launch Date | Date | Calendar date; converted to datetime on load |
| Target Type | Categorical | Type of celestial body (star, exoplanet, asteroid, etc.) |
| Target Name | String | Specific destination (e.g., Titan, Mars) |
| Mission Type | Categorical | Purpose: exploration, colonization, scientific survey, etc. |
| Distance from Earth (light-years) | Float | Distance to target |
| Mission Duration (years) | Float | Total mission length |
| Mission Cost (billion USD) | Float | Total cost in billions |
| Scientific Yield (points) | Float | Measured scientific output |
| Crew Size | Integer | Number of crew members |
| Mission Success (%) | Float | Success percentage (0–100) |
| Fuel Consumption (tons) | Float | Total fuel burned |
| Payload Weight (tons) | Float | Total payload carried |
| Launch Vehicle | Categorical | Rocket system used (e.g., SLS, Starship) |

On load, the app converts `Launch Date` to a proper datetime, coerces all numeric columns with `pd.to_numeric()`, and drops rows with missing values before rendering any chart.

---

## Sidebar and Filters

The sidebar serves as the app's control panel and contains two filters:

- **Launch Vehicle** — a selectbox to choose one rocket system (e.g., SLS, Starship).
- **Mission Type** — a selectbox to choose one mission category (e.g., exploration, colonization).

When either filter changes, Streamlit recomputes a filtered dataframe using a boolean mask and passes it to every chart and the preview table simultaneously — ensuring all visuals always reflect the same data slice.

---

## Dataset Preview

At the top of the main area, a filtered table shows the first several rows of the currently filtered dataset via `st.dataframe()`. This provides immediate transparency — the user can verify which missions are in scope before interpreting any chart.

---

## Charts and Visualizations

All charts update in real time whenever a sidebar filter changes. The following visualizations are included:

### Correlation Heatmap

A Seaborn heatmap showing Pearson correlation coefficients between all numeric columns. The `coolwarm` color scale runs from red (strong negative) through white (no relationship) to blue (strong positive), with numeric values annotated in each cell. Numeric columns included: Distance from Earth, Mission Duration, Mission Cost, Scientific Yield, Crew Size, Mission Success, Fuel Consumption, and Payload Weight.

### Payload Weight vs Fuel Consumption

A Plotly scatter plot with Payload Weight (tons) on the x-axis and Fuel Consumption (tons) on the y-axis, colored by Mission Type. Hovering reveals the Mission Name, Launch Vehicle, and Mission Cost — useful for identifying outliers that consumed far more fuel than their payload weight would suggest.

### Mission Cost vs Mission Success

A Plotly bar chart comparing average Mission Cost (billion USD) for successful versus failed missions. Missions are classified based on whether their success rate exceeds 50%. This chart directly tests whether higher spending correlates with better outcomes.

### Mission Duration vs Distance from Earth

A Plotly line chart with Distance from Earth (light-years) on the x-axis and Mission Duration (years) on the y-axis. Data is sorted by distance before plotting. Hovering reveals the Mission Name and Launch Vehicle, making it easy to investigate whether more distant targets always require longer missions.

### Crew Size vs Mission Success

A Plotly box plot with Crew Size on the x-axis and Mission Success (%) on the y-axis, colored by Mission Type. Box plots expose the median, quartile spread, and outliers for each crew size group — revealing whether larger crews are associated with more consistent or higher success rates.

### Scientific Yield vs Mission Cost

A Plotly scatter plot with Mission Cost (billion USD) on the x-axis and Scientific Yield (points) on the y-axis, colored by Mission Type. Hovering reveals Mission Name and Launch Vehicle, allowing investigation of whether more expensive missions deliver proportionally greater scientific value.

---

## Technical Implementation

### Stack

| Library | Role |
|---|---|
| Streamlit | Web framework, widgets, layout |
| pandas | Data loading, cleaning, filtering, aggregation |
| Plotly Express | Interactive scatter, bar, line, and box charts |
| Seaborn / Matplotlib | Correlation heatmap |

### Filtering Logic

The sidebar widgets return a single selected value each. The filtered dataframe is computed as:

```python
filtered = df[
    (df["Launch Vehicle"] == vehicle) &
    (df["Mission Type"] == mission_type)
]
```

This single filtered object is passed to every chart and the preview table.

### File Structure

```
├── app.py                        # All application logic and charts
├── space_missions_dataset.csv    # Mission dataset
└── requirements.txt              # Python dependencies
```

---

## Running the App

### Local Setup

Install dependencies:

```bash
pip install -r requirements.txt
```

Run the app:

```bash
streamlit run app.py
```

The app will open in your browser at `http://localhost:8501`.

### Requirements

- `streamlit >= 1.35.0`
- `pandas >= 2.0.0`
- `plotly >= 5.0.0`
- `seaborn >= 0.12.0`
- `matplotlib >= 3.5.0`

### Deployment on Streamlit Cloud

Push the repository to GitHub (ensuring `app.py`, `space_missions_dataset.csv`, and `requirements.txt` are all present), then connect the repository in the Streamlit Cloud dashboard. The app will be live at a public URL within minutes — no build step or configuration required.

---

## Educational Value

This dashboard demonstrates several core data science concepts in applied form:

- **Statistics** — correlation coefficients, distribution shapes, and group comparisons via box plots, scatter plots, and heatmaps.
- **Data engineering** — loading, cleaning, type conversion, and filtering a tabular dataset with pandas.
- **Data visualization** — selecting the right chart type for each question: scatter for relationships, box for distributions, line for trends, bar for group comparisons, heatmap for correlation matrices.
- **Software design** — centralizing filter state in the sidebar and passing a single filtered dataframe to all outputs for consistency across charts.

The interactive nature of the app reinforces learning: users can form a hypothesis (e.g., heavier payloads require more fuel), apply filters to test it, and observe results across multiple linked charts simultaneously.
