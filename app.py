import streamlit as st
import pickle

# Set up page configuration
st.set_page_config(page_title="Disease Prediction", page_icon="⚕️", layout="wide")

# Hide Streamlit menu and footer
hide_st_style = """
    <style>
    #MainMenu, footer, header {visibility: hidden;}
    </style>
"""
st.markdown(hide_st_style, unsafe_allow_html=True)

# Dark Professional Theme - Background & Styles
dark_theme = """
<style>
/* Dark Gradient Background */
[data-testid="stAppViewContainer"] {
    background: linear-gradient(135deg, #1E1E2F, #0A0A23);
    color: #FFFFFF;
}

/* Adding an Overlay */
[data-testid="stAppViewContainer"]::before {
    content: "";
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background: rgba(10, 10, 35, 0.85);
    z-index: -1;
}

/* Styling Text */
html, body, .stMarkdown, .stTitle, .stHeader, .stTextInput label, .stNumberInput label, .stSelectbox label, .stButton, .stAlert {
    font-family: 'Poppins', sans-serif;
    color: #E0E0E0;
}

/* Custom Button */
.stButton>button {
    background-color: #4A90E2;
    color: white;
    border-radius: 8px;
    padding: 5px 10px;  /* Adjusted padding for smaller buttons */
    font-weight: bold;
    border: none;
    transition: 0.3s;
    width: 150px;  /* Fixed width for buttons */
}
.stButton>button:hover {
    background-color: #E91E63;
}

/* Sidebar Styling */
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #0A0A23, #1E1E2F);
    color: #FFFFFF;
    padding: 15px;
}
.stSidebar .stButton>button {
    background-color: #E91E63;
    color: white;
}
</style>
"""

st.markdown(dark_theme, unsafe_allow_html=True)

# Load saved models
models = {
    'diabetes': pickle.load(open('diabetes_model.sav', 'rb')),
    'heart_disease': pickle.load(open('heart_disease_model.sav', 'rb')),
    'parkinsons': pickle.load(open('parkinsons_model.sav', 'rb')),
    'lung_cancer': pickle.load(open('lungs_disease_model.sav', 'rb')),
    'thyroid': pickle.load(open('Thyroid_model.sav', 'rb'))
}

# Initialize session state for selected disease
if 'selected_disease' not in st.session_state:
    st.session_state.selected_disease = None

# Main content area
if st.session_state.selected_disease is None:
    st.title("⚕️ Disease Prediction")
    st.write("Select a disease to predict:")
    
    selected = st.selectbox(
        'Choose a Disease',
        ['Select a Disease', 'Diabetes Prediction', 'Heart Disease Prediction', 'Parkinsons Prediction', 'Lung Cancer Prediction', 'Hypo-Thyroid Prediction']
    )

    # Update session state based on selection
    if selected != 'Select a Disease':
        st.session_state.selected_disease = selected

