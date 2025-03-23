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
                Pregnancies = st.number_input('Number of Pregnancies', min_value=0)
                Glucose = st.number_input('Glucose Level', min_value=0)
                BloodPressure = st.number_input('Blood Pressure value', min_value=0)
                SkinThickness = st.number_input('Skin Thickness value', min_value=0)

            with col2:
                Insulin = st.number_input('Insulin Level', min_value=0)
                BMI = st.number_input('BMI value', min_value=0.0)
                DiabetesPedigreeFunction = st.number_input('Diabetes Pedigree Function value', min_value=0.0)
                Age = st.number_input('Age of the Person', min_value=0)

            submitted = st.form_submit_button("🔍 Predict")

            if submitted:
                diab_prediction = models['diabetes'].predict([[Pregnancies, Glucose, BloodPressure, SkinThickness, Insulin, BMI, DiabetesPedigreeFunction, Age]])
                diab_diagnosis = '🛑 The person is diabetic' if diab_prediction[0] == 1 else '✅ The person is not diabetic'
                st.success(diab_diagnosis)

    elif st.session_state.selected_disease == 'Heart Disease Prediction':
        st.title('Heart Disease Prediction')
        st.write("Enter the following details:")
        
        with st.form("heart_form"):
            col1, col2 = st.columns(2)

            with col1:
                age = st.number_input('Age', min_value=0)
                sex = st.number_input('Sex (1 = male; 0 = female)', min_value=0, max_value=1)
                cp = st.number_input('Chest Pain types (0, 1, 2, 3)', min_value=0, max_value=3)

            with col2:
                trestbps = st.number_input('Resting Blood Pressure', min_value=0)
                chol = st.number_input('Serum Cholesterol in mg/dl', min_value=0)

            submitted = st.form_submit_button("🔍 Predict")

            if submitted:
                heart_prediction = models['heart_disease'].predict([[age, sex, cp, trestbps, chol]])
                heart_diagnosis = '🛑 The person has heart disease' if heart_prediction[0] == 1 else '✅ The person does not have heart disease'
                st.success(heart_diagnosis)

    elif st.session_state.selected_disease == "Parkinsons Prediction":
        st.title("Parkinson's Disease")
        st.write("Enter the following details to predict Parkinson's disease:")

        with st.form("parkinsons_form"):
            col1, col2 = st.columns(2)

            with col1:
                fo = st.number_input('MDVP:Fo(Hz)', min_value=0.0)
                fhi = st.number_input('MDVP:Fhi(Hz)', min_value=0.0)
                flo = st.number_input('MDVP:Flo(Hz)', min_value=0.0)
                Jitter_percent = st.number_input('MDVP:Jitter(%)', min_value=0.0)

            with col2:
                Jitter_Abs = st.number_input('MDVP:Jitter(Abs)', min_value=0.0)
                RAP = st.number_input('MDVP:RAP', min_value=0.0)
                PPQ = st.number_input('MDVP:PPQ', min_value=0.0)
                DDP = st.number_input('Jitter:DDP', min_value=0.0)

            submitted = st.form_submit_button("🔍 Predict")

            if submitted:
                parkinsons_prediction = models['parkinsons'].predict([[fo, fhi, flo, Jitter_percent, Jitter_Abs, RAP, PPQ, DDP]])
                parkinsons_diagnosis = "The person has Parkinson's disease" if parkinsons_prediction[0] == 1 else "The person does not have Parkinson's disease"
                st.success(parkinsons_diagnosis)

    elif st.session_state.selected_disease == "Lung Cancer Prediction":
        st.title("Lung Cancer")
        st.write("Enter the following details to predict lung cancer:")

        with st.form("lung_cancer_form"):
            col1, col2 = st.columns(2)

            with col1:
                GENDER = st.number_input('Gender (1 = Male; 0 = Female)', min_value=0, max_value=1)
                AGE = st.number_input('Age', min_value=0)
                SMOKING = st.number_input('Smoking (1 = Yes; 0 = No)', min_value=0, max_value=1)

            with col2:
                YELLOW_FINGERS = st.number_input('Yellow Fingers (1 = Yes; 0 = No)', min_value=0, max_value=1)
                ANXIETY = st.number_input('Anxiety (1 = Yes; 0 = No)', min_value=0, max_value=1)
                PEER_PRESSURE = st.number_input('Peer Pressure (1 = Yes; 0 = No)', min_value=0, max_value=1)

            submitted = st.form_submit_button("🔍 Predict")

            if submitted:
                lungs_prediction = models['lung_cancer'].predict([[GENDER, AGE, SMOKING, YELLOW_FINGERS, ANXIETY, PEER_PRESSURE]])
                lungs_diagnosis = "The person has lung cancer disease" if lungs_prediction[0] == 1 else "The person does not have lung cancer disease"
                st.success(lungs_diagnosis)

    elif st.session_state.selected_disease == "Hypo-Thyroid Prediction":
        st.title("Hypo-Thyroid")
        st.write("Enter the following details to predict hypo-thyroid disease:")

        with st.form("thyroid_form"):
            col1, col2 = st.columns(2)

            with col1:
                age = st.number_input('Age', min_value=0)
                sex = st.number_input('Sex (1 = Male; 0 = Female)', min_value=0, max_value=1)
                on_thyroxine = st.number_input('On Thyroxine (1 = Yes; 0 = No)', min_value=0, max_value=1)

            with col2:
                tsh = st.number_input('TSH Level', min_value=0.0)
                t3_measured = st.number_input('T3 Measured (1 = Yes; 0 = No)', min_value=0, max_value=1)
                t3 = st.number_input('T3 Level', min_value=0.0)

            submitted = st.form_submit_button("🔍 Predict")

            if submitted:
                thyroid_prediction = models['thyroid'].predict([[age, sex, on_thyroxine, tsh, t3_measured, t3]])
                thyroid_diagnosis = "The person has Hypo-Thyroid disease" if thyroid_prediction[0] == 1 else "The person does not have Hypo-Thyroid disease"
                st.success(thyroid_diagnosis)