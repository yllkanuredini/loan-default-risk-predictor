# EDA Insights

The EDA confirmed that the dataset is imbalanced:

- No Default: 88.39%
- Default: 11.61%

This means accuracy alone is not enough, so precision, recall, F1-score, ROC-AUC, and the confusion matrix are also used.

Main patterns found during EDA:

- Unemployed borrowers had a higher default rate.
- Lower-income borrowers defaulted more often.
- Higher interest rates were linked with higher default risk.
- Larger loan amounts were linked with higher default risk.
- Borrowers without a co-signer had a higher default rate.
- Borrowers without a mortgage also showed higher default risk.

The correlation matrix showed that Age, Income, MonthsEmployed, InterestRate, LoanAmount, and CreditScore had useful relationships with the target.

These findings support using borrower and loan features to predict default risk, while keeping in mind that correlation does not prove causation.