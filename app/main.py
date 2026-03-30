import streamlit as st
import pandas as pd
import joblib
import numpy as np
import shap
import matplotlib.pyplot as plt

# --- PAGE CONFIG ---
st.set_page_config(page_title="GymSense: AI CRM", page_icon="🏋️‍♂️", layout="wide")

# --- 1. LOAD DATA, MODELS, & EXPLAINERS ---
@st.cache_resource
def load_ai_engines():
    scaler = joblib.load('gym_scaler_v2.pkl')
    models = {
        'ROS': joblib.load('model_ros_xgb.pkl'),
        'SMOTE': joblib.load('model_smote_xgb.pkl'),
        'ADASYN': joblib.load('model_adasyn_xgb.pkl')
    }
    explainers = {
        'ROS': shap.TreeExplainer(models['ROS']),
        'SMOTE': shap.TreeExplainer(models['SMOTE']),
        'ADASYN': shap.TreeExplainer(models['ADASYN'])
    }
    return scaler, models, explainers

@st.cache_data
def load_and_predict():
    df = pd.read_csv('../data/gym_churn_V2.csv')
    df_live = df.drop(columns=['Churn'], errors='ignore')
    X_math = df_live.drop(columns=['Name', 'Email', 'Phone_Number'])
    
    scaler, models, _ = load_ai_engines()
    X_scaled = scaler.transform(X_math)
    
    df_live['Risk_ROS'] = models['ROS'].predict(X_scaled)
    df_live['Risk_SMOTE'] = models['SMOTE'].predict(X_scaled)
    df_live['Risk_ADASYN'] = models['ADASYN'].predict(X_scaled)
    
    df_live['Consensus_Risk'] = np.where(
        (df_live['Risk_ROS'] == 1) & (df_live['Risk_SMOTE'] == 1) & (df_live['Risk_ADASYN'] == 1), 
        "🚨 GUARANTEED CHURN", "Safe / Uncertain"
    )
    return df_live

try:
    df_results = load_and_predict()
except Exception as e:
    st.error(f"Error loading files: {e}")
    st.stop()

# --- 2. SIDEBAR FILTERS ---
st.sidebar.header("⚙️ Dashboard Controls")
view_option = st.sidebar.selectbox(
    "Select CRM View:",
    ["🚨 High-Risk Consensus", "⭐ VIP & Loyal Members", "🟠 ROS Prediction Only", "🟠 SMOTE Prediction Only", "🟠 ADASYN Prediction Only"]
)

st.sidebar.markdown("---")
st.sidebar.header("🔍 Filter Demographics")
min_age, max_age = int(df_results['Age'].min()), int(df_results['Age'].max())
selected_age = st.sidebar.slider("Age Range:", min_age, max_age, (min_age, max_age))
group_class_filter = st.sidebar.radio("Attends Group Classes?", ["All", "Yes", "No"])
contract_filter = st.sidebar.selectbox("Contract Period (Months)", ["All", 1, 6, 12])

st.sidebar.markdown("---")
st.sidebar.header("📍 Location & Partnerships")
location_filter = st.sidebar.radio("Lives/Works Near Gym?", ["All", "Yes (Near)", "No (Far)"])
partner_filter = st.sidebar.radio("Corporate Partner Member?", ["All", "Yes", "No"])
promo_friend_filter = st.sidebar.radio("Joined via Friend Referral?", ["All", "Yes", "No"])

st.sidebar.markdown("---")
st.sidebar.header("⏳ Member History")
min_life, max_life = int(df_results['Lifetime'].min()), int(df_results['Lifetime'].max())
selected_lifetime = st.sidebar.slider("Months as Member (Lifetime):", min_life, max_life, (min_life, max_life))

# --- 3. APPLYING THE FILTERS ---
# 1. Apply Age Filter
filtered_df = df_results[(df_results['Age'] >= selected_age[0]) & (df_results['Age'] <= selected_age[1])]

# 2. Apply Group Class Filter
if group_class_filter == "Yes":
    filtered_df = filtered_df[filtered_df['Group_visits'] == 1]
elif group_class_filter == "No":
    filtered_df = filtered_df[filtered_df['Group_visits'] == 0]

# 3. Apply Contract Filter
if contract_filter != "All":
    filtered_df = filtered_df[filtered_df['Contract_period'] == contract_filter]

