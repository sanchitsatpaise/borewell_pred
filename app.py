# -*- coding: utf-8 -*-
"""
Created on Sun Dec 28 14:39:40 2025

@author: Sanchit Satpaise
"""

import streamlit as st
import pandas as pd
import pickle
import numpy as np

# --------------------------------------------------
# Page Configuration
# --------------------------------------------------
st.set_page_config(
    page_title="Yashoda Borewell Success Predictor",
    layout="wide",
    page_icon="🚰"
)

# --------------------------------------------------
# Custom CSS (Heavy Decoration 😎)
# --------------------------------------------------
st.markdown("""
<style>

/* Background Image */
.stApp {
    background-image: url("https://i.pinimg.com/originals/64/66/18/646618458984113936.jpg");
    background-size: cover;
    background-attachment: fixed;
}

/* Overlay for readability */
.main {
    background: rgba(255,255,255,0.85);
    padding: 30px;
    border-radius: 20px;
}

/* Title Styling */
h1 {
    text-align: center;
    font-size: 3.2rem;
    font-weight: 800;
    color: #0b3d91;
    text-shadow: 2px 2px 5px rgba(0,0,0,0.15);
}

/* Subtitle */
.subtitle {
    text-align: center;
    font-size: 1.2rem;
    color: #333;
    margin-bottom: 30px;
}

/* Cards */
.card {
    background: rgba(255,255,255,0.9);
    padding: 25px;
    border-radius: 18px;
    box-shadow: 0px 8px 25px rgba(0,0,0,0.12);
    margin-bottom: 20px;
}

/* Metric styling */
[data-testid="stMetric"] {
    background: linear-gradient(135deg, #e0f7fa, #ffffff);
    padding: 20px;
    border-radius: 15px;
    box-shadow: 0 6px 18px rgba(0,0,0,0.12);
}

/* Button Styling */
.stButton > button {
    background: linear-gradient(135deg, #0072ff, #00c6ff);
    color: white;
    font-size: 18px;
    padding: 12px 30px;
    border-radius: 12px;
    border: none;
    box-shadow: 0px 5px 15px rgba(0,0,0,0.25);
    transition: 0.3s;
}

.stButton > button:hover {
    transform: scale(1.05);
    background: linear-gradient(135deg, #005bea, #00bcd4);
}

/* Footer */
.footer {
    text-align: center;
    color: #111;
    font-size: 14px;
    margin-top: 40px;
}

</style>
""", unsafe_allow_html=True)

# --------------------------------------------------
# Title Section
# --------------------------------------------------
st.markdown("<div class='main'>", unsafe_allow_html=True)

st.title("🚰 Yashoda Borewell Success Predictor")
st.markdown("""
<div class="subtitle">
Smart Groundwater Prediction System for Rural & Semi-Urban Maharashtra  
<br>📍 Chandrapur Region | 🌧️ Soil & Hydro Analysis 
</div>
""", unsafe_allow_html=True)

# --------------------------------------------------
# Load Data & Model
# --------------------------------------------------
@st.cache_resource
def load_resources():
    df = pd.read_csv("ml_project_borewell.csv")
    df = df.loc[:, ~df.columns.str.contains("^Unnamed")]

    with open("borewell_prediction_model.pkl", "rb") as f:
        pkg = pickle.load(f)

    return df, pkg

try:
    df, pkg = load_resources()

    m_depth = pkg["model_depth"]
    m_rate = pkg["model_rate"]
    m_soil = pkg["model_soil"]
    m_status = pkg["model_status"]

    le_loc = pkg["le_loc"]
    le_belong = pkg["le_belong"]
    le_soil = pkg["le_soil"]
    le_status = pkg["le_status"]

    # --------------------------------------------------
    # User Input Section
    # --------------------------------------------------
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.subheader("📍 Select Location Details")

    col1, col2 = st.columns(2)

    with col1:
        taluka_list = sorted(df["taluka"].unique())
        selected_taluka = st.selectbox("Select Taluka", taluka_list)

    with col2:
        location_list = sorted(df[df["taluka"] == selected_taluka]["location"].unique())
        selected_location = st.selectbox("Select Village", location_list)

    st.markdown("</div>", unsafe_allow_html=True)

    # --------------------------------------------------
    # Prediction
    # --------------------------------------------------
    if st.button("🔍 Generate Borewell Report"):
        row = df[df["location"] == selected_location].iloc[0]
        belonging_loc = row["belonging_location"]

        loc_encoded = le_loc.transform([selected_location])[0]
        belong_encoded = le_belong.transform([belonging_loc])[0]

        X = np.array([[loc_encoded, belong_encoded]])

        pred_depth = m_depth.predict(X)[0]
        pred_rate = m_rate.predict(X)[0]
        pred_soil = le_soil.inverse_transform([m_soil.predict(X)[0]])[0]
        pred_status = le_status.inverse_transform([m_status.predict(X)[0]])[0]

        # --------------------------------------------------
        # Results Section
        # --------------------------------------------------
        st.markdown("<div class='card'>", unsafe_allow_html=True)
        st.subheader(f"📊 Borewell Prediction Report – {selected_location}")

        r1, r2, r3, r4 = st.columns(4)

        r1.metric("💧 Estimated Water Depth", f"{pred_depth:.2f} ft")
        r2.metric("📈 Success Probability", f"{pred_rate:.1f}%")

        with r3:
            st.write("🌱 **Soil Quality**")
            st.info(pred_soil)

        with r4:
            st.write("🚧 **Drilling Status**")
            if pred_status == "Success":
                st.success("✅ SUCCESS")
            else:
                st.error("❌ FAIL")

        st.markdown(f"""
        **Geological Insight:**  
        The selected village belongs to **{belonging_loc} zone**.  
        Based on hydro-geological patterns, borewell drilling up to **~{pred_depth:.0f} feets**
        shows a **{pred_rate:.1f}% probability** of success.
        """)

        st.markdown("</div>", unsafe_allow_html=True)

except Exception as e:
    st.error(f"⚠️ Application Error: {e}")

# --------------------------------------------------
# Footer
# --------------------------------------------------
st.markdown("""
<div class="footer">
<hr>
🌍 Developed for <b>Maharashtra Groundwater Management</b><br>
🚰 “Jal hai toh kal hai”<br>
© 2025 Yashoda Borewell Solutions
</div>
""", unsafe_allow_html=True)

st.markdown("</div>", unsafe_allow_html=True)

