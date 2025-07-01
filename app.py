import streamlit as st
import numpy as np
import joblib

# Set page config
st.set_page_config(
    page_title="🩺 Diabetes Risk Assessment",
    page_icon="🩺",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for enhanced healthcare-themed UI with animations and light effects
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap');

    .main {
        background: linear-gradient(135deg, #e6f0fa 0%, #f5f7fa 100%);
        padding: 30px;
        min-height: 100vh;
    }

    /* Animated Title */
    h1 {
        color: #1a3c6d;
        font-family: 'Inter', sans-serif;
        font-weight: 700;
        font-size: 2.5rem;
        text-align: center;
        animation: typing 2s steps(30, end), blink-caret 0.75s step-end infinite;
        white-space: nowrap;
        overflow: hidden;
        border-right: 3px solid #2196F3;
    }

    @keyframes typing {
        from { width: 0; }
        to { width: 100%; }
    }

    @keyframes blink-caret {
        from, to { border-color: transparent; }
        50% { border-color: #2196F3; }
    }

    /* Card Styling with Glow */
    .card {
        background: white;
        border-radius: 12px;
        padding: 25px;
        box-shadow: 0 4px 20px rgba(0,0,0,0.1), 0 0 10px rgba(33,150,243,0.2);
        margin-bottom: 25px;
        transition: transform 0.3s ease, box-shadow 0.3s ease;
    }

    .card:hover {
        transform: translateY(-5px);
        box-shadow: 0 6px 25px rgba(0,0,0,0.15), 0 0 15px rgba(33,150,243,0.3);
    }

    /* Input Styling with Animation */
    .stNumberInput>div>input {
        border: 1px solid #e0e0e0;
        border-radius: 8px;
        padding: 12px;
        background-color: white;
        transition: all 0.3s ease;
    }

    .stNumberInput>div>input:focus {
        border-color: #2196F3;
        box-shadow: 0 0 8px rgba(33,150,243,0.3);
        background-color: #f8fbff;
    }

    /* Button with Light Effect */
    .stButton>button {
        background: linear-gradient(45deg, #2196F3, #42a5f5);
        color: white;
        font-weight: 600;
        font-family: 'Inter', sans-serif;
        border-radius: 10px;
        padding: 12px 24px;
        border: none;
        position: relative;
        overflow: hidden;
        transition: all 0.3s ease;
        width: 100%;
        text-transform: uppercase;
        letter-spacing: 1px;
    }

    .stButton>button:hover {
        background: linear-gradient(45deg, #1976D2, #2196F3);
        box-shadow: 0 4px 15px rgba(33,150,243,0.4);
        transform: translateY(-2px);
    }

    .stButton>button::after {
        content: '';
        position: absolute;
        top: 50%;
        left: 50%;
        width: 0;
        height: 0;
        background: rgba(255,255,255,0.3);
        border-radius: 50%;
        transform: translate(-50%, -50%);
        transition: width 0.6s ease, height 0.6s ease;
    }

    .stButton>button:hover::after {
        width: 200px;
        height: 200px;
    }

    /* Progress Bar */
    .stProgress .st-bo {
        background-color: #e3f2fd;
        border-radius: 8px;
    }

    .stProgress .st-bo > div {
        background: linear-gradient(90deg, #2196F3, #42a5f5);
        border-radius: 8px;
        animation: progress-pulse 2s ease-in-out infinite;
    }

    @keyframes progress-pulse {
        0% { opacity: 1; }
        50% { opacity: 0.7; }
        100% { opacity: 1; }
    }

    /* Subheader and Text */
    h3 {
        color: #2c5282;
        font-family: 'Inter', sans-serif;
        font-weight: 600;
        font-size: 1.5rem;
    }

    .footer {
        text-align: center;
        color: #666;
        padding: 20px;
        font-size: 14px;
        font-family: 'Inter', sans-serif;
        border-top: 1px solid #e0e0e0;
        margin-top: 30px;
    }

    /* Responsive Design */
    @media (max-width: 768px) {
        h1 {
            font-size: 2rem;
        }
        .card {
            padding: 15px;
        }
    }
    </style>
""", unsafe_allow_html=True)

# Load model and scaler
try:
    model = joblib.load("model.pkl")
    scaler = joblib.load("scaler.pkl")
except Exception as e:
    st.error(f"❌ Error loading model or scaler: {e}")
    st.stop()

# Sidebar with information
with st.sidebar:
    st.image("https://via.placeholder.com/150x50?text=HealthCare+Logo", use_column_width=True)
    st.markdown("### About This App")
    st.markdown("""
    This Diabetes Risk Assessment tool uses advanced machine learning to predict diabetes risk based on your health metrics.
    - Clinically-inspired design
    - Real-time risk assessment
    - Secure and private
    """)
    st.markdown("**Note**: Always consult a healthcare professional for medical advice.")

# Main content
st.title("🩺 Diabetes Risk Assessment")
st.markdown("Enter your health information below to assess your diabetes risk. All fields are required.")

# Input form in card layout
with st.form("diabetes_form"):
    st.markdown("### 📋 Patient Health Profile")
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown("#### General Health")
        preg = st.number_input("Pregnancies", min_value=0, step=1, help="Number of times pregnant")
        glucose = st.number_input("Glucose (mg/dL)", min_value=0.0, step=0.1, help="Blood glucose level")
        bp = st.number_input("Blood Pressure (mm Hg)", min_value=0.0, step=0.1, help="Diastolic blood pressure")
        skin = st.number_input("Skin Thickness (mm)", min_value=0.0, step=0.1, help="Triceps skin fold thickness")
        st.markdown('</div>', unsafe_allow_html=True)

    with col2:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown("#### Metabolic Profile")
        insulin = st.number_input("Insulin (mu U/ml)", min_value=0.0, step=0.1, help="Serum insulin level")
        bmi = st.number_input("BMI", min_value=0.0, step=0.1, help="Body Mass Index")
        dpf = st.number_input("Diabetes Pedigree Function", min_value=0.0, step=0.01, help="Diabetes family history score")
        age = st.number_input("Age", min_value=1, step=1, help="Age in years")
        st.markdown('</div>', unsafe_allow_html=True)

    # Submit button
    submit = st.form_submit_button("🔍 Assess Risk")

# Validation and prediction
if submit:
    # Input validation
    if any([preg < 0, glucose <= 0, bp <= 0, skin <  Platelets < 0, insulin < 0, bmi <= 0, dpf <= 0, age <= 0]):
        st.error("⚠️ Please enter valid values for all fields (positive numbers, non-zero for glucose, BP, BMI, DPK, and age).")
    else:
        with st.spinner("Analyzing health data..."):
            # Simulate analysis progress
            progress = st.progress(0)
            for i in range(100):
                progress.progress(i + 1)
            
            # Prediction
            input_data = np.array([[preg, glucose, bp, skin, insulin, bmi, dpf, age]])
            scaled_data = scaler.transform(input_data)
            prediction = model.predict(scaled_data)[0]
            probability = model.predict_proba(scaled_data)[0][1]
            
            # Result display
            st.markdown('<div class="card">', unsafe_allow_html=True)
            if prediction == 1:
                st.error(f"🟥 High Risk: Diabetic (Confidence: {probability:.1%})")
                st.markdown("""
                **Recommendation**: Your results indicate a high risk of diabetes. Please consult a healthcare provider for a comprehensive evaluation and personalized advice.
                """)
            else:
                st.success(f"🟩 Low Risk: Non-Diabetic (Confidence: {1-probability:.1%})")
                st.markdown("""
                **Recommendation**: Your results suggest a low risk of diabetes. Maintain a healthy lifestyle and schedule regular check-ups.
                """)
            st.info("⚠️ This is a predictive tool and not a medical diagnosis. Consult a doctor for professional medical advice.")
            st.markdown('</div>', unsafe_allow_html=True)

# Footer
st.markdown('<div class="footer">Developed by Ashish Sharma | Powered by Streamlit | © 2025 HealthCare Analytics</div>', unsafe_allow_html=True)