# Sidebar for disease selection
if st.session_state.selected_disease is not None:
    st.sidebar.title("🩺 Disease Prediction")
    
    # Create buttons for disease selection
    diseases = ['Diabetes Prediction', 'Heart Disease Prediction', 'Parkinsons Prediction', 'Lung Cancer Prediction', 'Hypo-Thyroid Prediction']
    
    for disease in diseases:
        if st.sidebar.button(disease):
            st.session_state.selected_disease = disease

    # Display input fields based on the selected disease
    if st.session_state.selected_disease == 'Diabetes Prediction':
        st.title('Diabetes Prediction')
        st.write("Enter the following details:")
        
        with st.form("diabetes_form"):
            col1, col2 = st.columns(2)

            with col1:
                Pregnancies = st.number_input('Number of Pregnancies', min_value=0, max_value=20, format="%d")
                Glucose = st.number_input('Glucose Level (mg/dL)', min_value=0.0, max_value=300.0, format="%.3f", step=0.1)
                BloodPressure = st.number_input('Blood Pressure (mm Hg)', min_value=0.0, max_value=200.0, format="%.3f", step=0.1)
                SkinThickness = st.number_input('Skin Thickness (mm)', min_value=0.0, max_value=100.0, format="%.3f", step=0.1)

            with col2:
                Insulin = st.number_input('Insulin Level (µU/mL)', min_value=0.0, max_value=1000.0, format="%.3f", step=0.1)
                BMI = st.number_input('BMI (kg/m²)', min_value=0.0, max_value=60.0, format="%.3f", step=0.1)
                DiabetesPedigreeFunction = st.number_input('Diabetes Pedigree Function', min_value=0.0, max_value=2.5, format="%.3f", step=0.01)
                Age = st.number_input('Age (years)', min_value=0, max_value=120, format="%d")

            submitted = st.form_submit_button("🔍 Predict")

            if submitted:
                try:
                    diab_prediction = models['diabetes'].predict([[Pregnancies, Glucose, BloodPressure, SkinThickness, Insulin, BMI, DiabetesPedigreeFunction, Age]])
                    diab_diagnosis = '🛑 The person is diabetic' if diab_prediction[0] == 1 else '✅ The person is not diabetic'
                    st.success(diab_diagnosis)
                except Exception as e:
                    st.error(f"An error occurred during prediction: {e}")

    elif st.session_state.selected_disease == 'Heart Disease Prediction':
        st.title('Heart Disease Prediction')
        st.write("Enter the following details:")
        
        with st.form("heart_form"):
            col1, col2 = st.columns(2)

            with col1:
                age = st.number_input('Age (years)', min_value=0, max_value=120, format="%d")
                sex = st.number_input('Gender (1 = Male; 0 = Female)', min_value=0, max_value=1, format="%d")
                cp = st.number_input('Chest Pain Type (0, 1, 2, 3)', min_value=0, max_value=3, format="%d")
                trestbps = st.number_input('Resting Blood Pressure (mm Hg)', min_value=0, max_value=300, format="%d")
                chol = st.number_input('Serum Cholesterol Level (mg/dL)', min_value=0, max_value=600, format="%d")
                fbs = st.number_input('Fasting Blood Sugar (1 = True, 0 = False)', min_value=0, max_value=1, format="%d")

            with col2:
                restecg = st.number_input('Resting ECG Results (0, 1, 2)', min_value=0, max_value=2, format="%d")
                thalach = st.number_input('Maximum Heart Rate Achieved', min_value=0, max_value=250, format="%d")
                exang = st.number_input('Exercise-Induced Angina (1 = Yes, 0 = No)', min_value=0, max_value=1, format="%d")
                oldpeak = st.number_input('ST Depression Induced by Exercise', min_value=0.0, max_value=10.0, format="%.2f")
                slope = st.number_input('Slope of the Peak Exercise ST Segment (0, 1, 2)', min_value=0, max_value=2, format="%d")
                ca = st.number_input('Number of Major Vessels Colored by Fluoroscopy (0–3)', min_value=0, max_value=3, format="%d")
                thal = st.number_input('Thalassemia Type (0, 1, 2, 3)', min_value=0, max_value=3, format="%d")

            submitted = st.form_submit_button("🔍 Predict")

            if submitted:
                try:
                    heart_prediction = models['heart_disease'].predict([[age, sex, cp, trestbps, chol, fbs, restecg, thalach, exang, oldpeak, slope, ca, thal]])
                    heart_diagnosis = '🛑 The person has heart disease' if heart_prediction[0] == 1 else '✅ The person does not have heart disease'
                    st.success(heart_diagnosis)
                except Exception as e:
                    st.error(f"An error occurred during prediction: {e}")

    elif st.session_state.selected_disease == "Parkinsons Prediction":
        st.title("Parkinson's Disease Prediction")
        st.write("Enter the following details to predict Parkinson's disease:")

        with st.form("parkinsons_form"):
            col1, col2 = st.columns(2)

            with col1:
                fo = st.number_input('MDVP:Fo (Hz)', min_value=0.0, format="%.3f", step=0.001)
                fhi = st.number_input('MDVP:Fhi (Hz)', min_value=0.0, format="%.3f", step=0.001)
                flo = st.number_input('MDVP:Flo (Hz)', min_value=0.0, format="%.3f", step=0.001)
                Jitter_percent = st.number_input('MDVP:Jitter (%)', min_value=0.0, format="%.3f", step=0.001)
                Jitter_Abs = st.number_input('MDVP:Jitter (Abs)', min_value=0.0, format="%.3f", step=0.001)

            with col2:
                RAP = st.number_input('MDVP:RAP', min_value=0.0, format="%.3f", step=0.001)
                PPQ = st.number_input('MDVP:PPQ', min_value=0.0, format="%.3f", step=0.001)
                DDP = st.number_input('Jitter:DDP', min_value=0.0, format="%.3f", step=0.001)
                Shimmer = st.number_input('MDVP:Shimmer', min_value=0.0, format="%.3f", step=0.001)
                Shimmer_dB = st.number_input('MDVP:Shimmer (dB)', min_value=0.0, format="%.3f", step=0.001)

            with st.expander("Advanced Features"):
                Shimmer_APQ3 = st.number_input('Shimmer:APQ3', min_value=0.0, format="%.3f", step=0.001)
                Shimmer_APQ5 = st.number_input('Shimmer:APQ5', min_value=0.0, format="%.3f", step=0.001)
                MDVP_APQ = st.number_input('MDVP:APQ', min_value=0.0, format="%.3f", step=0.001)
                Shimmer_DDA = st.number_input('Shimmer:DDA', min_value=0.0, format="%.3f", step=0.001)
                NHR = st.number_input('NHR', min_value=0.0, format="%.3f", step=0.001)
                HNR = st.number_input('HNR', min_value=0.0, format="%.3f", step=0.001)
                RPDE = st.number_input('RPDE', min_value=0.0, format="%.3f", step=0.001)
                DFA = st.number_input('DFA', min_value=0.0, format="%.3f", step=0.001)
                Spread1 = st.number_input('Spread1', min_value=-100.0, format="%.3f", step=0.001)
                Spread2 = st.number_input('Spread2', min_value=0.0, format="%.3f", step=0.001)
                D2 = st.number_input('D2', min_value=0.0, format="%.3f", step=0.001)
                PPE = st.number_input('PPE', min_value=0.0, format="%.3f", step=0.001)

            submitted = st.form_submit_button("🔍 Predict")

            if submitted:
                try:
                    parkinsons_prediction = models['parkinsons'].predict([[fo, fhi, flo, Jitter_percent, Jitter_Abs, RAP, PPQ, DDP, Shimmer, Shimmer_dB, Shimmer_APQ3, Shimmer_APQ5, MDVP_APQ, Shimmer_DDA, NHR, HNR, RPDE, DFA, Spread1, Spread2, D2, PPE]])
                    parkinsons_diagnosis = "🛑 The person has Parkinson's disease" if parkinsons_prediction[0] == 1 else "✅ The person does not have Parkinson's disease"
                    st.success(parkinsons_diagnosis)
                except Exception as e:
                    st.error(f"An error occurred during prediction: {e}")

    elif st.session_state.selected_disease == "Lung Cancer Prediction":
        st.title("Lung Cancer Prediction")
        st.write("Enter the following details to predict lung cancer:")

        with st.form("lung_cancer_form"):
            col1, col2 = st.columns(2)

            with col1:
                GENDER = st.number_input('Gender (1 = Male; 0 = Female)', min_value=0, max_value=1, format="%d")
                AGE = st.number_input('Age (years)', min_value=0, max_value=120, format="%d")
                SMOKING = st.number_input('Smoking (2 = Yes; 1 = No)', min_value=1, max_value=2, format="%d")
                YELLOW_FINGERS = st.number_input('Yellow Fingers (2 = Yes; 1 = No)', min_value=1, max_value=2, format="%d")
                ANXIETY = st.number_input('Anxiety (2 = Yes; 1 = No)', min_value=1, max_value=2, format="%d")

            with col2:
                PEER_PRESSURE = st.number_input('Peer Pressure (2 = Yes; 1 = No)', min_value=1, max_value=2, format="%d")
                CHRONIC_DISEASE = st.number_input('Chronic Disease (2 = Yes; 1 = No)', min_value=1, max_value=2, format="%d")
                FATIGUE = st.number_input('Fatigue (2 = Yes; 1 = No)', min_value=1, max_value=2, format="%d")
                ALLERGY = st.number_input('Allergy (2 = Yes; 1 = No)', min_value=1, max_value=2, format="%d")
                WHEEZING = st.number_input('Wheezing (2 = Yes; 1 = No)', min_value=1, max_value=2, format="%d")

            with st.expander("Additional Symptoms"):
                ALCOHOL_CONSUMING = st.number_input('Alcohol Consuming (2 = Yes; 1 = No)', min_value=1, max_value=2, format="%d")
                COUGHING = st.number_input('Coughing (2 = Yes; 1 = No)', min_value=1, max_value=2, format="%d")
                SHORTNESS_OF_BREATH = st.number_input('Shortness Of Breath (2 = Yes; 1 = No)', min_value=1, max_value=2, format="%d")
                SWALLOWING_DIFFICULTY = st.number_input('Swallowing Difficulty (2 = Yes; 1 = No)', min_value=1, max_value=2, format="%d")
                CHEST_PAIN = st.number_input('Chest Pain (2 = Yes; 1 = No)', min_value=1, max_value=2, format="%d")

            submitted = st.form_submit_button("🔍 Predict")

            if submitted:
                try:
                    lungs_prediction = models['lung_cancer'].predict([[GENDER, AGE, SMOKING, YELLOW_FINGERS, ANXIETY, PEER_PRESSURE, CHRONIC_DISEASE, FATIGUE, ALLERGY, WHEEZING, ALCOHOL_CONSUMING, COUGHING, SHORTNESS_OF_BREATH, SWALLOWING_DIFFICULTY, CHEST_PAIN]])
                    lungs_diagnosis = "🛑 The person has lung cancer" if lungs_prediction[0] == 1 else "✅ The person does not have lung cancer"
                    st.success(lungs_diagnosis)
                except Exception as e:
                    st.error(f"An error occurred during prediction: {e}")

    # Hypo-Thyroid Prediction Section
    elif st.session_state.selected_disease == "Hypo-Thyroid Prediction":
        st.title("Hypo-Thyroid Prediction")
        st.write("Enter the following details to predict hypo-thyroid disease:")

        with st.form("thyroid_form"):
            col1, col2 = st.columns(2)

            with col1:
                age = st.number_input('Age (years)', min_value=0, max_value=120, format="%d")
                sex = st.number_input('Sex (1 = Male; 0 = Female)', min_value=0, max_value=1, format="%d")
                on_thyroxine = st.number_input('On Thyroxine (1 = Yes; 0 = No)', min_value=0, max_value=1, format="%d")

            with col2:
                tsh = st.number_input('TSH Level (mIU/L)', min_value=0.0, format="%.3f", step=0.001)
                t3_measured = st.number_input('T3 Measured (1 = Yes; 0 = No)', min_value=0, max_value=1, format="%d")
                t3 = st.number_input('T3 Level (ng/dL)', min_value=0.0, format="%.3f", step=0.001)
                tt4 = st.number_input('TT4 Level (µg/dL)', min_value=0.0, format="%.3f", step=0.001)

            submitted = st.form_submit_button("🔍 Predict")

            if submitted:
                try:
                    thyroid_prediction = models['thyroid'].predict([[age, sex, on_thyroxine, tsh, t3_measured, t3, tt4]])
                    thyroid_diagnosis = "🛑 The person has Hypo-Thyroid disease" if thyroid_prediction[0] == 1 else "✅ The person does not have Hypo-Thyroid disease"
                    st.success(thyroid_diagnosis)
                except Exception as e:
                    st.error(f"An error occurred during prediction: {e}")

# End of the Streamlit application
