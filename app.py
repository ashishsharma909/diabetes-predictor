import streamlit as st
import numpy as np
import joblib

st.set_page_config(page_title="Diabetes Prediction", layout="centered")

st.title("🩺 Diabetes Prediction App")
st.write("Enter your health details to check diabetes risk:")

# ✅ Try loading model and scaler with error handling
try:
    model = joblib.load('model.pkl')
    scaler = joblib.load('scaler.pkl')
    st.success("✅ Model & Scaler loaded successfully!")
except Exception as e:
    st.error(f"❌ Error loading model or scaler: {e}")

# ✅ Input form
with st.form("form"):
    col1, col2 = st.columns(2)
    with col1:
        preg = st.number_input("Pregnancies", min_value=0)
        glucose = st.number_input("Glucose", min_value=0.0)
        bp = st.number_input("Blood Pressure", min_value=0.0)
        skin = st.number_input("Skin Thickness", min_value=0.0)
    with col2:
        insulin = st.number_input("Insulin", min_value=0.0)
        bmi = st.number_input("BMI", min_value=0.0)
        dpf = st.number_input("Diabetes Pedigree Function", min_value=0.0)
        age = st.number_input("Age", min_value=1)

    submit = st.form_submit_button("Predict")

# ✅ Prediction logic
if submit:
    try:
        input_data = np.array([[preg, glucose, bp, skin, insulin, bmi, dpf, age]])
        scaled_data = scaler.transform(input_data)
        prediction = model.predict(scaled_data)[0]
        result = "Diabetic" if prediction == 1 else "Non-Diabetic"
        st.success(f"Prediction: **{result}**")
    except Exception as e:
        st.error(f"❌ Prediction failed: {e}")
