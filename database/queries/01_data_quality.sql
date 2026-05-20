USE LoanDefaultRiskDB;
GO

-- 1. Count total rows
SELECT COUNT(*) AS total_rows
FROM loan_default_raw;

-- 2. Check target distribution
SELECT
    [Default],
    COUNT(*) AS total_records,
    CAST(COUNT(*) * 100.0 / SUM(COUNT(*)) OVER () AS DECIMAL(10, 2)) AS percentage
FROM loan_default_raw
GROUP BY [Default];

-- 3. Check duplicate LoanID values
SELECT
    LoanID,
    COUNT(*) AS duplicate_count
FROM loan_default_raw
GROUP BY LoanID
HAVING COUNT(*) > 1;

-- 4. Check missing values by column
SELECT
    SUM(CASE WHEN LoanID IS NULL THEN 1 ELSE 0 END) AS missing_loan_id,
    SUM(CASE WHEN Age IS NULL THEN 1 ELSE 0 END) AS missing_age,
    SUM(CASE WHEN Income IS NULL THEN 1 ELSE 0 END) AS missing_income,
    SUM(CASE WHEN LoanAmount IS NULL THEN 1 ELSE 0 END) AS missing_loan_amount,
    SUM(CASE WHEN CreditScore IS NULL THEN 1 ELSE 0 END) AS missing_credit_score,
    SUM(CASE WHEN MonthsEmployed IS NULL THEN 1 ELSE 0 END) AS missing_months_employed,
    SUM(CASE WHEN NumCreditLines IS NULL THEN 1 ELSE 0 END) AS missing_num_credit_lines,
    SUM(CASE WHEN InterestRate IS NULL THEN 1 ELSE 0 END) AS missing_interest_rate,
    SUM(CASE WHEN LoanTerm IS NULL THEN 1 ELSE 0 END) AS missing_loan_term,
    SUM(CASE WHEN DTIRatio IS NULL THEN 1 ELSE 0 END) AS missing_dti_ratio,
    SUM(CASE WHEN Education IS NULL THEN 1 ELSE 0 END) AS missing_education,
    SUM(CASE WHEN EmploymentType IS NULL THEN 1 ELSE 0 END) AS missing_employment_type,
    SUM(CASE WHEN MaritalStatus IS NULL THEN 1 ELSE 0 END) AS missing_marital_status,
    SUM(CASE WHEN HasMortgage IS NULL THEN 1 ELSE 0 END) AS missing_has_mortgage,
    SUM(CASE WHEN HasDependents IS NULL THEN 1 ELSE 0 END) AS missing_has_dependents,
    SUM(CASE WHEN LoanPurpose IS NULL THEN 1 ELSE 0 END) AS missing_loan_purpose,
    SUM(CASE WHEN HasCoSigner IS NULL THEN 1 ELSE 0 END) AS missing_has_cosigner,
    SUM(CASE WHEN [Default] IS NULL THEN 1 ELSE 0 END) AS missing_default
FROM loan_default_raw;

-- 5. Basic numerical ranges
SELECT
    MIN(Age) AS min_age,
    MAX(Age) AS max_age,
    MIN(Income) AS min_income,
    MAX(Income) AS max_income,
    MIN(LoanAmount) AS min_loan_amount,
    MAX(LoanAmount) AS max_loan_amount,
    MIN(CreditScore) AS min_credit_score,
    MAX(CreditScore) AS max_credit_score,
    MIN(InterestRate) AS min_interest_rate,
    MAX(InterestRate) AS max_interest_rate,
    MIN(DTIRatio) AS min_dti_ratio,
    MAX(DTIRatio) AS max_dti_ratio
FROM loan_default_raw;