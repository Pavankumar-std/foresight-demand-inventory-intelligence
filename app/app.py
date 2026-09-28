import streamlit as st
import pandas as pd
import plotly.express as px
from pathlib import Path


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="FORESIGHT | Demand & Inventory Intelligence",
    page_icon="📊",
    layout="wide"
)


# ============================================================
# PROJECT PATHS
# ============================================================

BASE_PATH = Path(__file__).resolve().parent.parent
PROCESSED_PATH = BASE_PATH / "data" / "processed"


# ============================================================
# LOAD DATA
# ============================================================

@st.cache_data
def load_data():

    forecast = pd.read_csv(
        PROCESSED_PATH / "future_weekly_forecast.csv"
    )

    risk = pd.read_csv(
        PROCESSED_PATH / "inventory_risk_scores.csv"
    )

    # Convert forecast date
    forecast["Date"] = pd.to_datetime(
        forecast["Date"]
    )

    # Convert inventory snapshot date if available
    if "Snapshot_Date" in risk.columns:
        risk["Snapshot_Date"] = pd.to_datetime(
            risk["Snapshot_Date"]
        )

    return forecast, risk


# ============================================================
# LOAD DATA WITH ERROR HANDLING
# ============================================================

try:

    forecast, risk = load_data()

except Exception as e:

    st.error(
        "Unable to load project data. "
        "Please check that the processed CSV files exist."
    )

    st.code(str(e))

    st.stop()


# ============================================================
# TITLE
# ============================================================

st.title("📊 FORESIGHT")

st.subheader(
    "Demand & Inventory Intelligence Dashboard"
)

st.caption(
    "NorthBay Living | Weekly Demand Forecasting & Inventory Risk Planning"
)


# ============================================================
# SIDEBAR
# ============================================================

st.sidebar.header("🎛️ Dashboard Filters")


# SKU filter
sku_list = sorted(
    risk["SKU_Standard"]
    .dropna()
    .unique()
)

selected_sku = st.sidebar.selectbox(
    "Select SKU",
    ["All SKUs"] + sku_list
)


# Action filter
action_list = sorted(
    risk["Recommended_Action"]
    .dropna()
    .unique()
)

selected_action = st.sidebar.multiselect(
    "Recommended Action",
    action_list,
    default=action_list
)


# ============================================================
# FILTER DATA
# ============================================================

filtered_risk = risk[
    risk["Recommended_Action"].isin(
        selected_action
    )
].copy()


if selected_sku != "All SKUs":

    filtered_risk = filtered_risk[
        filtered_risk["SKU_Standard"]
        == selected_sku
    ]

    filtered_forecast = forecast[
        forecast["SKU_Standard"]
        == selected_sku
    ].copy()

else:

    filtered_forecast = forecast.copy()


# ============================================================
# KPI CALCULATIONS
# ============================================================

total_skus = risk[
    "SKU_Standard"
].nunique()


stockout_count = int(
    risk["Stockout_Risk"].sum()
)


overstock_count = int(
    risk["Overstock_Risk"].sum()
)


total_forecast = risk[
    "Forecast_4W_Units"
].sum()


# ============================================================
# KPI SECTION
# ============================================================

st.divider()

col1, col2, col3, col4 = st.columns(4)


with col1:

    st.metric(
        "Forecast SKUs",
        total_skus
    )


with col2:

    st.metric(
        "4-Week Demand",
        f"{total_forecast:,.0f}"
    )


with col3:

    st.metric(
        "Stockout Risk",
        stockout_count
    )


with col4:

    st.metric(
        "Overstock Risk",
        overstock_count
    )


st.divider()


# ============================================================
# SELECTED SKU DETAILS
# ============================================================

if selected_sku != "All SKUs":

    st.subheader(
        f"🔎 SKU Details — {selected_sku}"
    )

    selected_row = risk[
        risk["SKU_Standard"]
        == selected_sku
    ]

    if not selected_row.empty:

        row = selected_row.iloc[0]

        c1, c2, c3, c4, c5 = st.columns(5)


        with c1:

            st.metric(
                "Current Stock",
                f"{row['Current_Stock']:.0f}"
            )


        with c2:

            st.metric(
                "On Order",
                f"{row['On_Order']:.0f}"
            )


        with c3:

            st.metric(
                "4W Forecast",
                f"{row['Forecast_4W_Units']:.1f}"
            )


        with c4:

            st.metric(
                "Lead Time",
                f"{row['Lead_Time_Days']:.0f} days"
            )


        with c5:

            st.metric(
                "Recommended Action",
                row["Recommended_Action"]
            )


    st.divider()


