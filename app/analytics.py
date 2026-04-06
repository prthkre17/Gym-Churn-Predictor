import streamlit as st
import numpy as np
import pandas as pd
import altair as alt
from data_loader import load_ai_engines
from config import FEATURE_TRANSLATOR

def render_bulk_analytics(display_df, df_results, view_option):
    if not display_df.empty and view_option != "Loyal Members ⭐":
        st.write("Understanding the macro-trends for this specific filtered group.")

        math_columns = df_results.drop(columns=[
            'Name', 'Email', 'Phone_Number', 'Risk_ROS', 'Risk_SMOTE', 'Risk_ADASYN', 'Consensus_Risk'
        ]).columns

        bulk_math = display_df[math_columns]
        scaler, models, explainers = load_ai_engines()
        bulk_scaled = scaler.transform(bulk_math)

        explainer = explainers['ROS']
        shap_values_bulk = explainer(bulk_scaled)

        mean_shap = np.abs(
            shap_values_bulk[0].values if isinstance(shap_values_bulk, list) else shap_values_bulk.values
        ).mean(axis=0)

        total_impact = mean_shap.sum()
        impact_percentage = (mean_shap / total_impact) if total_impact > 0 else 0

        macro_trends = pd.DataFrame({
            'Feature': math_columns,
            'Impact': mean_shap,
            'Impact_Percentage': impact_percentage
        })

        macro_trends['Feature'] = macro_trends['Feature'].map(lambda x: FEATURE_TRANSLATOR.get(x, x))
        macro_trends = macro_trends.sort_values(by='Impact', ascending=False).head(5)

        col_chart, col_text = st.columns([2, 1])

        with col_chart:
            st.subheader("Top 5 Macro Churn Drivers")
            horizontal_chart = alt.Chart(macro_trends).mark_bar(color="#ff4b4b").encode(
                x=alt.X('Impact_Percentage:Q', title='Relative Impact (%)', axis=alt.Axis(format='%')),
                y=alt.Y('Feature:N', sort='-x', title=''),
                tooltip=[
                    alt.Tooltip('Feature:N', title='Feature'),
                    alt.Tooltip('Impact_Percentage:Q', title='Impact Contribution', format='.1%')
                ]
            ).properties(height=300)
            st.altair_chart(horizontal_chart, use_container_width=True)

        with col_text:
            st.subheader("💡 Strategic Action")
            top_macro_reason = macro_trends.iloc[0]['Feature']
            st.info(f"For this specific segment of **{len(display_df)} members**, the #1 overarching issue is **{top_macro_reason}**.")
            st.success("If you are launching a mass marketing or email campaign today, target this specific pain point!")

    elif view_option == "Loyal Members ⭐":
        st.info("Bulk analytics are currently optimized to identify high-risk churn drivers.")
