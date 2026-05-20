# SQL Exploration Insights

The dataset was loaded into SQL Server and explored using SQL queries.

Data quality checks showed:

- 255,347 records
- no duplicate LoanID values
- no missing values
- target column: Default

Target distribution:

- No Default: 88.39%
- Default: 11.61%

SQL analysis showed higher default rates for:

- unemployed borrowers
- borrowers with lower income
- borrowers with lower credit scores
- borrowers with higher interest rates
- borrowers with larger loan amounts
- borrowers without a mortgage
- borrowers without a co-signer
- business loan purposes

These results helped confirm that borrower and loan characteristics contain useful patterns for predicting default risk.

The SQL findings support the machine learning part of the project, but they should be treated as patterns, not proof of direct cause and effect.