# ============================================================
# WEEKLY FORECAST CHART
# ============================================================

st.subheader(
    "📈 Weekly Demand Forecast"
)


forecast_chart = (
    filtered_forecast
    .groupby(
        "Date",
        as_index=False
    )["Forecast_Units"]
    .sum()
)


if not forecast_chart.empty:

    fig_forecast = px.line(
        forecast_chart,
        x="Date",
        y="Forecast_Units",
        markers=True,
        title="Forecasted Weekly Demand"
    )

    fig_forecast.update_layout(
        xaxis_title="Forecast Week",
        yaxis_title="Forecast Units"
    )

    st.plotly_chart(
        fig_forecast,
        use_container_width=True
    )

else:

    st.info(
        "No forecast data available for the selected filters."
    )


# ============================================================
# RISK DISTRIBUTION
# ============================================================

st.subheader(
    "⚠️ Inventory Risk & Recommended Actions"
)


action_summary = (
    filtered_risk[
        "Recommended_Action"
    ]
    .value_counts()
    .reset_index()
)


action_summary.columns = [
    "Recommended_Action",
    "SKU_Count"
]


if not action_summary.empty:

    fig_action = px.bar(
        action_summary,
        x="Recommended_Action",
        y="SKU_Count",
        text="SKU_Count",
        title="SKU Count by Recommended Action"
    )

    fig_action.update_layout(
        xaxis_title="Recommended Action",
        yaxis_title="Number of SKUs"
    )

    st.plotly_chart(
        fig_action,
        use_container_width=True
    )

else:

    st.info(
        "No risk data available for the selected filters."
    )


# ============================================================
# INVENTORY RISK TABLE
# ============================================================

st.subheader(
    "📋 Inventory Risk Details"
)


display_columns = [

    "SKU_Standard",

    "Current_Stock",

    "On_Order",

    "Forecast_4W_Units",

    "Lead_Time_Days",

    "Safety_Stock",

    "Stock_Coverage_Weeks",

    "Stockout_Risk",

    "Overstock_Risk",

    "Recommended_Action"

]


available_columns = [

    column

    for column in display_columns

    if column in filtered_risk.columns

]


display_data = filtered_risk[
    available_columns
].copy()


# Round numerical values

if "Forecast_4W_Units" in display_data.columns:

    display_data[
        "Forecast_4W_Units"
    ] = display_data[
        "Forecast_4W_Units"
    ].round(2)


if "Stock_Coverage_Weeks" in display_data.columns:

    display_data[
        "Stock_Coverage_Weeks"
    ] = display_data[
        "Stock_Coverage_Weeks"
    ].round(2)


# Show table

st.dataframe(
    display_data,
    use_container_width=True,
    hide_index=True
)


# ============================================================
# DOWNLOAD SECTION
# ============================================================

st.subheader(
    "⬇️ Export Risk Results"
)


csv_data = filtered_risk.to_csv(
    index=False
).encode("utf-8")


st.download_button(
    label="Download Risk Scores CSV",
    data=csv_data,
    file_name="inventory_risk_scores_filtered.csv",
    mime="text/csv"
)


# ============================================================
# PROJECT INFORMATION
# ============================================================

st.divider()

st.subheader(
    "ℹ️ About FORESIGHT"
)

st.write(
    """
    **FORESIGHT** is a demand and inventory intelligence
    solution developed for NorthBay Living.

    The system combines:

    • Historical sales analysis  
    • Weekly demand forecasting  
    • Seasonal-naive baseline comparison  
    • Machine-learning forecasting  
    • Inventory risk scoring  
    • Stockout detection  
    • Overstock detection  
    • Recommended inventory actions  

    Forecast horizon: **4 weeks**

    Forecasting model: **HistGradientBoostingRegressor**

    Risk actions:

    • Reorder Now  
    • Markdown / Clear  
    • Watch / Volatile  
    • Healthy
    """
)


# ============================================================
# FOOTER
# ============================================================

st.divider()

st.caption(
    "FORESIGHT — Demand & Inventory Intelligence | "
    "NorthBay Living | "
    "Forecast horizon: 4 weeks"
)