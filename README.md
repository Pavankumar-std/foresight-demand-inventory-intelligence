<<<<<<< HEAD
# FORESIGHT — Demand & Inventory Intelligence

## Project Overview

FORESIGHT is a demand forecasting and inventory intelligence project developed for **NorthBay Living** to support better SKU-level demand planning and inventory decisions.

The project uses historical sales, calendar, promotion, SKU, and inventory data to forecast product demand for the next four weeks and identify inventory conditions such as potential stockouts, overstock, and products that require monitoring.

The final solution includes:

- Data quality and preprocessing
- Exploratory data analysis
- Weekly demand forecasting
- Seasonal-naive baseline comparison
- Machine learning forecasting
- Rolling-origin validation
- Inventory risk scoring
- Recommended inventory actions
- Interactive Streamlit dashboard
- FastAPI scoring service

---

## Business Problem

Inventory planning becomes difficult when demand changes across products, weeks, seasons, and promotional periods.

The main objective of this project was to build a practical analytics solution that can help answer questions such as:

- How much demand can be expected for each SKU?
- Which products may face a stockout?
- Which products may have excess inventory?
- Which SKUs should be reordered?
- Which products should be monitored?
- Which products may require markdown or clearance action?
- How can forecast and inventory information be presented in a simple planning dashboard?

The project focuses on a **4-week forecasting horizon**.

---

## Project Objectives

The main objectives of FORESIGHT are:

1. Build a reproducible data preparation and quality pipeline.
2. Analyze historical SKU-level sales patterns.
3. Identify seasonal, weekly, and promotional demand patterns.
4. Establish a seasonal-naive forecasting baseline.
5. Build a machine learning demand forecasting model.
6. Validate the forecasting approach using time-based validation.
7. Calculate inventory risk using forecast demand and inventory information.
8. Assign practical recommended actions to each SKU.
9. Build an interactive dashboard for inventory planning.
10. Expose inventory risk results through a REST API.

---

# Project Workflow

```text
Raw Data
   |
   v
Data Quality & Cleaning
   |
   v
Exploratory Data Analysis
   |
   v
Feature Engineering
   |
   v
Seasonal-Naive Baseline
   |
   v
Machine Learning Forecast
   |
   v
4-Week Demand Forecast
   |
   v
Inventory Risk Scoring
   |
   +----------------------+
   |                      |
   v                      v
Streamlit Dashboard    FastAPI Service




Project Structure
foresight/
│
├── app/
│   └── app.py
│
├── service/
│   └── main.py
│
├── data/
│   ├── raw/
│   └── processed/
│
├── notebooks/
│   ├── 00_dataset_inventory.ipynb
│   ├── 01_data_quality.ipynb
│   ├── 02_eda_insights.ipynb
│   └── 03_forecasting.ipynb
│
├── reports/
│
├── README.md
└── requirements.txt



Technologies Used
Programming
Python
Data Analysis
Pandas
NumPy
Visualization
Plotly
Matplotlib
Machine Learning
Scikit-learn
HistGradientBoostingRegressor
Dashboard
Streamlit
API
FastAPI
Uvicorn
Development
Jupyter Notebook
Visual Studio Code
Git / GitHub



Running the FastAPI Service

From the project root:

python -m uvicorn service.main:app --reload

API:

http://127.0.0.1:8000

Swagger documentation:

http://127.0.0.1:8000/docs
=======
# foresight-demand-inventory-intelligence
>>>>>>> 199309f3011794ca588e57797b1a6ba1195e2d31
