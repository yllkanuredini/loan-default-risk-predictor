# API Validation Notes

The FastAPI endpoint includes validation to prevent unrealistic input values before sending data to the model.

Numerical rules include:

- Age: 18 to 100
- CreditScore: 300 to 850
- DTIRatio: 0 to 1
- Income, LoanAmount, MonthsEmployed, NumCreditLines, InterestRate: cannot be negative
- LoanTerm: must be positive

Categorical fields only accept known dataset values, such as valid education levels, employment types, loan purposes, and Yes/No fields.

The API also accepts null values. Missing numerical values are handled with median imputation, and missing categorical values are handled with most-frequent imputation in the preprocessing pipeline.

This makes the prediction endpoint safer and closer to a real deployment setup.