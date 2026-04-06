import streamlit as st
from config import MONTHLY_FEE

def get_display_df(view_option, filtered_df):
    if view_option == "High Risk Members🚨":
        return filtered_df[filtered_df['Consensus_Risk'] == "🚨 GUARANTEED CHURN"]
    elif view_option == "Loyal Members ⭐":
        return filtered_df[
            (filtered_df['Consensus_Risk'] == "Safe / Uncertain") &
            (filtered_df['Lifetime'] > 5) &
            (filtered_df['Attendance_Drop'] < 0)
        ]
    elif view_option == "📊 ROS + XGBoost":
        return filtered_df[filtered_df['Risk_ROS'] == 1]
    elif view_option == "📊 SMOTE + XGBoost":
        return filtered_df[filtered_df['Risk_SMOTE'] == 1]
    elif view_option == "📊 ADASYN + XGBoost":
        return filtered_df[filtered_df['Risk_ADASYN'] == 1]
    return filtered_df

def render_view_header(view_option, display_df):
    if view_option == "High Risk Members🚨":
        st.title("High Risk Members🚨")
        st.markdown("Flagged by **ALL THREE** AI models. Immediate intervention required.")
        rev_at_risk = len(display_df) * MONTHLY_FEE
        col1, col2 = st.columns(2)
        col1.metric(label="Total Members at Risk", value=len(display_df))
        col2.metric(label="Monthly Revenue at Risk", value=f"₹{rev_at_risk:,}", delta="High Risk", delta_color="inverse")

    elif view_option == "Loyal Members ⭐":
        st.title("Loyal Members ⭐")
        st.markdown("These members show ironclad consistency. Excellent targets for personal training upsells or referral requests.")
        st.metric(label="Total Highly Loyal Members", value=len(display_df), delta="Highly Stable", delta_color="normal")

    elif view_option == "📊 ROS + XGBoost":
        st.title("📊 ROS + XGBoost")
        st.metric(label="Total Members", value=len(display_df))

    elif view_option == "📊 SMOTE + XGBoost":
        st.title("📊 SMOTE + XGBoost")
        st.metric(label="Total Members", value=len(display_df))

    elif view_option == "📊 ADASYN + XGBoost":
        st.title("📊 ADASYN + XGBoost")
        st.metric(label="Total Members", value=len(display_df))

def render_member_table(display_df):
    manager_view_cols = ['Name', 'Phone_Number', 'Age', 'Lifetime', 'Contract_period', 'Attendance_Drop']

    if not display_df.empty:
        display_table = display_df[manager_view_cols].copy()

        def clean_phone(x):
            x = str(x).strip()
            if x.lower() in ['nan', 'none', 'no number provided', 'null', '']:
                return "-"
            if x.startswith("+91"):
                return x[3:].strip()
            return x

        display_table['Phone_Number'] = display_table['Phone_Number'].apply(clean_phone)

        st.markdown(
            "<div style='font-family: \"Roboto Condensed\", sans-serif; font-size: 0.95rem; color: #a0aab8; margin-bottom: 8px;'>"
            "<strong>📊 Attendance Drop:</strong> "
            "<span style='color:#ff4b4b; font-weight:600;'>Positive = Slacking Off (Risk)</span> | "
            "<span style='color:#00cc96; font-weight:600;'>Negative = Going More Often (Improving)</span>"
            "</div>", unsafe_allow_html=True
        )

        def color_attendance(val):
            try:
                if float(val) > 0.05:
                    return 'color: #ff4b4b; font-weight: 700;'
                elif float(val) < -0.05:
                    return 'color: #00cc96; font-weight: 700;'
                return 'color: #f0f2f6;'
            except:
                return ''

        th_props = [
            ('font-family', 'Montserrat, sans-serif'),
            ('font-size', '14px'),
            ('font-weight', '800'),
            ('color', '#ffffff')
        ]

        styled_df = display_table.style.map(color_attendance, subset=['Attendance_Drop']).set_table_styles([
            dict(selector="th", props=th_props)
        ])

        st.dataframe(
            styled_df,
            use_container_width=True,
            hide_index=True,
            column_config={
                "Name":            st.column_config.TextColumn("Member Name", width="medium"),
                "Phone_Number":    st.column_config.TextColumn("Contact Info"),
                "Age":             st.column_config.NumberColumn("Age", format="%d yrs"),
                "Lifetime":        st.column_config.NumberColumn("Gym Lifetime", format="%d Months"),
                "Contract_period": st.column_config.NumberColumn("Contract Length", format="%d Months"),
                "Attendance_Drop": st.column_config.NumberColumn("Attendance Drop", format="%.2f")
            }
        )
    else:
        st.dataframe(display_df[manager_view_cols], use_container_width=True, hide_index=True)
