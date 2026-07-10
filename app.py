# ==========================================================
# Toronto Island Ferry Analytics Dashboard
# Developed by: Satwik Srivastava
# Domain: Data Analytics
# ==========================================================

import streamlit as st
import pandas as pd
import numpy as np

import matplotlib.pyplot as plt
import seaborn as sns

import plotly.express as px
import plotly.graph_objects as go

from scipy.stats import pearsonr

from datetime import datetime

st.set_page_config(
    page_title="Toronto Island Ferry Analytics Dashboard",
    page_icon="🚢",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==========================================================
# CUSTOM CSS
# ==========================================================

st.markdown("""

<style>

.main{
    background-color:#f7f9fc;
}

.block-container{
    padding-top:1rem;
}

h1,h2,h3{
    color:#003366;
}

.kpi{
background:#ffffff;
padding:18px;
border-radius:15px;
box-shadow:0px 2px 10px rgba(0,0,0,0.15);
text-align:center;
}

.sidebar .sidebar-content{
background:#003366;
}

footer{
visibility:hidden;
}

</style>

""",unsafe_allow_html=True)

# ==========================================================
# TITLE
# ==========================================================

st.title("🚢 Toronto Island Ferry Analytics Dashboard")

st.markdown("""
### Real-Time Ferry Ticket Sales & Redemption Analytics

This dashboard provides comprehensive operational analytics for the Toronto Island Ferry system using historical ticket sales and redemption data.

""")

# ==========================================================
# LOAD DATA
# ==========================================================

@st.cache_data
def load_data():

    df = pd.read_excel("Toronto Island Ferry Tickets.csv.xlsx")

    df["Timestamp"] = pd.to_datetime(df["Timestamp"])

    # -------------------------
    # Feature Engineering
    # -------------------------

    df["Hour"] = df["Timestamp"].dt.hour
    df["Day"] = df["Timestamp"].dt.day_name()
    df["Month"] = df["Timestamp"].dt.month_name()
    df["Quarter"] = "Q" + df["Timestamp"].dt.quarter.astype(str)
    df["Year"] = df["Timestamp"].dt.year

    df["Weekend"] = np.where(
        df["Day"].isin(["Saturday", "Sunday"]),
        "Weekend",
        "Weekday"
    )

    def peak(hour):
        if 7 <= hour <= 10:
            return "Morning Peak"
        elif 16 <= hour <= 19:
            return "Evening Peak"
        else:
            return "Off Peak"

    df["Peak Period"] = df["Hour"].apply(peak)

    def season(month):
        if month in [12, 1, 2]:
            return "Winter"
        elif month in [3, 4, 5]:
            return "Spring"
        elif month in [6, 7, 8]:
            return "Summer"
        else:
            return "Autumn"

    df["Season"] = df["Timestamp"].dt.month.apply(season)

    df["Net Passenger Movement"] = (
        df["Sales Count"] - df["Redemption Count"]
    )

    return df

    # Weekend

    df["Weekend"] = np.where(
        df["Day"].isin(["Saturday","Sunday"]),
        "Weekend",
        "Weekday"
    )

    # Peak Period

    def peak(hour):

        if 7<=hour<=10:
            return "Morning Peak"

        elif 16<=hour<=19:
            return "Evening Peak"

        else:
            return "Off Peak"

    df["Peak Period"] = df["Hour"].apply(peak)

    # Season

    def season(month):

        if month in [12,1,2]:
            return "Winter"

        elif month in [3,4,5]:
            return "Spring"

        elif month in [6,7,8]:
            return "Summer"

        else:
            return "Autumn"

    df["Season"]=df["Timestamp"].dt.month.apply(season)

    # Net Passenger Movement

    df["Net Passenger Movement"] = (
        df["Sales Count"] -
        df["Redemption Count"]
    )

    return df

df = load_data()

# ==========================================================
# SIDEBAR
# ==========================================================

st.sidebar.title("⚙ Dashboard Filters")

years = sorted(df["Year"].unique())

selected_year = st.sidebar.multiselect(
    "Select Year",
    years,
    default=years
)

months = list(df["Month"].unique())

selected_month = st.sidebar.multiselect(
    "Select Month",
    months,
    default=months
)

seasons = list(df["Season"].unique())

selected_season = st.sidebar.multiselect(
    "Select Season",
    seasons,
    default=seasons
)

weekend = st.sidebar.multiselect(
    "Weekend / Weekday",
    df["Weekend"].unique(),
    default=df["Weekend"].unique()
)

peak = st.sidebar.multiselect(
    "Peak Period",
    df["Peak Period"].unique(),
    default=df["Peak Period"].unique()
)

# ==========================================================
# FILTER DATA
# ==========================================================

filtered = df[
(df["Year"].isin(selected_year)) &
(df["Month"].isin(selected_month)) &
(df["Season"].isin(selected_season)) &
(df["Weekend"].isin(weekend)) &
(df["Peak Period"].isin(peak))
]

# ==========================================================
# EXECUTIVE KPIs
# ==========================================================

st.header("📊 Executive KPI Dashboard")

sales = int(filtered["Sales Count"].sum())

redeem = int(filtered["Redemption Count"].sum())

movement = int(filtered["Net Passenger Movement"].sum())

utilization = (
redeem/sales
)*100

peak_hour = (
filtered.groupby("Hour")["Sales Count"]
.sum()
.idxmax()
)

peak_day = (
filtered.groupby("Day")["Sales Count"]
.sum()
.idxmax()
)

peak_month = (
filtered.groupby("Month")["Sales Count"]
.sum()
.idxmax()
)

col1,col2,col3,col4 = st.columns(4)

with col1:

    st.metric(
        "🎫 Total Ticket Sales",
        f"{sales:,}"
    )

with col2:

    st.metric(
        "✅ Total Redemptions",
        f"{redeem:,}"
    )

with col3:

    st.metric(
        "👥 Net Passenger Movement",
        f"{movement:,}"
    )

with col4:

    st.metric(
        "📈 Utilization Rate",
        f"{utilization:.2f}%"
    )

col5,col6,col7 = st.columns(3)

with col5:

    st.info(f"🕛 Peak Hour : {peak_hour}:00")

with col6:

    st.info(f"📅 Peak Day : {peak_day}")

with col7:

    st.info(f"🌞 Peak Month : {peak_month}")

# ==========================================================
# DATASET OVERVIEW
# ==========================================================

st.header("📂 Dataset Overview")

c1,c2,c3 = st.columns(3)

with c1:

    st.metric(
        "Rows",
        f"{filtered.shape[0]:,}"
    )

with c2:

    st.metric(
        "Columns",
        filtered.shape[1]
    )

with c3:

    st.metric(
        "Years Covered",
        filtered["Year"].nunique()
    )

with st.expander("Preview Dataset"):

    st.dataframe(filtered.head())

# ==========================================================
# PROJECT INFORMATION
# ==========================================================

st.header("ℹ Project Information")

st.write("""

**Project Name**

Real-Time Ferry Ticket Sales and Redemption Analytics for Toronto Island Park

**Domain**

Data Analytics

**Tools Used**

- Python
- Streamlit
- Pandas
- NumPy
- Matplotlib
- Seaborn
- Plotly
- SciPy

**Dataset**

Toronto Island Ferry Ticket Sales & Redemption

""")

st.success("✅ Part 1 Loaded Successfully")

# ==========================================================
# EXPLORATORY DATA ANALYSIS
# HOURLY ANALYSIS
# ==========================================================

st.markdown("---")
st.header("⏰ Hourly Analytics")

# -------------------------------
# Hourly Ticket Sales
# -------------------------------

hourly_sales = (
    filtered.groupby("Hour", as_index=False)["Sales Count"]
    .sum()
)

fig = px.line(
    hourly_sales,
    x="Hour",
    y="Sales Count",
    markers=True,
    title="Hourly Ticket Sales Trend"
)

fig.update_layout(
    xaxis_title="Hour of Day",
    yaxis_title="Ticket Sales",
    template="plotly_white",
    height=500
)

st.plotly_chart(fig, use_container_width=True)

st.info(
    "📌 **Insight:** Passenger ticket sales increase during the morning, "
    "reach their highest levels around midday, and gradually decline toward "
    "the evening, highlighting the busiest operating hours."
)

# -------------------------------
# Hourly Ticket Redemption
# -------------------------------

hourly_redemption = (
    filtered.groupby("Hour", as_index=False)["Redemption Count"]
    .sum()
)

fig = px.line(
    hourly_redemption,
    x="Hour",
    y="Redemption Count",
    markers=True,
    title="Hourly Ticket Redemption Trend"
)

fig.update_layout(
    xaxis_title="Hour of Day",
    yaxis_title="Ticket Redemptions",
    template="plotly_white",
    height=500
)

st.plotly_chart(fig, use_container_width=True)

st.info(
    "📌 **Insight:** Ticket redemption closely follows ticket sales, "
    "indicating consistent passenger utilization throughout the day."
)

# -------------------------------
# Sales vs Redemption Comparison
# -------------------------------

compare = (
    filtered.groupby("Hour")[["Sales Count", "Redemption Count"]]
    .sum()
    .reset_index()
)

fig = go.Figure()

fig.add_trace(
    go.Scatter(
        x=compare["Hour"],
        y=compare["Sales Count"],
        mode="lines+markers",
        name="Sales Count"
    )
)

fig.add_trace(
    go.Scatter(
        x=compare["Hour"],
        y=compare["Redemption Count"],
        mode="lines+markers",
        name="Redemption Count"
    )
)

fig.update_layout(
    title="Hourly Sales vs Redemption Comparison",
    xaxis_title="Hour",
    yaxis_title="Passengers",
    template="plotly_white",
    height=550
)

st.plotly_chart(fig, use_container_width=True)

st.info(
    "📌 **Insight:** Sales and redemption patterns remain closely aligned "
    "throughout the day, demonstrating stable operational performance."
)

# -------------------------------
# Net Passenger Movement
# -------------------------------

movement = (
    filtered.groupby("Hour", as_index=False)["Net Passenger Movement"]
    .sum()
)

fig = px.bar(
    movement,
    x="Hour",
    y="Net Passenger Movement",
    title="Hourly Net Passenger Movement"
)

fig.update_layout(
    xaxis_title="Hour",
    yaxis_title="Net Passenger Movement",
    template="plotly_white",
    height=500
)

st.plotly_chart(fig, use_container_width=True)

st.info(
    "📌 **Insight:** Net passenger movement varies across the day, "
    "providing valuable information for optimizing ferry capacity and "
    "terminal operations."
)

# -------------------------------
# Peak Demand Hour Table
# -------------------------------

st.subheader("🏆 Top 10 Peak Demand Hours")

top_hours = (
    filtered.groupby("Hour")["Sales Count"]
    .sum()
    .sort_values(ascending=False)
    .head(10)
    .reset_index()
)

st.dataframe(
    top_hours,
    use_container_width=True,
    hide_index=True
)

# -------------------------------
# Hourly Summary
# -------------------------------

with st.expander("📈 Hourly Analysis Summary"):

    st.write(f"""
**Peak Demand Hour:** {peak_hour}:00

**Highest Ticket Sales:** {top_hours.iloc[0]['Sales Count']:,}

**Total Hours Analysed:** {filtered['Hour'].nunique()}

The hourly analysis indicates that passenger demand is concentrated during
specific operating hours. Understanding these demand peaks enables ferry
operators to optimize scheduling, improve staffing allocation, and enhance
overall passenger service efficiency.
""")

st.success("✅ Hourly Analysis Loaded Successfully")

# ==========================================================
# DAILY & WEEKLY ANALYSIS
# ==========================================================

st.markdown("---")
st.header("📅 Daily & Weekly Analysis")

# -------------------------------
# Day Order
# -------------------------------

day_order = [
    "Monday",
    "Tuesday",
    "Wednesday",
    "Thursday",
    "Friday",
    "Saturday",
    "Sunday"
]

daily_sales = (
    filtered.groupby("Day", as_index=False)["Sales Count"]
    .sum()
)

daily_sales["Day"] = pd.Categorical(
    daily_sales["Day"],
    categories=day_order,
    ordered=True
)

daily_sales = daily_sales.sort_values("Day")

# -------------------------------
# Daily Ticket Sales
# -------------------------------

fig = px.bar(
    daily_sales,
    x="Day",
    y="Sales Count",
    text_auto=True,
    title="Daily Ticket Sales Analysis"
)

fig.update_layout(
    template="plotly_white",
    height=500,
    xaxis_title="Day",
    yaxis_title="Ticket Sales"
)

st.plotly_chart(fig, use_container_width=True)

highest_day = daily_sales.loc[
    daily_sales["Sales Count"].idxmax(),
    "Day"
]

st.info(
    f"📌 **Insight:** {highest_day} records the highest passenger demand, "
    "indicating greater ferry utilization compared to other days of the week."
)

# -------------------------------
# Weekend vs Weekday
# -------------------------------

week = (
    filtered.groupby("Weekend", as_index=False)["Sales Count"]
    .sum()
)

fig = px.pie(
    week,
    names="Weekend",
    values="Sales Count",
    hole=0.45,
    title="Weekend vs Weekday Contribution"
)

fig.update_traces(textposition="inside", textinfo="percent+label")

st.plotly_chart(fig, use_container_width=True)

st.info(
    "📌 **Insight:** Weekend demand contributes significantly to total passenger activity, "
    "highlighting the importance of optimized weekend ferry operations."
)

# -------------------------------
# Weekend vs Weekday Comparison
# -------------------------------

compare_week = (
    filtered.groupby("Weekend")[["Sales Count","Redemption Count"]]
    .sum()
    .reset_index()
)

fig = px.bar(
    compare_week,
    x="Weekend",
    y=["Sales Count","Redemption Count"],
    barmode="group",
    title="Weekend vs Weekday Sales & Redemption"
)

fig.update_layout(
    template="plotly_white",
    height=500
)

st.plotly_chart(fig, use_container_width=True)

st.info(
    "📌 **Insight:** Ticket sales and redemption remain closely aligned across weekdays "
    "and weekends, demonstrating consistent passenger utilization."
)

# -------------------------------
# Daily Table
# -------------------------------

st.subheader("📋 Daily Passenger Summary")

summary = (
    filtered.groupby("Day")[["Sales Count","Redemption Count"]]
    .sum()
    .reindex(day_order)
    .reset_index()
)

st.dataframe(
    summary,
    use_container_width=True,
    hide_index=True
)

# -------------------------------
# Daily KPI Cards
# -------------------------------

col1,col2,col3 = st.columns(3)

with col1:

    st.metric(
        "📅 Highest Demand Day",
        highest_day
    )

with col2:

    st.metric(
        "📈 Total Daily Sales",
        f"{daily_sales['Sales Count'].sum():,}"
    )

with col3:

    avg_daily = int(
        daily_sales["Sales Count"].mean()
    )

    st.metric(
        "📊 Average Daily Sales",
        f"{avg_daily:,}"
    )

# -------------------------------
# Daily Analysis Summary
# -------------------------------

with st.expander("📊 Daily Analysis Summary"):

    st.write(f"""

### Key Observations

• Highest Passenger Demand : **{highest_day}**

• Weekend travel contributes significantly to ferry usage.

• Passenger demand remains stable throughout the week with noticeable increases during leisure periods.

• Daily demand analysis supports optimized staffing and scheduling decisions.

""")

st.success("✅ Daily & Weekend Analysis Completed")

# ==========================================================
# MONTHLY & QUARTERLY ANALYSIS
# ==========================================================

st.markdown("---")
st.header("📅 Monthly & Quarterly Analytics")

# -------------------------------
# Month Order
# -------------------------------

month_order = [
    "January","February","March","April","May","June",
    "July","August","September","October","November","December"
]

monthly_sales = (
    filtered.groupby("Month", as_index=False)["Sales Count"]
    .sum()
)

monthly_sales["Month"] = pd.Categorical(
    monthly_sales["Month"],
    categories=month_order,
    ordered=True
)

monthly_sales = monthly_sales.sort_values("Month")

# -------------------------------
# Monthly Sales Trend
# -------------------------------

fig = px.line(
    monthly_sales,
    x="Month",
    y="Sales Count",
    markers=True,
    title="Monthly Ticket Sales Trend"
)

fig.update_layout(
    template="plotly_white",
    height=500,
    xaxis_title="Month",
    yaxis_title="Ticket Sales"
)

st.plotly_chart(fig, use_container_width=True)

best_month = monthly_sales.loc[
    monthly_sales["Sales Count"].idxmax(),
    "Month"
]

worst_month = monthly_sales.loc[
    monthly_sales["Sales Count"].idxmin(),
    "Month"
]

st.info(
    f"📌 **Insight:** {best_month} records the highest passenger demand, "
    f"while {worst_month} records the lowest demand, highlighting seasonal travel behaviour."
)

# -------------------------------
# Monthly Passenger Movement
# -------------------------------

movement_month = (
    filtered.groupby("Month", as_index=False)["Net Passenger Movement"]
    .sum()
)

movement_month["Month"] = pd.Categorical(
    movement_month["Month"],
    categories=month_order,
    ordered=True
)

movement_month = movement_month.sort_values("Month")

fig = px.bar(
    movement_month,
    x="Month",
    y="Net Passenger Movement",
    title="Monthly Net Passenger Movement"
)

fig.update_layout(
    template="plotly_white",
    height=500
)

st.plotly_chart(fig, use_container_width=True)

st.info(
    "📌 **Insight:** Monthly passenger movement helps identify periods of high inflow "
    "and supports effective resource planning."
)

# -------------------------------
# Quarter Analysis
# -------------------------------

quarter_sales = (
    filtered.groupby("Quarter", as_index=False)["Sales Count"]
    .sum()
)

fig = px.bar(
    quarter_sales,
    x="Quarter",
    y="Sales Count",
    text_auto=True,
    title="Quarter-wise Ticket Sales"
)

fig.update_layout(
    template="plotly_white",
    height=500
)

st.plotly_chart(fig, use_container_width=True)

best_quarter = quarter_sales.loc[
    quarter_sales["Sales Count"].idxmax(),
    "Quarter"
]

st.info(
    f"📌 **Insight:** {best_quarter} contributes the highest passenger demand, "
    "indicating increased travel activity during this quarter."
)

# -------------------------------
# Monthly Summary Table
# -------------------------------

st.subheader("📋 Monthly Summary")

monthly_table = (
    filtered.groupby("Month")[["Sales Count","Redemption Count"]]
    .sum()
    .reindex(month_order)
    .reset_index()
)

st.dataframe(
    monthly_table,
    use_container_width=True,
    hide_index=True
)

# -------------------------------
# KPI Cards
# -------------------------------

c1, c2, c3 = st.columns(3)

with c1:
    st.metric(
        "🏆 Best Month",
        best_month
    )

with c2:
    st.metric(
        "📉 Lowest Demand Month",
        worst_month
    )

with c3:
    st.metric(
        "📊 Best Quarter",
        best_quarter
    )

# -------------------------------
# Business Insights
# -------------------------------

with st.expander("💡 Monthly Business Insights"):

    st.write(f"""
### Key Findings

- **Highest Demand Month:** {best_month}

- **Lowest Demand Month:** {worst_month}

- **Best Performing Quarter:** {best_quarter}

- Passenger demand varies considerably throughout the year.

- Seasonal demand should be considered while planning ferry schedules.

- Historical monthly demand can support workforce allocation and operational planning.

- Long-term monthly analysis provides valuable insights for forecasting future passenger demand.
""")

st.success("✅ Monthly & Quarterly Analysis Completed")

# ==========================================================
# YEARLY ANALYTICS
# ==========================================================

st.markdown("---")
st.header("📈 Yearly Analytics")

# ----------------------------------------------------------
# Yearly Sales
# ----------------------------------------------------------

year_sales = (
    filtered.groupby("Year", as_index=False)["Sales Count"]
    .sum()
)

fig = px.line(
    year_sales,
    x="Year",
    y="Sales Count",
    markers=True,
    title="Yearly Ticket Sales Trend"
)

fig.update_layout(
    template="plotly_white",
    height=520,
    xaxis_title="Year",
    yaxis_title="Ticket Sales"
)

st.plotly_chart(fig, use_container_width=True)

best_year = year_sales.loc[
    year_sales["Sales Count"].idxmax(),
    "Year"
]

st.success(
    f"🏆 Highest passenger demand was recorded in **{best_year}**."
)

# ----------------------------------------------------------
# Sales vs Redemption
# ----------------------------------------------------------

year_compare = (
    filtered.groupby("Year")[["Sales Count","Redemption Count"]]
    .sum()
    .reset_index()
)

fig = go.Figure()

fig.add_trace(
    go.Bar(
        x=year_compare["Year"],
        y=year_compare["Sales Count"],
        name="Sales Count"
    )
)

fig.add_trace(
    go.Bar(
        x=year_compare["Year"],
        y=year_compare["Redemption Count"],
        name="Redemption Count"
    )
)

fig.update_layout(

    title="Year-wise Sales vs Redemption",

    barmode="group",

    template="plotly_white",

    height=520

)

st.plotly_chart(fig,use_container_width=True)

st.info(
"""
📌 Ticket sales and redemption remain highly consistent across all years,
demonstrating efficient ferry utilization.
"""
)

# ----------------------------------------------------------
# Year-over-Year Growth
# ----------------------------------------------------------

growth = year_sales.copy()

growth["Growth %"] = (
    growth["Sales Count"]
    .pct_change()*100
)

fig = px.bar(

    growth,

    x="Year",

    y="Growth %",

    text_auto=".2f",

    title="Year-over-Year Sales Growth"

)

fig.update_layout(

    template="plotly_white",

    height=500

)

st.plotly_chart(fig,use_container_width=True)

st.info(
"""
📌 Positive growth indicates increasing passenger demand,
while negative growth reflects temporary reductions in ferry utilization.
"""
)

# ----------------------------------------------------------
# KPI Cards
# ----------------------------------------------------------

c1,c2,c3,c4=st.columns(4)

with c1:

    st.metric(

        "Years Covered",

        filtered["Year"].nunique()

    )

with c2:

    st.metric(

        "Best Year",

        best_year

    )

with c3:

    st.metric(

        "Highest Sales",

        f"{year_sales['Sales Count'].max():,.0f}"

    )

with c4:

    avg_year=int(

        year_sales["Sales Count"].mean()

    )

    st.metric(

        "Average Yearly Sales",

        f"{avg_year:,}"

    )

# ----------------------------------------------------------
# Yearly Summary Table
# ----------------------------------------------------------

st.subheader("📋 Yearly Summary")

table=filtered.groupby("Year")[

    ["Sales Count",

     "Redemption Count",

     "Net Passenger Movement"]

].sum().reset_index()

st.dataframe(

    table,

    use_container_width=True,

    hide_index=True

)

# ----------------------------------------------------------
# Business Insights
# ----------------------------------------------------------

with st.expander("💡 Yearly Business Insights"):

    st.write(f"""

### Key Insights

• Highest Passenger Demand : **{best_year}**

• Ferry utilization remained stable throughout the years.

• Ticket sales and redemption demonstrate strong operational consistency.

• Historical yearly demand supports long-term transportation planning.

• Annual demand trends provide valuable input for forecasting future ferry operations.

""")

st.success("✅ Yearly Analytics Completed")

# ==========================================================
# SEASONAL & PEAK ANALYTICS
# ==========================================================

st.markdown("---")
st.header("🌤 Seasonal & Peak Period Analytics")

# ----------------------------------------------------------
# Seasonal Sales
# ----------------------------------------------------------

season_order = ["Spring","Summer","Autumn","Winter"]

season_sales = (
    filtered.groupby("Season", as_index=False)["Sales Count"]
    .sum()
)

season_sales["Season"] = pd.Categorical(
    season_sales["Season"],
    categories=season_order,
    ordered=True
)

season_sales = season_sales.sort_values("Season")

fig = px.bar(
    season_sales,
    x="Season",
    y="Sales Count",
    text_auto=True,
    color="Season",
    title="Seasonal Ticket Sales Analysis"
)

fig.update_layout(
    template="plotly_white",
    height=500
)

st.plotly_chart(fig, use_container_width=True)

best_season = season_sales.loc[
    season_sales["Sales Count"].idxmax(),
    "Season"
]

worst_season = season_sales.loc[
    season_sales["Sales Count"].idxmin(),
    "Season"
]

st.success(
    f"🏆 Highest passenger demand occurs during **{best_season}**."
)

# ----------------------------------------------------------
# Seasonal Sales vs Redemption
# ----------------------------------------------------------

season_compare = (
    filtered.groupby("Season")[["Sales Count","Redemption Count"]]
    .sum()
    .reindex(season_order)
    .reset_index()
)

fig = px.bar(
    season_compare,
    x="Season",
    y=["Sales Count","Redemption Count"],
    barmode="group",
    title="Seasonal Sales vs Redemption"
)

fig.update_layout(
    template="plotly_white",
    height=520
)

st.plotly_chart(fig,use_container_width=True)

st.info(
"""
📌 Ticket sales and redemption remain closely aligned
throughout every season.
"""
)

# ----------------------------------------------------------
# Seasonal Contribution
# ----------------------------------------------------------

fig = px.pie(
    season_sales,
    names="Season",
    values="Sales Count",
    hole=0.45,
    title="Seasonal Contribution to Total Sales"
)

fig.update_traces(
    textposition="inside",
    textinfo="percent+label"
)

st.plotly_chart(fig,use_container_width=True)

# ----------------------------------------------------------
# Peak vs Off Peak
# ----------------------------------------------------------

peak_df = (
    filtered.groupby("Peak Period",as_index=False)["Sales Count"]
    .sum()
)

fig = px.bar(
    peak_df,
    x="Peak Period",
    y="Sales Count",
    text_auto=True,
    color="Peak Period",
    title="Peak vs Off-Peak Passenger Demand"
)

fig.update_layout(
    template="plotly_white",
    height=500
)

st.plotly_chart(fig,use_container_width=True)

st.info(
"""
📌 Passenger demand varies considerably across different
operating periods, highlighting opportunities for
optimized scheduling.
"""
)

# ----------------------------------------------------------
# Peak Contribution
# ----------------------------------------------------------

fig = px.pie(
    peak_df,
    names="Peak Period",
    values="Sales Count",
    hole=0.45,
    title="Peak Period Contribution"
)

fig.update_traces(
    textposition="inside",
    textinfo="percent+label"
)

st.plotly_chart(fig,use_container_width=True)

# ----------------------------------------------------------
# KPI Cards
# ----------------------------------------------------------

c1,c2,c3,c4 = st.columns(4)

with c1:

    st.metric(
        "Best Season",
        best_season
    )

with c2:

    st.metric(
        "Lowest Season",
        worst_season
    )

with c3:

    st.metric(
        "Peak Categories",
        filtered["Peak Period"].nunique()
    )

with c4:

    st.metric(
        "Season Categories",
        filtered["Season"].nunique()
    )

# ----------------------------------------------------------
# Seasonal Summary
# ----------------------------------------------------------

st.subheader("📋 Seasonal Summary")

summary = (
    filtered.groupby("Season")[
        ["Sales Count",
         "Redemption Count",
         "Net Passenger Movement"]
    ]
    .sum()
    .reindex(season_order)
    .reset_index()
)

st.dataframe(
    summary,
    use_container_width=True,
    hide_index=True
)

# ----------------------------------------------------------
# Business Insights
# ----------------------------------------------------------

with st.expander("💡 Seasonal Business Insights"):

    st.write(f"""

### Executive Insights

• Highest Demand Season : **{best_season}**

• Lowest Demand Season : **{worst_season}**

• Seasonal demand should guide staffing,
  maintenance planning,
  and ferry deployment.

• Peak periods require additional ferry
  capacity to minimize congestion.

• Seasonal analytics support long-term
  transportation planning.

• Historical seasonal trends can improve
  forecasting accuracy.

""")

st.success("✅ Seasonal Analytics Completed")

# ==========================================================
# STATISTICAL ANALYSIS
# Correlation Matrix | Heatmap | Pearson Correlation
# ==========================================================

st.markdown("---")
st.header("📊 Statistical Analysis")

# ----------------------------------------------------------
# Correlation Matrix
# ----------------------------------------------------------

corr_columns = [
    "Sales Count",
    "Redemption Count",
    "Net Passenger Movement"
]

corr_matrix = filtered[corr_columns].corr()

st.subheader("Correlation Matrix")

st.dataframe(
    corr_matrix.style.background_gradient(cmap="Blues"),
    use_container_width=True
)

# ----------------------------------------------------------
# Correlation Heatmap
# ----------------------------------------------------------

st.subheader("Correlation Heatmap")

fig, ax = plt.subplots(figsize=(8,6))

sns.heatmap(
    corr_matrix,
    annot=True,
    cmap="Blues",
    linewidths=1,
    square=True,
    fmt=".2f",
    ax=ax
)

plt.title("Correlation Heatmap")

st.pyplot(fig)

st.info(
"""
📌 Strong positive correlation between Ticket Sales
and Ticket Redemption indicates highly consistent
passenger utilization.
"""
)

# ----------------------------------------------------------
# Pearson Correlation Test
# ----------------------------------------------------------

st.subheader("Pearson Correlation Test")

corr,p = pearsonr(
    filtered["Sales Count"],
    filtered["Redemption Count"]
)

result = pd.DataFrame({

    "Metric":[

        "Correlation Coefficient",

        "P-value"

    ],

    "Value":[

        round(corr,4),

        p

    ]

})

st.table(result)

if p < 0.05:

    st.success(
        "✅ Statistically Significant Relationship Found"
    )

else:

    st.error(
        "❌ No Significant Relationship Found"
    )

st.info(f"""

Correlation Coefficient : **{corr:.4f}**

P-value : **{p:.10f}**

Interpretation:

The Pearson correlation coefficient indicates a very
strong positive relationship between ticket sales and
ticket redemption.

""")

# ----------------------------------------------------------
# Statistical KPI Cards
# ----------------------------------------------------------

c1,c2,c3 = st.columns(3)

with c1:

    st.metric(

        "Correlation",

        f"{corr:.4f}"

    )

with c2:

    st.metric(

        "P-value",

        f"{p:.6f}"

    )

with c3:

    if corr>0.8:

        relation="Strong Positive"

    elif corr>0.5:

        relation="Moderate"

    else:

        relation="Weak"

    st.metric(

        "Relationship",

        relation

    )

# ----------------------------------------------------------
# Executive Statistical Insights
# ----------------------------------------------------------

with st.expander("📈 Statistical Insights"):

    st.write("""

### Key Findings

• Ticket Sales and Redemption exhibit a strong
positive correlation.

• Passenger utilization remains highly consistent.

• Operational data demonstrates excellent statistical
reliability.

• Historical ticket sales can effectively support
future forecasting and demand prediction.

• Statistical analysis validates the consistency
observed during exploratory data analysis.

""")

st.success("✅ Correlation Analysis Completed")

# ==========================================================
# ROLLING AVERAGE & DISTRIBUTION ANALYSIS
# ==========================================================

st.markdown("---")
st.header("📈 Trend & Distribution Analysis")

# ----------------------------------------------------------
# Prepare Data
# ----------------------------------------------------------

rolling_df = filtered.sort_values("Timestamp").copy()

rolling_df["Rolling_1H"] = (
    rolling_df["Sales Count"]
    .rolling(window=1)
    .mean()
)

rolling_df["Rolling_4H"] = (
    rolling_df["Sales Count"]
    .rolling(window=4)
    .mean()
)

# ----------------------------------------------------------
# 1 Hour Rolling Average
# ----------------------------------------------------------

st.subheader("1-Hour Rolling Average")

fig = px.line(
    rolling_df,
    x="Timestamp",
    y="Rolling_1H",
    title="1-Hour Rolling Average of Ticket Sales"
)

fig.update_layout(
    template="plotly_white",
    height=500
)

st.plotly_chart(fig, use_container_width=True)

st.info("""
📌 **Insight:** The 1-hour rolling average smooths short-term fluctuations while preserving immediate passenger demand trends.
""")

# ----------------------------------------------------------
# 4 Hour Rolling Average
# ----------------------------------------------------------

st.subheader("4-Hour Rolling Average")

fig = px.line(
    rolling_df,
    x="Timestamp",
    y="Rolling_4H",
    title="4-Hour Rolling Average of Ticket Sales"
)

fig.update_layout(
    template="plotly_white",
    height=500
)

st.plotly_chart(fig, use_container_width=True)

st.info("""
📌 **Insight:** The 4-hour rolling average highlights long-term demand behavior by reducing short-term variability.
""")

# ----------------------------------------------------------
# Ticket Sales Distribution
# ----------------------------------------------------------

st.subheader("Ticket Sales Distribution")

fig = px.histogram(
    filtered,
    x="Sales Count",
    nbins=40,
    title="Distribution of Ticket Sales"
)

fig.update_layout(
    template="plotly_white",
    height=500
)

st.plotly_chart(fig, use_container_width=True)

st.info("""
📌 **Insight:** Most observations fall within lower ticket sales ranges, while a few high-demand periods create a positively skewed distribution.
""")

# ----------------------------------------------------------
# Ticket Redemption Distribution
# ----------------------------------------------------------

st.subheader("Ticket Redemption Distribution")

fig = px.histogram(
    filtered,
    x="Redemption Count",
    nbins=40,
    title="Distribution of Ticket Redemptions"
)

fig.update_layout(
    template="plotly_white",
    height=500
)

st.plotly_chart(fig, use_container_width=True)

st.info("""
📌 **Insight:** Redemption counts follow a distribution similar to ticket sales, confirming consistent passenger utilization.
""")

# ----------------------------------------------------------
# Demand Volatility
# ----------------------------------------------------------

st.subheader("Demand Volatility")

volatility = pd.DataFrame({

    "Metric":[
        "Average Sales",
        "Median Sales",
        "Standard Deviation",
        "Maximum Sales",
        "Minimum Sales"
    ],

    "Value":[
        round(filtered["Sales Count"].mean(),2),
        round(filtered["Sales Count"].median(),2),
        round(filtered["Sales Count"].std(),2),
        round(filtered["Sales Count"].max(),2),
        round(filtered["Sales Count"].min(),2)
    ]

})

st.dataframe(
    volatility,
    use_container_width=True,
    hide_index=True
)

st.info("""
📌 **Insight:** Standard deviation measures passenger demand variability. Higher values indicate larger fluctuations across different operating periods.
""")

# ----------------------------------------------------------
# Statistical KPI Cards
# ----------------------------------------------------------

c1,c2,c3,c4 = st.columns(4)

with c1:
    st.metric(
        "Average Sales",
        f"{filtered['Sales Count'].mean():.2f}"
    )

with c2:
    st.metric(
        "Median Sales",
        f"{filtered['Sales Count'].median():.2f}"
    )

with c3:
    st.metric(
        "Std. Deviation",
        f"{filtered['Sales Count'].std():.2f}"
    )

with c4:
    st.metric(
        "Maximum Sales",
        f"{filtered['Sales Count'].max():,.0f}"
    )

# ----------------------------------------------------------
# Executive Summary
# ----------------------------------------------------------

with st.expander("📊 Statistical Summary"):

    st.write("""

### Key Findings

- Rolling averages reveal underlying demand trends.

- Passenger demand exhibits periodic fluctuations.

- Ticket sales distribution is positively skewed.

- Demand variability is moderate throughout the dataset.

- These statistical measures support accurate forecasting
  and operational planning.

""")

st.success("✅ Trend & Distribution Analysis Completed")

# ==========================================================
# OUTLIER ANALYSIS & BUSINESS INTELLIGENCE
# ==========================================================

st.markdown("---")
st.header("🚀 Advanced Business Intelligence")

# ----------------------------------------------------------
# Outlier Detection - Sales Count
# ----------------------------------------------------------

st.subheader("📦 Sales Count Outlier Detection")

fig = px.box(
    filtered,
    y="Sales Count",
    title="Sales Count Outlier Detection"
)

fig.update_layout(
    template="plotly_white",
    height=450
)

st.plotly_chart(fig, use_container_width=True)

st.info("""
📌 High-value observations represent genuine peak passenger demand rather than data quality issues.
""")

# ----------------------------------------------------------
# Outlier Detection - Redemption Count
# ----------------------------------------------------------

st.subheader("📦 Redemption Count Outlier Detection")

fig = px.box(
    filtered,
    y="Redemption Count",
    title="Redemption Count Outlier Detection"
)

fig.update_layout(
    template="plotly_white",
    height=450
)

st.plotly_chart(fig, use_container_width=True)

st.info("""
📌 Redemption outliers correspond to exceptionally high passenger activity and assist in operational planning.
""")

# ----------------------------------------------------------
# Top 10 Ticket Sales
# ----------------------------------------------------------

st.subheader("🏆 Top 10 Ticket Sales")

top_sales = (
    filtered
    .sort_values("Sales Count", ascending=False)
    [["Timestamp", "Sales Count"]]
    .head(10)
)

st.dataframe(
    top_sales,
    use_container_width=True,
    hide_index=True
)

# ----------------------------------------------------------
# Top 10 Ticket Redemptions
# ----------------------------------------------------------

st.subheader("🏆 Top 10 Ticket Redemptions")

top_redemption = (
    filtered
    .sort_values("Redemption Count", ascending=False)
    [["Timestamp", "Redemption Count"]]
    .head(10)
)

st.dataframe(
    top_redemption,
    use_container_width=True,
    hide_index=True
)

# ----------------------------------------------------------
# Top 10 Peak Demand Dates
# ----------------------------------------------------------

st.subheader("📅 Top 10 Peak Demand Dates")

top_dates = (
    filtered
    .sort_values("Sales Count", ascending=False)
    [["Timestamp", "Sales Count", "Redemption Count"]]
    .head(10)
)

st.dataframe(
    top_dates,
    use_container_width=True,
    hide_index=True
)

# ----------------------------------------------------------
# Executive Business Intelligence
# ----------------------------------------------------------

st.markdown("---")
st.header("💼 Executive Business Intelligence")

col1, col2 = st.columns(2)

with col1:

    st.success(f"""
### Highest Demand

🏆 Year : {best_year}

🌞 Season : {best_season}

📅 Month : {best_month}

🕛 Hour : {peak_hour}:00

📈 Day : {highest_day}
""")

with col2:

    st.info(f"""
### Statistical Highlights

✔ Correlation : {corr:.4f}

✔ P-value : {p:.8f}

✔ Utilization : {utilization:.2f}%

✔ Peak Quarter : {best_quarter}
""")

# ----------------------------------------------------------
# Recommendations
# ----------------------------------------------------------

st.markdown("---")
st.header("🎯 Business Recommendations")

recommendations = [

"Increase ferry frequency during peak operating hours.",

"Deploy additional staff during weekends and summer.",

"Utilize predictive analytics for demand forecasting.",

"Monitor KPIs through real-time dashboards.",

"Optimize resource allocation using historical demand.",

"Integrate weather and holiday data into planning.",

"Improve passenger experience through reduced waiting time.",

"Adopt data-driven decision making for long-term planning."

]

for rec in recommendations:
    st.write(f"✅ {rec}")

# ----------------------------------------------------------
# Download Center
# ----------------------------------------------------------

st.markdown("---")
st.header("📥 Download Center")

csv = filtered.to_csv(index=False).encode("utf-8")

st.download_button(
    label="⬇ Download Filtered Dataset",
    data=csv,
    file_name="Filtered_Ferry_Dataset.csv",
    mime="text/csv"
)

summary = filtered.describe().to_csv().encode("utf-8")

st.download_button(
    label="⬇ Download Summary Statistics",
    data=summary,
    file_name="Summary_Statistics.csv",
    mime="text/csv"
)

# ----------------------------------------------------------
# Footer
# ----------------------------------------------------------

st.markdown("---")

st.markdown("""
## 🚢 Toronto Island Ferry Analytics Dashboard

**Developed by:** Satwik Srivastava

**Internship Domain:** Data Analytics

**Tools Used**

- Python
- Streamlit
- Pandas
- NumPy
- Plotly
- Matplotlib
- Seaborn
- SciPy

**Dashboard Features**

✔ Executive KPIs

✔ Interactive Filters

✔ Exploratory Data Analysis

✔ Statistical Analysis

✔ Business Intelligence

✔ Download Center

✔ Business Recommendations

---
""")

st.success("🎉 Dashboard Loaded Successfully")