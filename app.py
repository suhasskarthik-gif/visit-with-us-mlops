import streamlit as st
import pandas as pd
import joblib
from huggingface_hub import hf_hub_download

st.title("Visit With Us — Wellness Package Prediction")

@st.cache_resource
def load_model():
    path = hf_hub_download(repo_id="suhaskarthik/tourism_package_model",
                           filename="best_pipeline.joblib",
                           repo_type="model")
    return joblib.load(path)

model = load_model()

# collect a subset of inputs for demo — extend to all fields from your data
age = st.number_input("Age", 18, 80)
monthly_inc = st.number_input("Monthly Income", 0, 2000000)
ptype = st.selectbox("TypeofContact", ["Company Invited", "Self Inquiry"])
pitch_duration = st.number_input("Duration of Pitch", 0, 100)
number_of_persons = st.number_input("Number of Persons Visiting", 1, 10)
number_of_children = st.number_input("Number of Children Visiting", 0, 5)
number_of_adults = st.number_input("Number of Adults Visiting", 0, 5)
number_of_trips = st.number_input("Number of Trips", 1, 50)
designation = st.selectbox("Designation", ["Manager", "Executive", "Senior Manager", "AVP", "VP", "Continental", "Director", "Junior Executive"])
gender = st.selectbox("Gender", ["Male", "Female"])
marital_status = st.selectbox("Marital Status", ["Single", "Married", "Divorced"])
occupation = st.selectbox("Occupation", ["Salaried", "Small Business", "Large Business", "Free Lancer", "Government Sector"])
city_tier = st.selectbox("City Tier", [1, 2, 3])
passport = st.selectbox("Passport", [0, 1])
pitch_satisfaction_score = st.selectbox("Pitch Satisfaction Score", [1, 2, 3, 4, 5])
preferred_property_star = st.selectbox("Preferred Property Star", [1.0, 2.0, 3.0, 4.0, 5.0])
product_pitched = st.selectbox("Product Pitched", ["Basic", "Deluxe", "Super Deluxe", "King", "Deluxe"])
own_car = st.selectbox("Own Car", [0, 1])


# build dataframe with same columns order as training (VERY IMPORTANT)
input_df = pd.DataFrame([[age, monthly_inc, ptype, city_tier, pitch_duration, occupation, gender, number_of_persons, product_pitched, preferred_property_star, marital_status, number_of_trips, passport, pitch_satisfaction_score, own_car, number_of_children, number_of_adults, designation]],
                        columns=["Age", "MonthlyIncome", "TypeofContact", "CityTier", "DurationOfPitch", "Occupation", "Gender", "NumberOfPersonVisiting", "ProductPitched", "PreferredPropertyStar", "MaritalStatus", "NumberOfTrips", "Passport", "PitchSatisfactionScore", "OwnCar", "NumberOfChildrenVisiting", "NumberOfAdults", "Designation"])


if st.button("Predict"):
    # ensure column names + preprocessing match training pipeline
    pred = model.predict(input_df)[0]
    prob = model.predict_proba(input_df)[0,1] if hasattr(model, 'predict_proba') else None
    st.success(f"Prediction: {'Will Purchase' if pred==1 else 'Will Not Purchase'}")
    if prob is not None:
        st.info(f"Predicted probability: {prob:.2f}")
