# 🏋️‍♂️ GymSense

## Project Overview
Customer retention is one of the biggest challenges in the fitness industry. 
This project provides a robust, end-to-end Machine Learning pipeline designed to predict gym member churn. 
By analyzing behavioral data, contract types, and attendance history, the model accurately identifies high-risk members, allowing gym management to take proactive retention measures.

## Key Highlights
* **Advanced Feature Engineering:** Engineered a highly predictive `Attendance_Drop` metric (comparing lifetime visit frequency to current month frequency), which proved to be the single strongest indicator of flight risk.

* **Tackling Class Imbalance:** Implemented and compared multiple data sampling techniques (**ROS, SMOTE, and ADASYN**) to ensure the AI correctly identifies minority churners without biasing towards majority active members.

* **High-Performance Modeling:** Trained an **XGBoost Classifier** achieving ~98% ROC-AUC.

* **Executive Dashboards (Explainable AI):** Utilized **SHAP** (SHapley Additive exPlanations) to translate complex AI math into intuitive percentage-based impact charts for business stakeholders.

* **Interactive Web App:** Includes a fully modular Python application architecture ready for deployment.

---

## 📂 Repository Architecture

```text
Gym-Churn-Predictor/
│
├── app/                        # Production Application Scripts & Models
│   ├── app.py                  # Main application entry point
│   ├── config.py               # Application configurations
│   ├── data_loader.py          # Data ingestion and caching
│   ├── member_detail.py        # Individual member risk profiling
│   ├── sidebar.py              # UI Navigation logic
│   ├── styles.py               # Custom UI styling
│   ├── views.py                # Dashboard routing
│   ├── analytics.py            # SHAP & business logic
│   ├── scaler.pkl              # Fitted StandardScaler
│   ├── xgb_ros.pkl             # Trained XGBoost (Random Oversampling)
│   ├── xgb_smote.pkl           # Trained XGBoost (SMOTE)
│   └── xgb_adasyn.pkl          # Trained XGBoost (ADASYN)
│
├── data/                       # Datasets
│   ├── gym_churn_us.csv        # Raw initial dataset
│   └── gym_churn_featured.csv  # Cleaned dataset with engineered features
│
├── notebooks/                  # Experimental Jupyter Notebooks
│   ├── Data_Preparation.ipynb  # EDA, Data Cleaning, and Feature Engineering
│   └── Data_Training.ipynb     # Model building, Pipeline testing, and SHAP Visuals
│
├── requirements.txt            # Python dependencies
└── README.md                   # Project documentation