# Business Analytics Project Datasets

These are synthetic datasets created for the multi-part Business Analytics and Machine Learning project. They are intentionally designed to be realistic enough for data cleaning, EDA, feature engineering, modeling, and business recommendations.

## Files

1. `part_1_ecommerce_customer_segmentation.csv`
   - Use for customer segmentation using RFM and K-Means clustering.
   - Contains transaction-level e-commerce data with invoices, products, quantities, prices, customers, and countries.
   - Includes intentional data quality issues: missing customer IDs, missing descriptions, cancelled invoices, negative quantities, zero/negative prices, and duplicates.

2. `part_2_market_basket_analysis.csv`
   - Use for association rule mining and market basket analysis.
   - Contains transaction-product rows suitable for converting into basket format.
   - Includes product co-occurrence patterns useful for support, confidence, and lift analysis.

3. `part_3_customer_churn_prediction.csv`
   - Use for churn classification.
   - Contains telecom-style customer demographics, services, billing, contract, payment, and churn status.
   - Includes a few missing `TotalCharges` values for preprocessing practice.

4. `part_4_marketing_budget_optimization.csv`
   - Use for multiple linear regression and marketing budget analysis.
   - Contains campaign-level spends across TV, radio, social media, search ads, and influencer marketing, with sales revenue as the target.
   - Includes some missing values and outliers.

5. `part_5_customer_ltv_prediction.csv`
   - Use for customer lifetime value analysis and future spending prediction.
   - Contains customer demographics, engagement, purchase behavior, loyalty tier, returns, cancellations, and future spending target.
   - Includes a few missing values for cleaning practice.

## Suggested README Dataset Source Text for Students

Dataset Source: Synthetic dataset provided as part of the project assignment for academic use.

## Notes

- These datasets are not real customer/company data.
- Students should not assume the data represents any real business.
- Students are expected to perform cleaning and justify their choices.
- Each project part should use only the dataset relevant to that part.