# 4. Apply Location Filter
if location_filter == "Yes (Near)":
    filtered_df = filtered_df[filtered_df['Near_Location'] == 1]
elif location_filter == "No (Far)":
    filtered_df = filtered_df[filtered_df['Near_Location'] == 0]

# 5. Apply Corporate Partner Filter
if partner_filter == "Yes":
    filtered_df = filtered_df[filtered_df['Partner'] == 1]
elif partner_filter == "No":
    filtered_df = filtered_df[filtered_df['Partner'] == 0]

# 6. Apply Friend Referral Filter
if promo_friend_filter == "Yes":
    filtered_df = filtered_df[filtered_df['Promo_friends'] == 1]
elif promo_friend_filter == "No":
    filtered_df = filtered_df[filtered_df['Promo_friends'] == 0]

# 7. Apply Lifetime Slider Filter
filtered_df = filtered_df[(filtered_df['Lifetime'] >= selected_lifetime[0]) & (filtered_df['Lifetime'] <= selected_lifetime[1])]
# --- 4. APPLYING THE VIEW OPTION & REVENUE TRACKER ---
monthly_fee = 1500 # Assuming ₹1500 per month for the gym

if view_option == "🚨 High-Risk Consensus":
    display_df = filtered_df[filtered_df['Consensus_Risk'] == "🚨 GUARANTEED CHURN"]
    st.title("🚨 High-Risk Consensus List")
    st.markdown("Flagged by **ALL THREE** AI models. Immediate intervention required.")
    
    # REVENUE AT RISK TICKER
    rev_at_risk = len(display_df) * monthly_fee
    col1, col2 = st.columns(2)
    col1.metric(label="Total Members at Risk", value=len(display_df))
    col2.metric(label="Monthly Revenue at Risk", value=f"₹{rev_at_risk:,}", delta="-High Risk", delta_color="normal")

elif view_option == "⭐ VIP & Loyal Members":
    # THE NEW LOYALTY MATH: Safe, >5 months lifetime, and negative attendance drop (going to the gym MORE often)
    display_df = filtered_df[(filtered_df['Consensus_Risk'] == "Safe / Uncertain") & 
                             (filtered_df['Lifetime'] > 5) & 
                             (filtered_df['Attendance_Drop'] < 0)]
    st.title("⭐ VIP & Loyal Members")
    st.markdown("These members show ironclad consistency. Excellent targets for personal training upsells or referral requests.")
    st.metric(label="Total Highly Loyal Members", value=len(display_df), delta="+Highly Stable")

elif view_option == "🟠 ROS Prediction Only":
    display_df = filtered_df[filtered_df['Risk_ROS'] == 1]
    st.title("🟠 ROS Prediction List")
    st.metric(label="Total Members", value=len(display_df))
elif view_option == "🟠 SMOTE Prediction Only":
    display_df = filtered_df[filtered_df['Risk_SMOTE'] == 1]
    st.title("🟠 SMOTE Prediction List")
    st.metric(label="Total Members", value=len(display_df))
elif view_option == "🟠 ADASYN Prediction Only":
    display_df = filtered_df[filtered_df['Risk_ADASYN'] == 1]
    st.title("🟠 ADASYN Prediction List")
    st.metric(label="Total Members", value=len(display_df))

manager_view_cols = ['Name', 'Phone_Number', 'Age', 'Lifetime', 'Contract_period', 'Attendance_Drop']
st.dataframe(display_df[manager_view_cols], use_container_width=True)

# =====================================================================
# --- PHASE 1.5: BULK ANALYTICS DASHBOARD ---
# =====================================================================
st.markdown("---")
st.header("📊 Bulk Analytics: Segment Overview")

