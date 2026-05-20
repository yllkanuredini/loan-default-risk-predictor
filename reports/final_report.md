# Loan Default Risk Predictor — Final Report

## 1. Project Goal

The goal of this project is to predict whether a borrower is likely to default on a loan using borrower, financial, and loan-related information.

The model predicts:

- `0` = No Default
- `1` = Default

This project was built as a complete machine learning workflow, including SQL exploration, preprocessing, model development, evaluation, deployment, testing, and documentation.

---

## 2. Dataset Summary

The dataset contains:

- 255,347 rows
- 18 original columns
- No missing values
- No duplicate rows

The target column is `Default`.

Target distribution:

| Class | Meaning | Percentage |
|---|---|---:|
| 0 | No Default | 88.39% |
| 1 | Default | 11.61% |

The dataset is imbalanced, so accuracy alone is not enough to evaluate the model.

The `LoanID` column was removed before modeling because it is only an identifier.

---

## 3. Data Preparation

The data preparation process included:

- loading the raw dataset
- removing the `LoanID` column
- splitting data into train, validation, and test sets
- scaling numerical features
- encoding categorical features
- handling missing values in the preprocessing pipeline

Dataset split:

| Split | Rows |
|---|---:|
| Train | 178,742 |
| Validation | 38,302 |
| Test | 38,303 |

Stratified splitting was used to keep the target distribution consistent across all splits.

---

## 4. SQL and EDA Findings

SQL Server and Python EDA were used to understand the dataset before and after modeling.

Main findings:

- Unemployed borrowers had higher default rates.
- Lower-income borrowers defaulted more often.
- Lower credit score groups showed higher default risk.
- Higher interest rates were linked with higher default rates.
- Larger loan amounts were linked with higher default rates.
- Borrowers without a co-signer or mortgage had higher default rates.

These findings showed that the dataset contains useful borrower and loan patterns for default prediction.

The findings show relationships in the data, but they do not prove direct cause and effect.

---

## 5. Models Tested

The project tested both baseline and advanced models.

Baseline models:

- Logistic Regression
- Decision Tree

Advanced models:

- Random Forest
- Hist Gradient Boosting
- XGBoost
- LightGBM

Random Forest was selected for tuning because it gave the strongest F1-score among the first advanced models.

---

## 6. Baseline Model Results

| Model | Accuracy | Precision | Recall | F1-score | ROC-AUC |
|---|---:|---:|---:|---:|---:|
| Logistic Regression | 0.6744 | 0.2172 | 0.6927 | 0.3307 | 0.7486 |
| Decision Tree | 0.6563 | 0.2040 | 0.6754 | 0.3134 | 0.7229 |

Logistic Regression was the stronger baseline because it had better F1-score and ROC-AUC.

---

## 7. Advanced Model Results

| Model | Accuracy | Precision | Recall | F1-score | ROC-AUC |
|---|---:|---:|---:|---:|---:|
| Random Forest | 0.7694 | 0.2643 | 0.5526 | 0.3576 | 0.7504 |
| Hist Gradient Boosting | 0.8872 | 0.6388 | 0.0652 | 0.1183 | 0.7550 |
| XGBoost | 0.7002 | 0.2289 | 0.6679 | 0.3410 | 0.7549 |
| LightGBM | 0.7018 | 0.2307 | 0.6713 | 0.3434 | 0.7542 |

Hist Gradient Boosting had the highest accuracy, but its recall was very low. This means it missed most actual default cases.

Random Forest gave the best F1-score among the advanced models, so it was selected for tuning.

---

## 8. Random Forest Tuning

Several Random Forest configurations were tested.

| Model | Accuracy | Precision | Recall | F1-score | ROC-AUC |
|---|---:|---:|---:|---:|---:|
| Random Forest Tuned 1 | 0.7301 | 0.2429 | 0.6254 | 0.3499 | 0.7521 |
| Random Forest Tuned 2 | 0.7696 | 0.2645 | 0.5524 | 0.3577 | 0.7516 |
| Random Forest Tuned 3 | 0.8112 | 0.2983 | 0.4625 | 0.3627 | 0.7517 |
| Random Forest Tuned 4 | 0.8452 | 0.3417 | 0.3593 | 0.3502 | 0.7515 |
| Random Forest Tuned 5 | 0.8663 | 0.3891 | 0.2655 | 0.3156 | 0.7504 |

The best tuned model was:

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

It had the best validation F1-score.

---

## 9. Final Model Evaluation

The final model was evaluated on the test set.

| Metric | Value |
|---|---:|
| Accuracy | 0.8126 |
| Precision | 0.3029 |
| Recall | 0.4719 |
| F1-score | 0.3690 |
| ROC-AUC | 0.7571 |

Confusion matrix:

```text
[[29025  4830]
 [ 2349  2099]]
```

Interpretation:

- 29,025 borrowers were correctly predicted as No Default.
- 4,830 borrowers were wrongly flagged as Default.
- 2,349 actual default cases were missed.
- 2,099 actual default cases were correctly identified.

The model caught 2,099 out of 4,448 actual default cases.

---

## 10. Threshold Strategy

The model returns a default probability. A threshold decides when that probability becomes a `Default` prediction.

Several thresholds were tested.

The selected threshold is:

```text
0.50
```

Reason:

- It had the best F1-score.
- It gave the best balance between precision and recall.

A lower threshold catches more default cases but creates many false positives. A higher threshold reduces false positives but misses more real defaults.

---

## 11. Feature Importance

The final Random Forest model relied most on these features:

- Age
- InterestRate
- Income
- LoanAmount
- MonthsEmployed
- CreditScore
- DTIRatio
- LoanTerm
- NumCreditLines

These features are also meaningful from a lending perspective and match the SQL/EDA patterns.

Feature importance helps explain the model, but it does not prove direct cause and effect.

---

## 12. Deployment

A FastAPI prediction endpoint was created.

The API returns:

- prediction
- prediction label
- default probability
- risk category

The API includes:

- numerical validation
- categorical validation
- null handling through the preprocessing pipeline

Example response:

```json
{
  "prediction": 1,
  "prediction_label": "Default",
  "default_probability": 0.5262,
  "risk_category": "Medium"
}
```

---

## 13. Testing and Logging

Basic tests were added with `pytest`.

The tests cover:

- data cleaning
- prediction output
- model file existence
- API health endpoint
- valid API requests
- invalid API inputs

Current result:

```text
8 passed
```

Basic logging was also added for prediction activity. Logs are saved in:

```text
logs/prediction.log
```

---

## 14. Limitations

The model has several limitations:

- The dataset is imbalanced.
- Precision for default predictions is still low.
- Some actual default cases are missed.
- The dataset is public and not real bank production data.
- Fairness and bias checks were not included.
- Production monitoring was not implemented.

The model should be used as a decision-support tool, not as the only basis for loan approval decisions.

---

## 15. Future Improvements

Possible improvements:

- Add MLflow tracking
- Add deeper hyperparameter tuning
- Add SHAP explanations
- Add Docker support
- Add GitHub Actions
- Add fairness and bias analysis
- Add production-style monitoring
- Improve threshold strategy based on business cost

---

## 16. Final Conclusion

This project built a complete loan default prediction workflow.

It includes SQL exploration, data preparation, EDA, model comparison, model tuning, threshold analysis, feature importance, FastAPI deployment, testing, and logging.

The final selected model was Random Forest Tuned 3. It achieved the best validation F1-score and produced a balanced final test result compared with the other tested models.

The model is not perfect, but it is a solid first version of a practical loan default risk prediction system.