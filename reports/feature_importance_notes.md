# Feature Importance Notes

Feature importance was used to understand which inputs the final Random Forest model relied on most.

Top important features included:

- Age
- InterestRate
- Income
- LoanAmount
- MonthsEmployed
- CreditScore
- DTIRatio
- LoanTerm
- NumCreditLines

Most of the strongest features were numerical borrower and loan-related variables.

The results are consistent with the SQL and EDA findings: default risk was higher for younger borrowers, lower-income borrowers, borrowers with higher interest rates, larger loan amounts, fewer months employed, and lower credit scores.

Feature importance helps explain the model, but it does not prove that a feature directly causes default.