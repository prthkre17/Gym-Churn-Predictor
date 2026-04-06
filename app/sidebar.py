import streamlit as st

def render_sidebar(df_results):
    st.sidebar.header("⚙️ Dashboard Controls")
    view_option = st.sidebar.selectbox(
        "Select CRM View:",
        ["High Risk Members🚨", "Loyal Members ⭐", "📊 ROS + XGBoost", "📊 SMOTE + XGBoost", "📊 ADASYN + XGBoost"]
    )

    st.sidebar.markdown("---")
    st.sidebar.header("🔍 Filter Demographics")

    min_age, max_age = int(df_results['Age'].min()), int(df_results['Age'].max())
    st.sidebar.caption(f"ℹ️ Valid age range: **{min_age} to {max_age}** years")

    age_col1, age_col2 = st.sidebar.columns(2)
    start_age = age_col1.number_input("Min Age", min_value=min_age, max_value=max_age, value=min_age, help=f"Lowest age allowed is {min_age}")
    end_age   = age_col2.number_input("Max Age", min_value=min_age, max_value=max_age, value=max_age, help=f"Highest age allowed is {max_age}")
    selected_age = (start_age, end_age)

    st.sidebar.markdown("<hr style='border: 1px dashed rgba(255,255,255,0.1); margin: 15px 0;'>", unsafe_allow_html=True)
    group_class_filter = st.sidebar.radio("Attends Group Classes?", ["All", "Yes", "No"])

    st.sidebar.markdown("<hr style='border: 1px dashed rgba(255,255,255,0.1); margin: 15px 0;'>", unsafe_allow_html=True)
    contract_filter = st.sidebar.selectbox("Contract Period (Months)", ["All", 1, 6, 12])

    st.sidebar.markdown("---")
    st.sidebar.header("📍 Location & Partnerships")

    location_filter = st.sidebar.radio("Lives/Works Near Gym?", ["All", "Yes (Near)", "No (Far)"])

    st.sidebar.markdown("<hr style='border: 1px dashed rgba(255,255,255,0.1); margin: 15px 0;'>", unsafe_allow_html=True)
    partner_filter = st.sidebar.radio("Corporate Partner Member?", ["All", "Yes", "No"])

    st.sidebar.markdown("<hr style='border: 1px dashed rgba(255,255,255,0.1); margin: 15px 0;'>", unsafe_allow_html=True)
    promo_friend_filter = st.sidebar.radio("Joined via Friend Referral?", ["All", "Yes", "No"])

    filtered_df = df_results[
        (df_results['Age'] >= selected_age[0]) & (df_results['Age'] <= selected_age[1])
    ]

    if group_class_filter == "Yes":
        filtered_df = filtered_df[filtered_df['Group_visits'] == 1]
    elif group_class_filter == "No":
        filtered_df = filtered_df[filtered_df['Group_visits'] == 0]

    if contract_filter != "All":
        filtered_df = filtered_df[filtered_df['Contract_period'] == contract_filter]

    if location_filter == "Yes (Near)":
        filtered_df = filtered_df[filtered_df['Near_Location'] == 1]
    elif location_filter == "No (Far)":
        filtered_df = filtered_df[filtered_df['Near_Location'] == 0]

    if partner_filter == "Yes":
        filtered_df = filtered_df[filtered_df['Partner'] == 1]
    elif partner_filter == "No":
        filtered_df = filtered_df[filtered_df['Partner'] == 0]

    if promo_friend_filter == "Yes":
        filtered_df = filtered_df[filtered_df['Promo_friends'] == 1]
    elif promo_friend_filter == "No":
        filtered_df = filtered_df[filtered_df['Promo_friends'] == 0]

    return view_option, filtered_df
