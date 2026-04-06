import streamlit as st
import pandas as pd
import numpy as np
import joblib
import shap

@st.cache_resource
def load_ai_engines():
    scaler = joblib.load('scaler.pkl')
    models = {
        'ROS':   joblib.load('xgb_ros.pkl'),
        'SMOTE': joblib.load('xgb_smote.pkl'),
        'ADASYN':joblib.load('xgb_adasyn.pkl')
    }
    explainers = {
        'ROS':   shap.TreeExplainer(models['ROS']),
        'SMOTE': shap.TreeExplainer(models['SMOTE']),
        'ADASYN':shap.TreeExplainer(models['ADASYN'])
    }
    return scaler, models, explainers

@st.cache_data
def load_and_predict():
    df = pd.read_csv('../data/gym_churn_featured.csv')
    df_live = df.drop(columns=['Churn'], errors='ignore')
    X_math = df_live.drop(columns=['Name', 'Email', 'Phone_Number'])

    scaler, models, _ = load_ai_engines()
    X_scaled = scaler.transform(X_math)

    df_live['Risk_ROS']   = models['ROS'].predict(X_scaled)
    df_live['Risk_SMOTE'] = models['SMOTE'].predict(X_scaled)
    df_live['Risk_ADASYN']= models['ADASYN'].predict(X_scaled)

    df_live['Consensus_Risk'] = np.where(
        (df_live['Risk_ROS'] == 1) & (df_live['Risk_SMOTE'] == 1) & (df_live['Risk_ADASYN'] == 1),
        "🚨 GUARANTEED CHURN", "Safe / Uncertain"
    )
    return df_live
