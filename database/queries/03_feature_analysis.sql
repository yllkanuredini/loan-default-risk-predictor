USE LoanDefaultRiskDB;
GO

-- 1. Default rate by age group
SELECT
    CASE
        WHEN Age < 25 THEN 'Under 25'
        WHEN Age BETWEEN 25 AND 34 THEN '25-34'
        WHEN Age BETWEEN 35 AND 44 THEN '35-44'
        WHEN Age BETWEEN 45 AND 54 THEN '45-54'
        WHEN Age BETWEEN 55 AND 64 THEN '55-64'
        ELSE '65+'
    END AS age_group,
    COUNT(*) AS total_records,
    SUM(CASE WHEN [Default] = 1 THEN 1 ELSE 0 END) AS default_records,
    CAST(SUM(CASE WHEN [Default] = 1 THEN 1 ELSE 0 END) * 100.0 / COUNT(*) AS DECIMAL(10, 2)) AS default_rate_percentage
FROM loan_default_raw
GROUP BY
    CASE
        WHEN Age < 25 THEN 'Under 25'
        WHEN Age BETWEEN 25 AND 34 THEN '25-34'
        WHEN Age BETWEEN 35 AND 44 THEN '35-44'
        WHEN Age BETWEEN 45 AND 54 THEN '45-54'
        WHEN Age BETWEEN 55 AND 64 THEN '55-64'
        ELSE '65+'
    END
ORDER BY default_rate_percentage DESC;


-- 2. Default rate by income range
SELECT
    CASE
        WHEN Income < 30000 THEN 'Under 30k'
        WHEN Income BETWEEN 30000 AND 59999 THEN '30k-59k'
        WHEN Income BETWEEN 60000 AND 89999 THEN '60k-89k'
        WHEN Income BETWEEN 90000 AND 119999 THEN '90k-119k'
        ELSE '120k+'
    END AS income_range,
    COUNT(*) AS total_records,
    SUM(CASE WHEN [Default] = 1 THEN 1 ELSE 0 END) AS default_records,
    CAST(SUM(CASE WHEN [Default] = 1 THEN 1 ELSE 0 END) * 100.0 / COUNT(*) AS DECIMAL(10, 2)) AS default_rate_percentage
FROM loan_default_raw
GROUP BY
    CASE
        WHEN Income < 30000 THEN 'Under 30k'
        WHEN Income BETWEEN 30000 AND 59999 THEN '30k-59k'
        WHEN Income BETWEEN 60000 AND 89999 THEN '60k-89k'
        WHEN Income BETWEEN 90000 AND 119999 THEN '90k-119k'
        ELSE '120k+'
    END
ORDER BY default_rate_percentage DESC;


-- 3. Default rate by credit score range
SELECT
    CASE
        WHEN CreditScore < 500 THEN 'Below 500'
        WHEN CreditScore BETWEEN 500 AND 599 THEN '500-599'
        WHEN CreditScore BETWEEN 600 AND 699 THEN '600-699'
        WHEN CreditScore BETWEEN 700 AND 799 THEN '700-799'
        ELSE '800+'
    END AS credit_score_range,
    COUNT(*) AS total_records,
    SUM(CASE WHEN [Default] = 1 THEN 1 ELSE 0 END) AS default_records,
    CAST(SUM(CASE WHEN [Default] = 1 THEN 1 ELSE 0 END) * 100.0 / COUNT(*) AS DECIMAL(10, 2)) AS default_rate_percentage
FROM loan_default_raw
GROUP BY
    CASE
        WHEN CreditScore < 500 THEN 'Below 500'
        WHEN CreditScore BETWEEN 500 AND 599 THEN '500-599'
        WHEN CreditScore BETWEEN 600 AND 699 THEN '600-699'
        WHEN CreditScore BETWEEN 700 AND 799 THEN '700-799'
        ELSE '800+'
    END
ORDER BY default_rate_percentage DESC;


-- 4. Default rate by loan amount range
SELECT
    CASE
        WHEN LoanAmount < 50000 THEN 'Under 50k'
        WHEN LoanAmount BETWEEN 50000 AND 99999 THEN '50k-99k'
        WHEN LoanAmount BETWEEN 100000 AND 149999 THEN '100k-149k'
        WHEN LoanAmount BETWEEN 150000 AND 199999 THEN '150k-199k'
        ELSE '200k+'
    END AS loan_amount_range,
    COUNT(*) AS total_records,
    SUM(CASE WHEN [Default] = 1 THEN 1 ELSE 0 END) AS default_records,
    CAST(SUM(CASE WHEN [Default] = 1 THEN 1 ELSE 0 END) * 100.0 / COUNT(*) AS DECIMAL(10, 2)) AS default_rate_percentage
FROM loan_default_raw
GROUP BY
    CASE
        WHEN LoanAmount < 50000 THEN 'Under 50k'
        WHEN LoanAmount BETWEEN 50000 AND 99999 THEN '50k-99k'
        WHEN LoanAmount BETWEEN 100000 AND 149999 THEN '100k-149k'
        WHEN LoanAmount BETWEEN 150000 AND 199999 THEN '150k-199k'
        ELSE '200k+'
    END
ORDER BY default_rate_percentage DESC;


-- 5. Default rate by interest rate range
SELECT
    CASE
        WHEN InterestRate < 10 THEN 'Under 10%'
        WHEN InterestRate BETWEEN 10 AND 14.99 THEN '10%-14.99%'
        WHEN InterestRate BETWEEN 15 AND 19.99 THEN '15%-19.99%'
        ELSE '20%+'
    END AS interest_rate_range,
    COUNT(*) AS total_records,
    SUM(CASE WHEN [Default] = 1 THEN 1 ELSE 0 END) AS default_records,
    CAST(SUM(CASE WHEN [Default] = 1 THEN 1 ELSE 0 END) * 100.0 / COUNT(*) AS DECIMAL(10, 2)) AS default_rate_percentage
FROM loan_default_raw
GROUP BY
    CASE
        WHEN InterestRate < 10 THEN 'Under 10%'
        WHEN InterestRate BETWEEN 10 AND 14.99 THEN '10%-14.99%'
        WHEN InterestRate BETWEEN 15 AND 19.99 THEN '15%-19.99%'
        ELSE '20%+'
    END
ORDER BY default_rate_percentage DESC;