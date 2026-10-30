-- =========================================================
-- Churn Analytics and Business Intelligence Queries
-- Database: SQLite (Telco Churn Dataset)
-- =========================================================

-- 1. Churn Rate Percentage by Contract Type
SELECT
    Contract,
    COUNT(*) AS total_customers,
    SUM(Churn_flag) AS churn_count,
    ROUND(AVG(Churn_flag) * 100, 2) AS churn_pct
FROM customers
GROUP BY Contract
ORDER BY churn_pct DESC;

-- 2. Churn Drivers: Payment Methods vs. Autopay
SELECT
    PaymentMethod,
    COUNT(*) AS total_customers,
    SUM(Churn_flag) AS churn_count,
    ROUND(AVG(Churn_flag) * 100, 2) AS churn_pct
FROM customers
GROUP BY PaymentMethod
ORDER BY churn_pct DESC;

-- 3. Top High-Revenue Risk Segments (Fiber Optic & Month-to-Month Contract)
SELECT
    Contract,
    InternetService,
    COUNT(*) AS total_customers,
    ROUND(SUM(MonthlyCharges), 2) AS total_monthly_revenue,
    ROUND(AVG(Churn_flag) * 100, 2) AS churn_pct
FROM customers
GROUP BY Contract, InternetService
HAVING total_customers > 10
ORDER BY churn_pct DESC;

-- 4. Revenue Leakage from Existing Lost Churners
SELECT
    Contract,
    COUNT(*) AS churned_customers,
    ROUND(SUM(MonthlyCharges), 2) AS monthly_revenue_loss,
    ROUND(SUM(TotalCharges), 2) AS cumulative_lifetime_loss
FROM customers
WHERE Churn_flag = 1
GROUP BY Contract
ORDER BY monthly_revenue_loss DESC;