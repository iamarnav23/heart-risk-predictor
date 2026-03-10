import streamlit as st
import requests

API_URL = "http://127.0.0.1:8000/predict"

st.title("Heart Disease Risk Predictor")
st.markdown("Enter patient health details below:")


age = st.number_input("Age", min_value=1, max_value=120)
gender = st.selectbox("Gender", [1,2], format_func=lambda x: "Female" if x==1 else "Male")

height = st.number_input("Height (cm)", min_value=100, max_value=250)
weight = st.number_input("Weight (kg)", min_value=30.0, max_value=200.0)

ap_hi = st.number_input("Systolic Blood Pressure")
ap_lo = st.number_input("Diastolic Blood Pressure")

cholesterol = st.selectbox(
    "Cholesterol Level",
    [1,2,3],
    format_func=lambda x: {1:"Normal",2:"Medium",3:"High"}[x]
)

gluc = st.selectbox(
    "Glucose Level",
    [1,2,3],
    format_func=lambda x: {1:"Normal",2:"Medium",3:"High"}[x]
)

smoke = st.selectbox("Smoker", [0,1], format_func=lambda x: "No" if x==0 else "Yes")
alco = st.selectbox("Alcohol Consumption", [0,1], format_func=lambda x: "No" if x==0 else "Yes")
active = st.selectbox("Physically Active", [0,1], format_func=lambda x: "No" if x==0 else "Yes")


bmi = weight / ((height/100)**2)
st.metric("Calculated BMI", round(bmi,2))


if st.button("Predict Heart Disease Risk"):

    input_data = {
        "age": age,
        "gender": gender,
        "height": height,
        "weight": weight,
        "ap_hi": ap_hi,
        "ap_lo": ap_lo,
        "cholesterol": cholesterol,
        "gluc": gluc,
        "smoke": smoke,
        "alco": alco,
        "active": active
    }

    try:
        response = requests.post(API_URL, json=input_data)
        result = response.json()

        if response.status_code == 200:

            risk = result["risk_probability"]

            st.subheader("Prediction Result")

            if risk > 0.6:
                st.error(f" High Risk ({risk})")
            elif risk > 0.4:
                st.warning(f" Moderate Risk ({risk})")
            else:
                st.success(f" Low Risk ({risk})")

            st.write("### Top Contributing Factors")
            st.write(result["top_contributing_factors"])


            st.subheader(" Health Recommendations")

            if smoke == 1:
                st.warning(" Smoking increases heart disease risk. Consider quitting smoking.")

            if alco == 1:
                st.warning(" Excess alcohol consumption can increase cardiovascular risk. Try reducing alcohol intake.")

            if bmi > 27:
                st.info(" Try to maintain a good bmi between 19 to 25")

            if active == 0:
                st.info(" Regular physical activity improves heart health.")

            st.success(" Maintain a balanced diet, manage stress, and monitor blood pressure regularly.")

        else:
            st.error("API Error")
            st.write(result)

    except requests.exceptions.ConnectionError:
        st.error("❌ Could not connect to FastAPI server")