if not display_df.empty and view_option != "⭐ VIP & Loyal Members":
    st.write("Understanding the macro-trends for this specific filtered group.")
    
    # Isolate the math columns for the current filtered group
    math_columns = df_results.drop(columns=['Name', 'Email', 'Phone_Number', 'Risk_ROS', 'Risk_SMOTE', 'Risk_ADASYN', 'Consensus_Risk']).columns
    bulk_math = display_df[math_columns]
    
    # Scale the data using our pre-loaded scaler
    scaler, models, explainers = load_ai_engines()
    bulk_scaled = scaler.transform(bulk_math)
    
    # Use ROS explainer as the baseline for rapid group analytics
    explainer = explainers['ROS']
    shap_values_bulk = explainer(bulk_scaled)
    
    # Calculate mean absolute SHAP values across the entire filtered group
    mean_shap = np.abs(shap_values_bulk[0].values if isinstance(shap_values_bulk, list) else shap_values_bulk.values).mean(axis=0)
    
    # Create a DataFrame for easy plotting
    macro_trends = pd.DataFrame({
        'Feature': math_columns,
        'Impact': mean_shap
    })
    
    # Translate features to English using our dictionary
    feature_translator = {
        'Lifetime': 'Overall Time as Member',
        'Contract_period': 'Contract Length',
        'Age': 'Demographic Profile',
        'Avg_class_frequency_current_month': 'Recent Visit Frequency',
        'Avg_class_frequency_total': 'Historical Visit Frequency',
        'Group_visits': 'Group Class Attendance',
        'Attendance_Drop': 'Motivation / Routine Change',
        'Months_Served': 'Current Month in Contract',
        'Age_at_Joining': 'Starting Age',
        'Near_Location': 'Distance to Gym',
        'Partner': 'Corporate Partner Status',
        'Promo_friends': 'Friend Referral Status'
    }
    macro_trends['Feature'] = macro_trends['Feature'].map(lambda x: feature_translator.get(x, x))
    
    # Sort and grab the top 5 biggest factors
    macro_trends = macro_trends.sort_values(by='Impact', ascending=False).head(5)
    
    # Display side-by-side layout
    col_chart, col_text = st.columns([2, 1])
    with col_chart:
        st.subheader("Top 5 Macro Churn Drivers")
        st.bar_chart(macro_trends.set_index('Feature'), color="#ff4b4b")
        
    with col_text:
        st.subheader("💡 Strategic Action")
        top_macro_reason = macro_trends.iloc[0]['Feature']
        st.info(f"For this specific segment of **{len(display_df)} members**, the #1 overarching issue is **{top_macro_reason}**.")
        st.success("If you are launching a mass marketing or email campaign today, target this specific pain point!")

elif view_option == "⭐ VIP & Loyal Members":
    st.info("Bulk analytics are currently optimized to identify high-risk churn drivers.")

# =====================================================================
# --- PHASE 2: THE MEMBER 360 & SHAP X-RAY ---
# =====================================================================
st.markdown("---")
st.header("🧠 Member 360° & AI X-Ray")

