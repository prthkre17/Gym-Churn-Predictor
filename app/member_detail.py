import streamlit as st
from data_loader import load_ai_engines
from config import FEATURE_TRANSLATOR, ACTION_TRANSLATOR

def render_member_detail(display_df, df_results, view_option):
    if not display_df.empty:
        selected_name = st.selectbox("Select Member to generate snapshot", display_df['Name'].tolist())

        if selected_name:
            person_data = df_results[df_results['Name'] == selected_name].iloc[0]
            math_columns = df_results.drop(columns=[
                'Name', 'Email', 'Phone_Number', 'Risk_ROS', 'Risk_SMOTE', 'Risk_ADASYN', 'Consensus_Risk'
            ]).columns
            person_math = person_data[math_columns].values.reshape(1, -1)

            scaler, models, explainers = load_ai_engines()
            person_scaled = scaler.transform(person_math)

            st.markdown(f"### 👤 Profile Snapshot: **{selected_name}**")

            snap1, snap2, snap3, snap4 = st.columns(4)
            snap1.metric("Age", int(person_data['Age']))
            snap2.metric("Contract Length", f"{int(person_data['Contract_period'])} Months")
            snap3.metric("Gym Lifetime", f"{int(person_data['Lifetime'])} Months")

            att_drop = person_data['Attendance_Drop']
            trend_label = "Slacking Off" if att_drop > 0 else "Highly Consistent"
            snap4.metric("Recent Routine", trend_label, f"{-att_drop:.2f} diff vs avg")
            st.markdown("<br>", unsafe_allow_html=True)

            tab1, tab2, tab3 = st.tabs(["ROS Assessment", "SMOTE Assessment", "ADASYN Assessment"])

            def render_beautiful_shap(model_name):
                explainer = explainers[model_name]
                shap_values = explainer(person_scaled)
                shap_values.feature_names = math_columns.tolist()

                vals = shap_values[0].values
                feature_impacts = list(zip(math_columns.tolist(), vals))
                feature_impacts.sort(key=lambda x: x[1], reverse=True)

                top_reasons = [feat for feat, impact in feature_impacts if impact > 0][:3]

                if top_reasons and view_option != "Loyal Members ⭐":
                    col1, col2 = st.columns([1, 1])
                    with col1:
                        st.markdown("#### 📛 Top 3 Reasons for Churning:")
                        for feat in top_reasons:
                            clean_reason = FEATURE_TRANSLATOR.get(feat, feat)
                            st.markdown(f"🚩 **{clean_reason}**")
                    with col2:
                        st.markdown("#### ☑️Action Plan:")
                        primary_reason = top_reasons[0]
                        suggested_action = ACTION_TRANSLATOR.get(
                            primary_reason,
                            "Give them a quick check-in call to see how their fitness journey is going."
                        )
                        st.info(suggested_action)

                elif view_option == "Loyal Members ⭐":
                    st.success(f"🏆 **VIP STATUS:** {selected_name} is highly consistent.")
                    st.info("💡 **Upsell Opportunity:** Offer them an advanced Personal Training package or ask for a referral!")

                else:
                    st.success(f"✅ {selected_name} appears stable according to this specific model.")

            with tab1:
                render_beautiful_shap('ROS')
            with tab2:
                render_beautiful_shap('SMOTE')
            with tab3:
                render_beautiful_shap('ADASYN')

    else:
        st.info("No members match your current filter settings.")
