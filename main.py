from fastapi import FastAPI
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field, computed_field
from typing import Annotated
import pickle
import pandas as pd
import numpy as np


with open("model.pkl", "rb") as f:
    model = pickle.load(f)

with open("scaler.pkl", "rb") as f:
    scaler = pickle.load(f)

with open("features.pkl", "rb") as f:
    features = pickle.load(f)

app = FastAPI(title="Heart Disease Risk Prediction API")


class PatientData(BaseModel):

    age: Annotated[int, Field(..., gt=0, lt=120, description="Age of user in years")]
    gender: Annotated[int, Field(..., description="Gender of User")]
    height: Annotated[float, Field(..., gt=100, lt=250, description="Height of user in cm")]
    weight: Annotated[float, Field(..., gt=30, lt=200, description="Weight of user in kg")]

    ap_hi: Annotated[int, Field(..., gt=80, lt=250, description="Systolic BP of user")]
    ap_lo: Annotated[int, Field(..., gt=40, lt=200, description="Diastolic BP of user")]

    cholesterol: Annotated[int, Field(..., description="Cholestrol level : 1 normal, 2 above normal, 3 high")]
    gluc: Annotated[int, Field(..., description="Glucose level : 1 normal, 2 above normal, 3 high")]

    smoke: Annotated[int, Field(..., description="Smoker : 0 no, 1 yes")]
    alco: Annotated[int, Field(..., description="Alcohol consumption : 0 no, 1 yes")]
    active: Annotated[int, Field(..., description="Physical activity : 0 no, 1 yes ")]


    @computed_field
    @property
    def bmi(self) -> float:
        return self.weight / ((self.height/100) ** 2)


@app.get("/")
def home():
    return {"message: Heart disease risk predictor api"}

@app.post("/predict")

def predict_risk(data: PatientData):

    
    input_df = pd.DataFrame([{
        "gender": data.gender,
        "height": data.height,
        "weight": data.weight,
        "ap_hi": data.ap_hi,
        "ap_lo": data.ap_lo,
        "cholesterol": data.cholesterol,
        "gluc": data.gluc,
        "smoke": data.smoke,
        "alco": data.alco,
        "active": data.active,
        "age_years": data.age,
        "BMI": data.bmi
    }])


    input_df = input_df[features]


    scaled_input = scaler.transform(input_df)


    prediction = model.predict(scaled_input)[0]
    probability = model.predict_proba(scaled_input)[0][1]


    coefficients = model.coef_[0]
    contribution = scaled_input[0] * coefficients

    top_idx = np.argsort(np.abs(contribution))[-3:]
    top_features = [features[i] for i in top_idx]

    result = {
        "risk_probability": round(float(probability), 2),
        "prediction": "High Risk" if prediction >= .75 else "Low Risk",
        "top_contributing_factors": top_features
    }

    return JSONResponse(status_code=200, content=result)