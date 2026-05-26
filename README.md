# Loan Default Risk Predictor

## Project Overview

Loan Default Risk Predictor is an end-to-end machine learning project that predicts whether a borrower is likely to default on a loan.

The project covers the full workflow:

- SQL-based data exploration
- Data preparation and preprocessing
- Model training and comparison
- Hyperparameter tuning
- Final model evaluation
- FastAPI prediction endpoint
- Basic testing and logging

The model is intended as a decision-support tool, not as an automatic loan approval system.

---

## Problem Type

This is a supervised binary classification problem.

Target column:

- `0` = No Default
- `1` = Default

---

## Dataset

The project uses the Loan Default Prediction dataset from Kaggle.

Dataset summary:

- 255,347 rows
- 18 original columns
- No missing values
- No duplicate rows
- Target column: `Default`

The `LoanID` column was removed before modeling because it is only an identifier.

---

## Tools and Technologies

- Python
- Pandas
- NumPy
- Scikit-learn
- XGBoost
- LightGBM
- FastAPI
- Uvicorn
- Joblib
- Pytest
- SQL Server / SSMS
- Matplotlib / Seaborn

---

## Project Structure

```text
loan-default-risk-predictor/
│
├── app/
│   ├── main.py
│   └── schemas.py
│
├── data/
│   ├── raw/
│   ├── processed/
│   └── sample/
│
├── database/
│   ├── schema.sql
│   ├── sql_insights.md
│   └── queries/
│
├── models/
│   ├── best_model.joblib
│   └── model_metadata.json
│
├── reports/
│   ├── figures/
│   ├── metrics/
│   ├── final_report.md
│   ├── eda_insights.md
│   ├── threshold_strategy.md
│   └── testing_notes.md
│
├── src/
│   ├── config.py
│   ├── data_prep.py
│   ├── features.py
│   ├── train_baselines.py
│   ├── train_advanced.py
│   ├── tune_random_forest.py
│   ├── evaluate.py
│   ├── predict.py
│   ├── threshold_analysis.py
│   ├── feature_importance.py
│   ├── eda.py
│   └── utils.py
│
├── tests/
├── requirements.txt
├── pytest.ini
├── README.md
└── .gitignore
```

---

## Data Preparation

The preprocessing pipeline includes:

- Removing the `LoanID` column
- Splitting data into train, validation, and test sets
- Scaling numerical features
- Encoding categorical features
- Handling missing values with imputation

Dataset split:

- Training set: 178,742 rows
- Validation set: 38,302 rows
- Test set: 38,303 rows

---

## SQL and EDA Summary

SQL Server was used to explore data quality and default-risk patterns.

Main findings:

- The dataset is imbalanced: 88.39% No Default and 11.61% Default.
- Higher default rates appeared among unemployed borrowers.
- Lower income and lower credit score groups showed higher default risk.
- Higher interest rates and larger loan amounts were linked with higher default rates.
- Borrowers without a co-signer or mortgage showed higher default risk.

Python EDA charts were also generated and saved in `reports/figures/`.

---

## Model Development

Models tested:

- Logistic Regression
- Decision Tree
- Random Forest
- Hist Gradient Boosting
- XGBoost
- LightGBM

Random Forest gave the best balance during model comparison, so it was tuned further.

Final selected model:

```text
Random Forest Tuned 3
```

Selected parameters:

```text
n_estimators = 200
max_depth = 14
min_samples_split = 20
min_samples_leaf = 8
class_weight = balanced_subsample
```

---

## Final Test Results

```text
Accuracy: 0.8126
Precision: 0.3029
Recall: 0.4719
F1-score: 0.3690
ROC-AUC: 0.7571
```

Confusion matrix:

```text
[[29025  4830]
 [ 2349  2099]]
```

The model correctly identified 2,099 out of 4,448 actual default cases.

---

## Threshold Strategy

Several probability thresholds were tested.

The final selected threshold is:

```text
0.50
```

It was selected because it produced the best F1-score and gave the best balance between precision and recall.

A lower threshold catches more default cases but creates more false positives. A higher threshold reduces false positives but misses more actual defaults.

---

## Feature Importance

The most important features for the final model included:

- Age
- InterestRate
- Income
- LoanAmount
- MonthsEmployed
- CreditScore
- DTIRatio

These features were also consistent with the SQL and EDA findings.

---

## FastAPI Deployment

Start the API:

```bash
uvicorn app.main:app --reload
```

Open Swagger UI:

```text
http://127.0.0.1:8000/docs
```

Prediction endpoint:

```text
POST /predict
```

Example request:

```json
{
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
  "HasCoSigner": "No"
}
```

Example response:

```json
{
  "prediction": 1,
  "prediction_label": "Default",
  "default_probability": 0.5262,
  "risk_category": "Medium"
}
```

The API includes validation for numerical ranges and allowed categorical values. It can also handle null values through the preprocessing pipeline.

---

## Testing

Tests were added using `pytest`.

Current test coverage includes:

- data cleaning
- duplicate removal
- saved model existence
- prediction output structure
- FastAPI home endpoint
- valid API prediction request
- invalid numerical input
- invalid categorical input

Run tests:

```bash
pytest
```

Current result:

```text
8 passed
```

---

## How to Run

Create virtual environment:

```bash
python -m venv .venv
```

Activate on Windows:

```bash
.venv\Scripts\activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Prepare data:

```bash
python -m src.data_prep
```

Train models:

```bash
python -m src.train_baselines
python -m src.train_advanced
python -m src.tune_random_forest
```

Evaluate final model:

```bash
python -m src.evaluate
```

Run prediction script:

```bash
python -m src.predict
```

Run API:

```bash
uvicorn app.main:app --reload
```

Run tests:

```bash
pytest
```

---

