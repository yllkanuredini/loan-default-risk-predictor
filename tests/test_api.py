from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_home_endpoint():
    response = client.get("/")

    assert response.status_code == 200
    assert response.json() == {
        "message": "Loan Default Risk Predictor API is running."
    }


def test_predict_endpoint_valid_input():
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

    response = client.post("/predict", json=sample_input)

    assert response.status_code == 200

    result = response.json()

    assert "prediction" in result
    assert "prediction_label" in result
    assert "default_probability" in result
    assert "risk_category" in result


def test_predict_endpoint_invalid_age():
    sample_input = {
        "Age": -5,
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

    response = client.post("/predict", json=sample_input)

    assert response.status_code == 422


def test_predict_endpoint_invalid_category():
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
        "Education": "Random Degree",
        "EmploymentType": "Unemployed",
        "MaritalStatus": "Divorced",
        "HasMortgage": "Yes",
        "HasDependents": "Yes",
        "LoanPurpose": "Auto",
        "HasCoSigner": "No",
    }

    response = client.post("/predict", json=sample_input)

    assert response.status_code == 422