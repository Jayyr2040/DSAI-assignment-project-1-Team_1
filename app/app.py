import streamlit as st
import pandas as pd
import plotly.express as px

# --- PAGE CONFIG ---
st.set_page_config(page_title="Recruitment Intelligence Pro", layout="wide")

# --- LOAD DATA ---
@st.cache_data
def load_data():
    df = pd.read_csv('app/singapore_leads_app.csv')
    return df

df = load_data()

# --- SIDEBAR FILTERS ---
st.sidebar.header("Recruitment Intelligence Filters")

# The Competitor Filter Logic
agency_keywords = [
    'RECRUIT', 'MANPOWER', 'PERSONNEL', 'TALENT', 'ADVISORY', 
    'CONSULTANT', 'SEARCH', 'AGENCY', 'EMPLOYMENT', 'CAREER', 
    'SERVICES', 'STAFFING', 'JOBS', 'RESOURCE', 'CONSULTING', 
    'SOLUTIONS', 'HR', 'HUMAN RESOURCE', 'HEADHUNTER',
    'ANRADUS', 'PERSOLKELLY', 'RANDSTAD', 'ADECCO', 
    'MICHAEL PAGE', 'SCIENTEC', 'PEOPLE PROFILERS', 'PEOPLE PROFILERS', 'ZENITH',
    'MORGAN MCKINLEY', 'AMBITION GROUP', 'GOOD JOB CREATIONS', 
    'GMP TECHNOLOGIES', 'BEATHCHAPMAN'
]

filter_agencies = st.sidebar.checkbox("Exclude Recruitment Competitors", value=True)

if filter_agencies:
    display_df = df[~df['company'].str.contains('|'.join(agency_keywords), case=False, na=False)]
else:
    display_df = df

selected_sector = st.sidebar.multiselect("Select Target Sectors", options=display_df['sector'].unique())
if selected_sector:
    display_df = display_df[display_df['sector'].isin(selected_sector)]

# --- MAIN DASHBOARD ---
st.title("🇸🇬 Singapore Recruitment ROI Dashboard")
st.markdown("### Strategic Intelligence for Headhunters & BD Teams")

# 1. TOP METRICS
total_comm = display_df['est_commission_revenue'].sum()
avg_val = display_df['average_salary'].mean()
open_leads = len(display_df)

col1, col2, col3 = st.columns(3)
col1.metric("Total Commission Pool", f"${total_comm:,.0f}")
col2.metric("Avg Role Value", f"${avg_val:,.0f}")
col3.metric("Actionable Leads", f"{open_leads:,}")

st.divider()

# 2. CHARTS
c1, c2 = st.columns(2)

with c1:
    st.subheader("Top Sectors by Revenue Potential")
    sector_data = display_df.groupby('sector')['est_commission_revenue'].sum().sort_values(ascending=False).head(10)
    fig = px.bar(sector_data, orientation='h', color_continuous_scale='Viridis')
    st.plotly_chart(fig, use_container_width=True)

with c2:
    st.subheader("Target Company Hitlist")
    company_data = display_df.groupby('company')['est_commission_revenue'].sum().sort_values(ascending=False).head(10).reset_index()
    
    # Format the money columns
    company_data['est_commission_revenue'] = company_data['est_commission_revenue'].map('${:,.0f}'.format)
    
    # Use st.dataframe for a cleaner look than st.table
    st.dataframe(company_data, use_container_width=True, hide_index=True)

# 3. DATA DRILL-DOWN
st.subheader("Detailed Lead Search")
#st.dataframe(display_df[['company', 'title', 'talent_tier', 'average_salary', 'est_commission_revenue']].head(100))
# Format the table for the final presentation
search_df = display_df[['company', 'title', 'talent_tier', 'average_salary', 'est_commission_revenue']].head(100).copy()

# Add dollar signs and commas
search_df['average_salary'] = search_df['average_salary'].map('${:,.0f}'.format)
search_df['est_commission_revenue'] = search_df['est_commission_revenue'].map('${:,.0f}'.format)

st.dataframe(search_df, use_container_width=True, hide_index=True)