from fastapi import FastAPI

from app.schemas import LoanApplication, PredictionResponse
from src.predict import predict_single


app = FastAPI(
    title="Loan Default Risk Predictor",
    description="A local API that predicts loan default risk using a trained machine learning model.",
    version="1.0.0",
)


@app.get("/")
def home():
    return {
        "message": "Loan Default Risk Predictor API is running."
    }


@app.post("/predict", response_model=PredictionResponse)
def predict_default(application: LoanApplication):
    input_data = application.model_dump()
    result = predict_single(input_data)

    return result