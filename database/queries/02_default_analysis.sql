USE LoanDefaultRiskDB;
GO

-- 1. Overall default rate
SELECT
    COUNT(*) AS total_records,
    SUM(CASE WHEN [Default] = 1 THEN 1 ELSE 0 END) AS default_records,
    CAST(SUM(CASE WHEN [Default] = 1 THEN 1 ELSE 0 END) * 100.0 / COUNT(*) AS DECIMAL(10, 2)) AS default_rate_percentage
FROM loan_default_raw;


-- 2. Default rate by employment type
SELECT
    EmploymentType,
    COUNT(*) AS total_records,
    SUM(CASE WHEN [Default] = 1 THEN 1 ELSE 0 END) AS default_records,
    CAST(SUM(CASE WHEN [Default] = 1 THEN 1 ELSE 0 END) * 100.0 / COUNT(*) AS DECIMAL(10, 2)) AS default_rate_percentage
FROM loan_default_raw
GROUP BY EmploymentType
ORDER BY default_rate_percentage DESC;


-- 3. Default rate by education level
SELECT
    Education,
    COUNT(*) AS total_records,
    SUM(CASE WHEN [Default] = 1 THEN 1 ELSE 0 END) AS default_records,
    CAST(SUM(CASE WHEN [Default] = 1 THEN 1 ELSE 0 END) * 100.0 / COUNT(*) AS DECIMAL(10, 2)) AS default_rate_percentage
FROM loan_default_raw
GROUP BY Education
ORDER BY default_rate_percentage DESC;


-- 4. Default rate by marital status
SELECT
    MaritalStatus,
    COUNT(*) AS total_records,
    SUM(CASE WHEN [Default] = 1 THEN 1 ELSE 0 END) AS default_records,
    CAST(SUM(CASE WHEN [Default] = 1 THEN 1 ELSE 0 END) * 100.0 / COUNT(*) AS DECIMAL(10, 2)) AS default_rate_percentage
FROM loan_default_raw
GROUP BY MaritalStatus
ORDER BY default_rate_percentage DESC;


-- 5. Default rate by loan purpose
SELECT
    LoanPurpose,
    COUNT(*) AS total_records,
    SUM(CASE WHEN [Default] = 1 THEN 1 ELSE 0 END) AS default_records,
    CAST(SUM(CASE WHEN [Default] = 1 THEN 1 ELSE 0 END) * 100.0 / COUNT(*) AS DECIMAL(10, 2)) AS default_rate_percentage
FROM loan_default_raw
GROUP BY LoanPurpose
ORDER BY default_rate_percentage DESC;


-- 6. Default rate by mortgage status
SELECT
    HasMortgage,
    COUNT(*) AS total_records,
    SUM(CASE WHEN [Default] = 1 THEN 1 ELSE 0 END) AS default_records,
    CAST(SUM(CASE WHEN [Default] = 1 THEN 1 ELSE 0 END) * 100.0 / COUNT(*) AS DECIMAL(10, 2)) AS default_rate_percentage
FROM loan_default_raw
GROUP BY HasMortgage
ORDER BY default_rate_percentage DESC;


-- 7. Default rate by dependent status
SELECT
    HasDependents,
    COUNT(*) AS total_records,
    SUM(CASE WHEN [Default] = 1 THEN 1 ELSE 0 END) AS default_records,
    CAST(SUM(CASE WHEN [Default] = 1 THEN 1 ELSE 0 END) * 100.0 / COUNT(*) AS DECIMAL(10, 2)) AS default_rate_percentage
FROM loan_default_raw
GROUP BY HasDependents
ORDER BY default_rate_percentage DESC;


-- 8. Default rate by co-signer status
SELECT
    HasCoSigner,
    COUNT(*) AS total_records,
    SUM(CASE WHEN [Default] = 1 THEN 1 ELSE 0 END) AS default_records,
    CAST(SUM(CASE WHEN [Default] = 1 THEN 1 ELSE 0 END) * 100.0 / COUNT(*) AS DECIMAL(10, 2)) AS default_rate_percentage
FROM loan_default_raw
GROUP BY HasCoSigner
ORDER BY default_rate_percentage DESC;