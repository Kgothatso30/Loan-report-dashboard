import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# Page config
st.set_page_config(page_title="Loan Report Dashboard", layout="wide")

# Title
st.title("🏦 Loan Report Dashboard")
st.markdown("*Comprehensive analysis of loan distribution, applicant income, and borrower characteristics*")

# Load data
@st.cache_data
def load_data():
    return pd.read_csv('loan_data.csv')

df = load_data()

# --- SIDEBAR FILTERS ---
st.sidebar.header("🔍 Filter Dashboard")

# Loan status filter
status_filter = st.sidebar.multiselect(
    "Loan Status",
    options=df['loan_status'].unique(),
    default=df['loan_status'].unique()
)

# Loan purpose filter
purpose_filter = st.sidebar.multiselect(
    "Loan Purpose",
    options=df['loan_purpose'].unique(),
    default=df['loan_purpose'].unique()
)

# Income category filter
income_filter = st.sidebar.multiselect(
    "Income Category",
    options=df['income_category'].unique(),
    default=df['income_category'].unique()
)

# Apply filters
filtered_df = df[
    df['loan_status'].isin(status_filter) & 
    df['loan_purpose'].isin(purpose_filter) &
    df['income_category'].isin(income_filter)
]

# --- KPI CARDS ---
col1, col2, col3, col4 = st.columns(4)

with col1:
    total_loan_amount = filtered_df['loan_amount'].sum()
    st.metric(
        "💰 Total Loan Amount",
        f"R{total_loan_amount:,.0f}",
        delta=f"{total_loan_amount/1000:.1f}K"
    )

with col2:
    avg_loan = filtered_df['loan_amount'].mean()
    st.metric(
        "📊 Avg Loan Amount",
        f"R{avg_loan:,.0f}",
        delta=f"{avg_loan:,.0f}"
    )

with col3:
    total_loans = len(filtered_df)
    st.metric(
        "📋 Total Loans",
        f"{total_loans:,}",
        delta=f"{len(filtered_df) - len(df):+}" if len(filtered_df) != len(df) else None
    )

with col4:
    approval_rate = (filtered_df['loan_status'] == 'Approved').mean() * 100
    st.metric(
        "✅ Approval Rate",
        f"{approval_rate:.1f}%",
        delta="Good" if approval_rate > 50 else "Low",
        delta_color="normal" if approval_rate > 50 else "inverse"
    )

st.divider()

# --- CHARTS ---
col1, col2 = st.columns(2)

with col1:
    # Loan Amount by Purpose
    loan_by_purpose = filtered_df.groupby('loan_purpose')['loan_amount'].sum().reset_index()
    loan_by_purpose = loan_by_purpose.sort_values('loan_amount', ascending=False)
    fig_purpose = px.bar(
        loan_by_purpose,
        x='loan_purpose',
        y='loan_amount',
        title='💰 Loan Amount by Purpose',
        color='loan_purpose',
        color_discrete_sequence=px.colors.qualitative.Set2,
        labels={'loan_purpose': 'Purpose', 'loan_amount': 'Total Loan Amount (R)'}
    )
    st.plotly_chart(fig_purpose, use_container_width=True)

with col2:
    # Loan Status Distribution
    status_counts = filtered_df['loan_status'].value_counts().reset_index()
    status_counts.columns = ['Status', 'Count']
    colors = {'Approved': '#2ecc71', 'Rejected': '#e74c3c', 'Pending': '#f39c12'}
    fig_status = px.pie(
        status_counts,
        values='Count',
        names='Status',
        title='📊 Loan Status Distribution',
        color='Status',
        color_discrete_map=colors
    )
    fig_status.update_traces(textposition='inside', textinfo='percent+label')
    st.plotly_chart(fig_status, use_container_width=True)

# --- ROW 2 ---
col1, col2 = st.columns(2)

with col1:
    # Income vs Loan Amount
    fig_income_loan = px.scatter(
        filtered_df,
        x='annual_income',
        y='loan_amount',
        color='loan_status',
        title='📈 Income vs Loan Amount',
        labels={'annual_income': 'Annual Income (R)', 'loan_amount': 'Loan Amount (R)'},
        color_discrete_map={'Approved': '#2ecc71', 'Rejected': '#e74c3c', 'Pending': '#f39c12'},
        opacity=0.6
    )
    st.plotly_chart(fig_income_loan, use_container_width=True)

with col2:
    # Loan Amount by Employment Type
    loan_by_employment = filtered_df.groupby('employment_type')['loan_amount'].mean().reset_index()
    loan_by_employment = loan_by_employment.sort_values('loan_amount', ascending=False)
    fig_employment = px.bar(
        loan_by_employment,
        x='employment_type',
        y='loan_amount',
        title='💼 Average Loan by Employment Type',
        color='employment_type',
        color_discrete_sequence=px.colors.qualitative.Pastel,
        labels={'employment_type': 'Employment Type', 'loan_amount': 'Avg Loan Amount (R)'}
    )
    st.plotly_chart(fig_employment, use_container_width=True)

# --- ROW 3 ---
col1, col2 = st.columns(2)

with col1:
    # Credit Score Distribution
    fig_credit = px.histogram(
        filtered_df,
        x='credit_score',
        color='loan_status',
        title='📊 Credit Score Distribution',
        labels={'credit_score': 'Credit Score', 'count': 'Number of Applicants'},
        color_discrete_map={'Approved': '#2ecc71', 'Rejected': '#e74c3c', 'Pending': '#f39c12'},
        nbins=30
    )
    st.plotly_chart(fig_credit, use_container_width=True)

with col2:
    # Loan Amount by Education Level
    loan_by_education = filtered_df.groupby('education_level')['loan_amount'].mean().reset_index()
    loan_by_education = loan_by_education.sort_values('loan_amount', ascending=False)
    fig_education = px.bar(
        loan_by_education,
        x='education_level',
        y='loan_amount',
        title='🎓 Average Loan by Education Level',
        color='education_level',
        color_discrete_sequence=px.colors.sequential.Blues_r,
        labels={'education_level': 'Education Level', 'loan_amount': 'Avg Loan Amount (R)'}
    )
    st.plotly_chart(fig_education, use_container_width=True)

# --- ROW 4: Correlation Heatmap ---
st.subheader("📈 Key Metrics Correlation")

correlation_cols = ['annual_income', 'loan_amount', 'interest_rate', 'credit_score', 'debt_to_income_ratio']
correlation_df = filtered_df[correlation_cols].corr()

fig_corr = px.imshow(
    correlation_df,
    text_auto=True,
    aspect="auto",
    color_continuous_scale='RdBu_r',
    title="Metric Correlations"
)
st.plotly_chart(fig_corr, use_container_width=True)

# --- RAW DATA ---
with st.expander("📊 View Raw Loan Data"):
    st.dataframe(filtered_df.head(100))

# --- SUMMARY STATISTICS ---
with st.expander("📈 Summary Statistics"):
    st.write("### Loan Overview")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.write("**Top 5 Loan Purposes**")
        top_purposes = filtered_df['loan_purpose'].value_counts().head(5)
        st.dataframe(top_purposes)
    
    with col2:
        st.write("**Average Loan by Gender**")
        gender_loan = filtered_df.groupby('gender')['loan_amount'].mean()
        st.dataframe(gender_loan)
    
    with col3:
        st.write("**Average Credit Score by Status**")
        credit_by_status = filtered_df.groupby('loan_status')['credit_score'].mean()
        st.dataframe(credit_by_status)