import pandas as pd
import numpy as np
from datetime import datetime, timedelta

np.random.seed(42)

# Number of loan applications
n = 1000

# Loan purposes
loan_purposes = ['Home', 'Auto', 'Education', 'Business', 'Personal', 'Debt Consolidation']
purpose_weights = [0.25, 0.20, 0.15, 0.15, 0.15, 0.10]

# Employment types
employment_types = ['Salaried', 'Self-Employed', 'Business Owner', 'Student', 'Retired']
employment_weights = [0.40, 0.25, 0.20, 0.05, 0.10]

# Property ownership
property_ownership = ['Rented', 'Owned', 'Mortgage']
property_weights = [0.30, 0.40, 0.30]

# Loan status
loan_status = ['Approved', 'Rejected', 'Pending']
status_weights = [0.70, 0.20, 0.10]

# Generate data
data = {
    'loan_id': range(1, n+1),
    'applicant_name': [f'Applicant_{i}' for i in range(1, n+1)],
    'age': np.random.randint(21, 65, n),
    'gender': np.random.choice(['Male', 'Female'], n, p=[0.55, 0.45]),
    'marital_status': np.random.choice(['Married', 'Single', 'Divorced'], n, p=[0.55, 0.35, 0.10]),
    'dependents': np.random.choice([0, 1, 2, 3, 4], n, p=[0.20, 0.25, 0.25, 0.20, 0.10]),
    'education_level': np.random.choice(['Graduate', 'Post-Graduate', 'Under-Graduate', 'High School'], 
                                         n, p=[0.40, 0.25, 0.20, 0.15]),
    'employment_type': np.random.choice(employment_types, n, p=employment_weights),
    'employment_years': np.random.exponential(8, n).astype(int).clip(0, 35),
    'annual_income': np.random.normal(850000, 400000, n).clip(150000, 3000000).round(2),
    'loan_amount': np.random.normal(500000, 280000, n).clip(50000, 2500000).round(2),
    'loan_purpose': np.random.choice(loan_purposes, n, p=purpose_weights),
    'loan_term_months': np.random.choice([12, 24, 36, 48, 60, 84, 120], n, p=[0.05, 0.10, 0.20, 0.25, 0.25, 0.10, 0.05]),
    'interest_rate': np.random.normal(8.5, 3.5, n).clip(3, 18).round(2),
    'credit_score': np.random.normal(680, 80, n).clip(350, 850).astype(int),
    'property_ownership': np.random.choice(property_ownership, n, p=property_weights),
    'loan_status': np.random.choice(loan_status, n, p=status_weights),
    'application_date': [datetime.today() - timedelta(days=np.random.randint(0, 365)) for _ in range(n)]
}

df = pd.DataFrame(data)

# Add derived columns
df['debt_to_income_ratio'] = (df['loan_amount'] / df['annual_income'] * 100).round(2)
df['income_category'] = pd.cut(
    df['annual_income'],
    bins=[0, 30000, 60000, 100000, 200000, float('inf')],
    labels=['Low', 'Lower-Middle', 'Middle', 'Upper-Middle', 'High']
)
df['loan_status_approved'] = df['loan_status'] == 'Approved'

# Save to CSV
df.to_csv('loan_data.csv', index=False)
print("✅ loan_data.csv created with 1,000 loan records!")
print(f"📊 Total Loans: {len(df):,}")
print(f"💰 Total Loan Amount: ${df['loan_amount'].sum():,.2f}")
print(f"💰 Average Loan Amount: ${df['loan_amount'].mean():,.2f}")
print(f"✅ Approval Rate: {(df['loan_status'] == 'Approved').mean() * 100:.1f}%")