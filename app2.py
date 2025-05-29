import streamlit as st
import pandas as pd
import joblib

# Load model
model = joblib.load("co2_model.joblib")
# try:
#     model = joblib.load("co2_model.joblib")
#     st.write("✅ Model loaded successfully")
# except Exception as e:
#     st.error(f"❌ Model load failed: {e}")

# Custom CSS styling
st.markdown("""
    <style>
    body {
        background-color: #f0f2f6;
        font-family: 'Segoe UI', sans-serif;
    }
    .main {
        max-width: 800px;
        margin: auto;
        padding: 3rem;
    }
    .stTextInput>div>div>input,
    .stNumberInput>div>div>input,
    .stSelectbox>div>div>div {
        border: 2px solid #ccc;
        border-radius: 9px;
        padding: 8px;
        font-size: 16px;
    }
    .stButton>button {
        background-color: #D2D0A0;
        color: black;
        padding: 10px 20px;
        border-radius: 16px;
        font-size: 16px;
    }
    .stButton>button:hover {
        background-color: #EFEEEA;
    }
    h1 {
        background-color: #B6B09F;
        border: 2px solid #ccc;
        border-radius: 9px;
        padding: 8px;
        text-align: center;
        color: #F4E7E1;
        font-size: 28px;
        margin-bottom: 20px;
    }
    </style>
""", unsafe_allow_html=True)

# App title
st.title("🚗 CO₂ Emissions Predictor")

# Sidebar Inputs
st.sidebar.header("Enter Vehicle Details")

engine_size = st.sidebar.number_input("Engine Size (L)", min_value=0.5, max_value=10.0, step=0.1)
cylinders = st.sidebar.selectbox("Cylinders", [4, 6, 8, 10, 12])
transmission = st.sidebar.selectbox("Transmission", [
    "AS5-5-speed automatic with overdrive",
    "M6-6-speed manual",
    "AV-Continuously Variable Transmission (CVT)",
    "AS6-6-speed automatic with overdrive",
    "A6-6-speed automatic",
    "AM-Automated Manual (manual gear system, automatic clutch)",
    "AS8-8-speed automatic with overdrive"
])
fuel_display = {
    "Regular Gasoline": "Z",
    "Premium Gasoline": "X",
    "Diesel": "D",
    "Ethanol/Flex Fuel (E85)": "E"
}
fuel_choice = st.sidebar.selectbox("Fuel Type", list(fuel_display.keys()))
fuel = fuel_display[fuel_choice]

vehicle_class = st.sidebar.selectbox("Vehicle Class", [
    "COMPACT", "SUV", "MID-SIZE", "SUBCOMPACT", "PICKUP TRUCK", "TWO-SEATER"
])

# Predict button
if st.sidebar.button("Predict CO₂ Emissions"):
    input_df = pd.DataFrame([{
        "ENGINE SIZE": engine_size,
        "CYLINDERS": cylinders,
        "TRANSMISSION": transmission,
        "FUEL": fuel,
        "VEHICLE CLASS": vehicle_class
    }])
    
    # Make prediction
    try:
        prediction = model.predict(input_df)[0]
        st.success(f"Estimated CO₂ Emissions: **{prediction:.2f} g/km**")
    except Exception as e:
        st.error(f"⚠️ Prediction failed: {e}")
