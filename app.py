import streamlit as st
import numpy as np
import joblib

# Set page config
st.set_page_config(
    page_title="🩺 Diabetes Risk Assessment by Ashish Sharma",
    page_icon="🩺",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for enhanced healthcare-themed UI with animations and light effects
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Roboto:wght@300;400;600;700&display=swap');

    .main {
        background: linear-gradient(135deg, #e3f2fd 0%, #bbdefb 100%);
        padding: 40px;
        min-height: 100vh;
        position: relative;
        overflow: hidden;
    }

    /* Particle Background Effect */
    .particle {
        position: absolute;
        border-radius: 50%;
        background: rgba(33,150,243,0.3);
        animation: particle-float 10s infinite;
    }

    @keyframes particle-float {
        0% { transform: translateY(0); opacity: 0.3; }
        50% { opacity: 0.6; }
        100% { transform: translateY(-100vh); opacity: 0; }
    }

    /* Animated Title */
    h1 {
        color: #1a3c6d;
        font-family: 'Roboto', sans-serif;
        font-weight: 700;
        font-size: 2.8rem;
        text-align: center;
        animation: typing 3s steps(40, end), blink-caret 0.8s step-end infinite;
        white-space: nowrap;
        overflow: hidden;
        border-right: 4px solid #2196F3;
        margin-bottom: 20px;
    }

    @keyframes typing {
        from { width: 0; }
        to { width: 100%; }
    }

    @keyframes blink-caret {
        from, to { border-color: transparent; }
        50% { border-color: #2196F3; }
    }

    /* Card Styling with Glow and Animation */
    .card {
        background: white;
        border-radius: 16px;
        padding: 30px;
        box-shadow: 0 6px 20px rgba(0,0,0,0.1), 0 0 12px rgba(33,150,243,0.2);
        margin-bottom: 30px;
        transition: transform 0.4s ease, box-shadow 0.4s ease;
        animation: fadeInUp 0.6s ease-out;
    }

    .card:hover {
        transform: translateY(-8px);
        box-shadow: 0 8px 25px rgba(0,0,0,0.15), 0 0 15px rgba(33,150,243,0.3);
    }

    @keyframes fadeInUp {
        from { opacity: 0; transform: translateY(20px); }
        to { opacity: 1; transform: translateY(0); }
    }

    /* Input Styling with Floating Labels */
    .stNumberInput {
        position: relative;
        margin-bottom: 20px;
    }

    .stNumberInput label {
        position: absolute;
        top: 12px;
        left: 12px;
        color: #666;
        font-family: 'Roboto', sans-serif;
        font-size: 14px;
        transition: all 0.3s ease;
        pointer-events: none;
    }

    .stNumberInput input:focus + label,
    .stNumberInput input:not(:placeholder-shown) + label {
        top: -10px;
        left: 10px;
        font-size: 12px;
        color: #2196F3;
        background: white;
        padding: 0 4px;
    }

    .stNumberInput>div>input {
        border: 1px solid #e0e0e0;
        border-radius: 10px;
        padding: 14px;
        background-color: white;
        transition: all 0.3s ease;
        font-family: 'Roboto', sans-serif;
    }

    .stNumberInput>div>input:focus {
        border-color: #2196F3;
        box-shadow: 0 0 10px rgba(33,150,243,0.3);
        background-color: #f8fbff;
    }

    /* Button with Light Effect and Animation */
    .stButton>button {
        background: linear-gradient(45deg, #2196F3, #42a5f5);
        color: white;
        font-weight: 600;
        font-family: 'Roboto', sans-serif;
        border-radius: 12px;
        padding: 14px 30px;
        border: none;
        position: relative;
        overflow: hidden;
        transition: all 0.4s ease;
        width: 100%;
        text-transform: uppercase;
        letter-spacing: 1.2px;
        animation: pulse 2s infinite;
    }

    .stButton>button:hover {
        background: linear-gradient(45deg, #1976D2, #2196F3);
        box-shadow: 0 6px 20px rgba(33,150,243,0.5);
        transform: scale(1.05);
    }

    .stButton>button::after {
        content: '';
        position: absolute;
        top: 50%;
        left: 50%;
        width: 0;
        height: 0;
        background: rgba(255,255,255,0.4);
        border-radius: 50%;
        transform: translate(-50%, -50%);
        transition: width 0.6s ease, height 0.6s ease;
    }

    .stButton>button:hover::after {
        width: 300px;
        height: 300px;
    }

    @keyframes pulse {
        0% { box-shadow: 0 0 0 0 rgba(33,150,243,0.4); }
        70% { box-shadow: 0 0 0 15px rgba(33,150,243,0); }
        100% { box-shadow: 0 0 0 0 rgba(33,150,243,0); }
    }

    /* Progress Bar */
    .stProgress .st-bo {
        background-color: #e3f2fd;
        border-radius: 10px;
    }

    .stProgress .st-bo > div {
        background: linear-gradient(90deg, #2196F3, #42a5f5);
        border-radius: 10px;
        animation: progress-pulse 1.5s ease-in-out infinite;
    }

    @keyframes progress-pulse {
        0% { opacity: 1; }
        50% { opacity: 0.7; }
        100% { opacity: 1; }
    }

    /* Subheader and Text */
    h3 {
        color: #2c5282;
        font-family: 'Roboto', sans-serif;
        font-weight: 600;
        font-size: 1.6rem;
        margin-bottom: 20px;
    }

    /* Sidebar Styling */
    .sidebar .card {
        background: rgba(255,255,255,0.95);
        border-radius: 12px;
        padding: 20px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
        animation: fadeInUp 0.6s ease-out;
    }

    .footer {
        text-align: center;
        color: #666;
        padding: 30px;
        font-size: 14px;
        font-family: 'Roboto', sans-serif;
        border-top: 1px solid #e0e0e0;
        margin-top: 40px;
        background: rgba(255,255,255,0.9);
        border-radius: 10px;
    }

    /* Responsive Design */
    @media (max-width: 768px) {
        h1 {
            font-size: 2.2rem;
        }
        .card {
            padding: 20px;
        }
        .stButton>button {
            padding: 12px 20px;
        }
    }
    </style>
    <script>
    // Particle effect
    function createParticle() {
        const particle = document.createElement('div');
        particle.classList.add('particle');
        particle.style.width = Math.random() * 10 + 5 + 'px';
        particle.style.height = particle.style.width;
        particle.style.left = Math.random() * 100 + 'vw';
        particle.style.top = '100vh';
        particle.style.animationDuration = Math.random() * 5 + 5 + 's';
        document.body.appendChild(particle);
        setTimeout(() => particle.remove(), 10000);
    }
    setInterval(createParticle, 500);
    </script>
""", unsafe_allow_html=True)

# Load model and scaler
try:
    model = joblib.load("model.pkl")
    scaler = joblib.load("scaler.pkl")
except Exception as e:
    st.error(f"❌ Error loading model or scaler: {e}")
    st.stop()

# Sidebar with enhanced About section
with st.sidebar:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.image("https://via.placeholder.com/150x50?text=HealthCare+Logo", use_container_width=True)
    st.markdown("### 🩺 About This App")
    st.markdown("""
    **Diabetes Risk Assessment** is a cutting-edge tool designed to help you understand your diabetes risk using advanced machine learning. Developed by Ashish Sharma, this app provides:
    - **Accurate Predictions**: Powered by a robust ML model
    - **User-Friendly Interface**: Intuitive and secure design
    - **Healthcare Focus**: Aligned with medical standards
    - **Instant Results**: Get insights in seconds
    
    **Disclaimer**: This tool is for informational purposes only. Always consult a healthcare professional for a comprehensive diagnosis.
    """)
    st.markdown("#### Why Use This App?")
    st.markdown("""
    - Monitor your health proactively
    - Understand key risk factors
    - Take informed steps toward prevention
    """)
    st.markdown('<div style="text-align: center; margin-top: 20px;"><a href="https://x.ai" target="_blank">Powered by xAI</a></div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

# Main content
st.title("🩺 Diabetes Risk Assessment by Ashish Sharma")
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    st.image("https://images.pexels.com/photos/5473178/pexels-photo-5473178.jpeg", caption="Monitoring your health, one step at a time.", width=300)
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
    if any([preg < 0, glucose <= 0, bp <= 0, skin < 0, insulin < 0, bmi <= 0, dpf <= 0, age <= 0]):
        st.error("⚠️ Please enter valid values for all fields (positive numbers, non-zero for glucose, BP, BMI, DPF, and age).")
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