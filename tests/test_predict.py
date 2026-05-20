from src.config import BEST_MODEL_PATH
from src.predict import predict_single


def test_model_file_exists():
    assert BEST_MODEL_PATH.exists()


def test_predict_single_returns_expected_fields():
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

    assert "prediction" in result
    assert "prediction_label" in result
    assert "default_probability" in result
    assert "risk_category" in result

    assert result["prediction"] in [0, 1]
    assert result["prediction_label"] in ["Default", "No Default"]
    assert 0 <= result["default_probability"] <= 1
    assert result["risk_category"] in ["Low", "Medium", "High"]