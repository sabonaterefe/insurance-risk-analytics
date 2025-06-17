Insurance Risk Analytics & Pricing System
A complete end-to-end analytics pipeline for assessing insurance risk and developing a dynamic, data-driven premium optimization strategy.

Project Objective
Design a robust analytical framework to:

Statistically validate key risk factors

Predict claim severity and claim probability

Build risk-based premium models with interpretable insights

Provide actionable recommendations for segmentation and pricing

Tasks Overview
Task 1–2: Data Preparation & Exploration
Cleaned and validated large-scale insurance policy data

Created derived features such as claim frequency, severity, margin, and loss ratio

Visualized distributions and trends by province, gender, zip code, vehicle type, and more

Task 3: A/B Hypothesis Testing
Formally tested hypotheses on geographic and demographic risk factors

Applied t-tests, z-tests, and chi-squared tests

Rejected key null hypotheses with statistical evidence (e.g. risk disparity across provinces and genders)

Delivered interpretable business implications and segmentation recommendations

Task 4: Modeling & Risk-Based Pricing
Built models for:

Claim severity (XGBoost)

Claim probability (Random Forest)

Premium optimization (Random Forest)

Evaluated performance using RMSE, R², and AUC

Interpreted models with SHAP to explain the top 10 most influential features

Generated SHAP plots for transparency and regulatory alignment

 Directory Structure
├── 01_data/               # Raw & processed datasets
├── 02_stat_testing/       # Statistical analysis scripts (Task 3)
├── 03_modeling/           # Modeling code (Task 4)
├── notebooks/             # Exploration, EDA, testing & modeling reports
├── reports/figures/       # Visual outputs (e.g. SHAP plots)
├── requirements.txt       # Python dependencies
Technical Stack
Python (pandas, numpy, matplotlib, seaborn)

scikit-learn, XGBoost, SHAP

Jupyter Notebooks for iterative analysis

Git & GitHub for version control

DVC (optional) for data versioning and pipeline reproducibility

Key Business Insight
Gauteng province demonstrates a 15% higher loss ratio than Western Cape (p < 0.01), suggesting a regional premium uplift may be warranted.

Vehicle age, margin, and insured sum are the most predictive features in claim severity—offering clear leverage points for pricing adjustment.
 Next Steps
Integrate cost structure assumptions for finalized premium recommendations

Explore policy renewal prediction and customer retention modeling

Connect to live quote systems for end-to-end automation