if not display_df.empty:
    selected_name = st.selectbox("Select Member Name to generate dossier:", display_df['Name'].tolist())
    
    if selected_name:
        person_data = df_results[df_results['Name'] == selected_name].iloc[0]
        math_columns = df_results.drop(columns=['Name', 'Email', 'Phone_Number', 'Risk_ROS', 'Risk_SMOTE', 'Risk_ADASYN', 'Consensus_Risk']).columns
        person_math = person_data[math_columns].values.reshape(1, -1)
        
        scaler, models, explainers = load_ai_engines()
        person_scaled = scaler.transform(person_math)
        
        st.markdown(f"### 👤 Profile Snapshot: **{selected_name}**")
        
        # --- THE MEMBER 360° SNAPSHOT ---
        snap1, snap2, snap3, snap4 = st.columns(4)
        snap1.metric("Age", int(person_data['Age']))
        snap2.metric("Contract Length", f"{int(person_data['Contract_period'])} Months")
        snap3.metric("Gym Lifetime", f"{int(person_data['Lifetime'])} Months")
        
        # Show if they are slacking or improving this month
        att_drop = person_data['Attendance_Drop']
        trend_label = "Slacking Off" if att_drop > 0 else "Highly Consistent"
        snap4.metric("Recent Routine", trend_label, f"{-att_drop:.2f} diff vs avg")
        st.markdown("<br>", unsafe_allow_html=True)
        
        # --- SHAP X-RAY ---
        tab1, tab2, tab3 = st.tabs(["ROS Assessment", "SMOTE Assessment", "ADASYN Assessment"])
        
        # Dictionary 1: Translates the math feature into English
        feature_translator = {
            'Lifetime': 'Overall Time as Member',
            'Contract_period': 'Contract Length',
            'Age': 'Demographic Profile',
            'Avg_class_frequency_current_month': 'Recent Visit Frequency',
            'Avg_class_frequency_total': 'Historical Visit Frequency',
            'Group_visits': 'Group Class Attendance',
            'Attendance_Drop': 'Motivation / Routine Change',
            'Months_Served': 'Current Month in Contract',
            'Age_at_Joining': 'Starting Age',
            'Near_Location': 'Distance to Gym',
            'Partner': 'Corporate Partner Status',
            'Promo_friends': 'Friend Referral Status'
        }
        
        # Dictionary 2: THE NEW DYNAMIC ACTION LOGIC
        action_translator = {
            'Lifetime': "Reach out to welcome them back. Newer members need extra hand-holding to build a solid gym habit.",
            'Contract_period': "They are on a short-term deal. Offer a heavily discounted 6-month or 12-month upgrade to lock them in.",
            'Age': "Send them a targeted promotion for a fitness program or class designed specifically for their age demographic.",
            'Avg_class_frequency_current_month': "Send a quick 'We miss you!' text to check in on their sudden absence this month.",
            'Avg_class_frequency_total': "Offer a free 1-on-1 Personal Training session to help them build a realistic, consistent workout split.",
            'Group_visits': "Give them a free VIP guest pass so they can bring a friend to a group class and build social ties at the gym.",
            'Attendance_Drop': "They are losing motivation. Call to ask about their fitness goals and offer a free body-composition scan to reset their focus.",
            'Months_Served': "They are nearing a critical point in their billing cycle. Trigger an automated renewal discount email.",
            'Age_at_Joining': "Send a welcome package or beginner's guide to help them feel comfortable continuing their fitness journey.",
            'Near_Location': "Commute is an issue. Highlight your gym's off-peak hours to help them avoid traffic, or promote your digital/at-home workouts.",
            'Partner': "Highlight the benefits of corporate memberships. Ask if their company offers wellness stipends.",
            'Promo_friends': "Send them a 'Refer a Friend' promo code where they get a free month if they bring a workout buddy."
        }

        def render_beautiful_shap(model_name):
            explainer = explainers[model_name]
            shap_values = explainer(person_scaled)
            shap_values.feature_names = math_columns.tolist()
            
            vals = shap_values[0].values
            feature_impacts = list(zip(math_columns.tolist(), vals))
            feature_impacts.sort(key=lambda x: x[1], reverse=True)
            top_reasons = [feat for feat, impact in feature_impacts if impact > 0][:3]
            
            if top_reasons and view_option != "⭐ VIP & Loyal Members":
                st.error(f"🚨 **SYSTEM ALERT:** {selected_name} is exhibiting flight-risk behaviors.")
                col1, col2 = st.columns([1, 1])
                with col1:
                    st.markdown("#### 🔍 Top 3 Reasons for Leaving:")
                    for i, feat in enumerate(top_reasons):
                        clean_reason = feature_translator.get(feat, feat)
                        st.markdown(f"{i+1}. 🚩 **{clean_reason}**")
                
                with col2:
                    st.markdown("#### 💡 Dynamic Action Plan:")
                    # Grab the absolute #1 reason they are leaving
                    primary_reason = top_reasons[0]
                    # Fetch the specific action for that reason, with a default fallback just in case
                    suggested_action = action_translator.get(primary_reason, "Give them a quick check-in call to see how their fitness journey is going.")
                    st.info(suggested_action)
                    
            elif view_option == "⭐ VIP & Loyal Members":
                st.success(f"🏆 **VIP STATUS:** {selected_name} is highly consistent.")
                st.info("💡 **Upsell Opportunity:** Offer them an advanced Personal Training package or ask for a referral!")
            else:
                st.success(f"✅ {selected_name} appears stable according to this specific model.")

            with st.expander("📊 View Raw AI Mathematical Proof"):
                shap.plots.waterfall(shap_values[0], max_display=7, show=False)
                fig = plt.gcf()
                st.pyplot(fig)
                plt.clf()

        with tab1:
            render_beautiful_shap('ROS')
        with tab2:
            render_beautiful_shap('SMOTE')
        with tab3:
            render_beautiful_shap('ADASYN')

else:
    st.info("No members match your current filter settings.")