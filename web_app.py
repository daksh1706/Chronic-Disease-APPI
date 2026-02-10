from fastapi import FastAPI
from pydantic import BaseModel
from src.predict import predict_disease

app = FastAPI(title="Chronic Disease Risk API")

class PatientInput(BaseModel):
    disease: str
    symptoms: dict
    clinical: dict

@app.post("/predict")
def predict(data: PatientInput):
    user_input = {
        **data.symptoms,
        **data.clinical
    }

    risk, accuracy = predict_disease(data.disease, user_input)

    return {
        "disease": data.disease,
        "risk_level": risk,
        "model_accuracy": accuracy
    }
