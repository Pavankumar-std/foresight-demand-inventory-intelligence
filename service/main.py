from fastapi import FastAPI
from pathlib import Path
import pandas as pd


# =========================================================
# APP CONFIGURATION
# =========================================================

app = FastAPI(
    title="FORESIGHT Inventory Risk API",
    description="Demand and inventory risk scoring service",
    version="1.0.0"
)


# =========================================================
# DATA PATH
# =========================================================

BASE_PATH = Path(__file__).resolve().parent.parent

DATA_PATH = (
    BASE_PATH
    / "data"
    / "processed"
    / "inventory_risk_scores.csv"
)


# =========================================================
# LOAD DATA
# =========================================================

risk_data = pd.read_csv(DATA_PATH)


# =========================================================
# ROOT ENDPOINT
# =========================================================

@app.get("/")
def home():

    return {
        "project": "FORESIGHT",
        "service": "Inventory Risk Scoring API",
        "status": "running",
        "records": len(risk_data)
    }


# =========================================================
# ALL RISK SCORES
# =========================================================

@app.get("/risk")
def get_all_risks():

    return risk_data.to_dict(
        orient="records"
    )


# =========================================================
# SINGLE SKU
# =========================================================

@app.get("/risk/{sku}")
def get_sku_risk(sku: str):

    result = risk_data[
        risk_data["SKU_Standard"].str.upper()
        == sku.upper()
    ]

    if result.empty:

        return {
            "error": f"SKU {sku} not found"
        }

    return result.iloc[0].to_dict()


# =========================================================
# SUMMARY
# =========================================================

@app.get("/summary")
def get_summary():

    return {

        "total_skus":
            int(len(risk_data)),

        "stockout_risk":
            int(risk_data["Stockout_Risk"].sum()),

        "overstock_risk":
            int(risk_data["Overstock_Risk"].sum()),

        "healthy":
            int(
                (
                    risk_data["Recommended_Action"]
                    == "Healthy"
                ).sum()
            ),

        "watch_volatile":
            int(
                (
                    risk_data["Recommended_Action"]
                    == "Watch / Volatile"
                ).sum()
            ),

        "reorder_now":
            int(
                (
                    risk_data["Recommended_Action"]
                    == "Reorder Now"
                ).sum()
            ),

        "markdown_clear":
            int(
                (
                    risk_data["Recommended_Action"]
                    == "Markdown / Clear"
                ).sum()
            ),

        "total_four_week_forecast":
            round(
                risk_data[
                    "Forecast_4W_Units"
                ].sum(),
                2
            )
    }