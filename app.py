import streamlit as st
import numpy as np
import joblib

# Load model and scaler
try:
    model = joblib.load("model.pkl")
    scaler = joblib.load("scaler.pkl")
except Exception as e:
    st.error(f"❌ Error loading model or scaler: {e}")
    st.stop()

# Set page config
st.set_page_config(page_title="🩺 Diabetes Prediction by Ashish Sharma", page_icon="🩺", layout="centered")

# Custom CSS for better UI
st.markdown("""
    <style>
    .main {
        background-color: #f4f6fa;
    }
    h1 {
        color: #2c3e50;
        font-size: 2.2rem;
    }
    .stButton>button {
        background-color: #4CAF50;
        color: white;
        font-weight: bold;
        border-radius: 6px;
        height: 3em;
        width: 100%;
    }
    .stTextInput>div>input, .stNumberInput>div>input {
        border-radius: 6px;
        height: 2.5em;
    }
    </style>
""", unsafe_allow_html=True)

# Title section
st.title("🩺 Diabetes Prediction App by Ashish Sharma")
st.write("Fill in your health details below to predict your risk of diabetes.")

# Input form
with st.form("diabetes_form"):
    st.subheader("📝 Health Information")
    col1, col2 = st.columns(2)
    with col1:
        preg = st.number_input("Pregnancies", min_value=0)
        glucose = st.number_input("Glucose (mg/dL)", min_value=0.0)
        bp = st.number_input("Blood Pressure (mm Hg)", min_value=0.0)
        skin = st.number_input("Skin Thickness (mm)", min_value=0.0)
    with col2:
        insulin = st.number_input("Insulin (mu U/ml)", min_value=0.0)
        bmi = st.number_input("BMI", min_value=0.0)
        dpf = st.number_input("Diabetes Pedigree Function", min_value=0.0)
        age = st.number_input("Age", min_value=1)

    submit = st.form_submit_button("🔍 Predict")

# Prediction logic
if submit:
    input_data = np.array([[preg, glucose, bp, skin, insulin, bmi, dpf, age]])
    scaled_data = scaler.transform(input_data)
    prediction = model.predict(scaled_data)[0]
    result = "🟥 Diabetic" if prediction == 1 else "🟩 Non-Diabetic"

    st.success(f"✅ Prediction Result: **{result}**")
    st.info("⚠️ This is a prediction tool. Please consult a doctor for medical advice.")

# Footer
st.markdown("---")
st.markdown(
    "<center>Made with ❤️ by <b>Ashish Sharma</b> | Powered by Streamlit</center>",
    unsafe_allow_html=True,
)
