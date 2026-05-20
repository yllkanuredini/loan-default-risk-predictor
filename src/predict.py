import pandas as pd
import joblib

from src.config import BEST_MODEL_PATH, PREDICTION_LOG_PATH
from src.utils import setup_logger

logger = setup_logger("prediction_logger", PREDICTION_LOG_PATH)


def load_model():
    if not BEST_MODEL_PATH.exists():
        raise FileNotFoundError(f"Model not found: {BEST_MODEL_PATH}")

    model = joblib.load(BEST_MODEL_PATH)
    logger.info("Model loaded successfully.")
    return model


def assign_risk_category(default_probability: float) -> str:
    if default_probability >= 0.70:
        return "High"
    elif default_probability >= 0.40:
        return "Medium"
    else:
        return "Low"


def predict_single(input_data: dict) -> dict:
    model = load_model()

    input_df = pd.DataFrame([input_data])

    prediction = model.predict(input_df)[0]
    probability = model.predict_proba(input_df)[0][1]

    risk_category = assign_risk_category(probability)

    
    logger.info(
    "Prediction completed. Label=%s, Probability=%.4f, Risk=%s",
    "Default" if prediction == 1 else "No Default",
    probability,
    risk_category,
    )
    
    return {
        "prediction": int(prediction),
        "prediction_label": "Default" if prediction == 1 else "No Default",
        "default_probability": round(float(probability), 4),
        "risk_category": risk_category,
    }


if __name__ == "__main__":
    sample_input = {
        "Age": 46,
        "Income": 84208,
        "LoanAmount": 129188,
        "CreditScore": 451,
        "MonthsEmployed": 26,
        "NumCreditLines": 3,
        "InterestRate": 15.23,
        "LoanTerm": 36,
        "DTIRatio": 0.43,
        "Education": "Master's",
        "EmploymentType": "Unemployed",
        "MaritalStatus": "Divorced",
        "HasMortgage": "Yes",
        "HasDependents": "Yes",
        "LoanPurpose": "Auto",
        "HasCoSigner": "No",
    }

    result = predict_single(sample_input)

    print("\nPrediction result:")
    print(result)