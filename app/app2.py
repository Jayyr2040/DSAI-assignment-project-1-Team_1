import streamlit as st
import pandas as pd
import plotly.express as px

# --- PAGE CONFIG ---
st.set_page_config(page_title="Recruitment Intelligence Pro", layout="wide")

# --- LOAD DATA ---
@st.cache_data
def load_data():
    # Load your newly cleaned 'Gold Standard' dataset
    df = pd.read_csv('app/Final_Cleaned_SG_Jobs.csv')
    
    # Calculate Estimated Commission based on Singaporean Market Norms (15-25%)
    # Using 20% as a standard baseline for professional roles
    # df['est_commission'] = df['monthly_pay'] * 12 * 0.20
    
    # 1. Convert to Datetime
    df['metadata_newPostingDate'] = pd.to_datetime(df['metadata_newPostingDate'])
    df['metadata_expiryDate'] = pd.to_datetime(df['metadata_expiryDate'])
    
    # 2. Define "Today" based on the freshest data in your file
    today_ref = df['metadata_newPostingDate'].max()
    
    # 3. Apply the "Recency" and "Expiry" Filters
    # Only roles posted in the last 60 days AND not yet expired
    mask = (df['metadata_newPostingDate'] >= (today_ref - pd.Timedelta(days=60))) & \
           (df['metadata_expiryDate'] >= today_ref)
    
    df = df[mask].copy()
    
    # 4. Deduplicate (The most important step to stop double-counting!)
    # If same company has same title and pay, it's usually the same lead
    df = df.drop_duplicates(subset=['clean_company', 'clean_title', 'monthly_pay'])
    
    return df

df = load_data()

# --- SIDEBAR FILTERS ---
st.sidebar.header("Intelligence Filters")

# Expanded list to catch specific high-volume agencies appearing in your Top 10
agency_keywords = [
   'RECRUIT', 'MANPOWER', 'PERSONNEL', 'TALENT', 'ADVISORY', 
    'CONSULTANT', 'SEARCH', 'AGENCY', 'EMPLOYMENT', 'CAREER', 
    'SERVICES', 'STAFFING', 'JOBS', 'RESOURCE', 'CONSULTING', 
    'SOLUTIONS', 'HR', 'HUMAN RESOURCE', 'HEADHUNTER',
    'ANRADUS', 'PERSOLKELLY', 'RANDSTAD', 'ADECCO', 'FLINTEX', 
    'ZENITH', 'MTC', 'HYPERSCAL', 'MICHAEL PAGE', 'SCIENTEC',
    'MORGAN MCKINLEY', 'AMBITION GROUP', 'GOOD JOB CREATIONS', 
    'GMP TECHNOLOGIES', 'BEATHCHAPMAN', 'PEOPLE PROFILERS',
    'ROBERT HALF', 'PROSTAFF', 'EAMES', 'PASONA', 'WECRUIT', 
    'STAFFKING', 'ACCEO', 'ELITEZ', 'DYNAMIC HUMAN CAPITAL',
     'PERSOLKELLY',
]


filter_agencies = st.sidebar.checkbox("Exclude Recruitment Competitors", value=True)

if filter_agencies:
    # Use 'clean_company' from your Gold Standard script
    display_df = df[~df['clean_company'].str.contains('|'.join(agency_keywords), case=False, na=False)]
else:
    display_df = df

# Filter by Business Tiers (The new tiers you created: Junior, Mid, Senior, C-Suite)
selected_tier = st.sidebar.multiselect("Select Talent Tiers", options=display_df['business_tier'].unique())
if selected_tier:
    display_df = display_df[display_df['business_tier'].isin(selected_tier)]

# --- MAIN DASHBOARD ---
st.title("Singapore Recruitment ROI Dashboard")
st.caption("🚀 Analyzed based on active roles posted within the last 60 days to ensure lead freshness.")
st.markdown("### Strategic Intelligence for Headhunters & BD Teams")

# 1. TOP METRICS
total_comm = display_df['est_commission'].sum()
avg_monthly = display_df['monthly_pay'].mean() # Uses your normalized pay
open_leads = len(display_df)

col1, col2, col3 = st.columns(3)
col1.metric("Total Commission Pool", f"${total_comm / 1e9:.2f}B")
col2.metric("Avg Monthly Pay", f"${avg_monthly:,.0f}")
# Calculate the date range for the tooltip
start_date = df['metadata_newPostingDate'].min().strftime('%d %b')
end_date = df['metadata_newPostingDate'].max().strftime('%d %b %Y')
col3.metric("Live Market Leads", f"{open_leads:,}", help=f"Only including roles marked as Open or Re-open ({start_date} - {end_date})")

st.divider()

# 2. Talent tier Revenue & TOP DIRECT client CHARTS
c1, c2 = st.columns(2)

with c1:
    st.subheader("Revenue Potential by Talent Tier")
    # Define the professional order for the chart
    tier_order = ['C-Suite', 'Senior / Managerial', 'Mid-Level', 'Junior / Entry']
    
    tier_data = display_df.groupby('business_tier')['est_commission'].sum().reset_index()
    
    # 3. Create the Horizontal Bar Chart
    fig_tier = px.bar(
        tier_data, 
        x='est_commission', 
        y='business_tier', 
        orientation='h',
        color='est_commission',
        # Use 'Viridis' or 'GnBu' to match the professional look of your sector chart
        color_continuous_scale='Viridis', 
        category_orders={"business_tier": tier_order}, 
        text_auto='.2s',
        labels={'est_commission': 'Potential Revenue ($)', 'business_tier': 'Career Tier'}
    )

    # 4. Polish the layout
    fig_tier.update_layout(
        xaxis_tickformat='$,.0f',
        showlegend=False,
        height=400,
        margin=dict(l=0, r=0, t=30, b=0),
        yaxis_title=None
    )

    st.plotly_chart(fig_tier, use_container_width=True)

# 2.1 Sector Tier revenue
with c2:
    st.subheader("Top Direct Client Hitlist")
    # Grouping by consolidated 'clean_company' names
    company_data = display_df.groupby('clean_company')['est_commission'].sum().sort_values(ascending=False).head(10).reset_index()
    # 1. Title Case the company names (e.g., TIKTOK -> Tiktok)
    company_data['clean_company'] = company_data['clean_company'].str.title()
    company_data['est_commission'] = company_data['est_commission'].map('${:,.0f}'.format)
    # 2. Rename columns for a professional look
    company_data.columns = ['Target Company', 'Total Potential Commission']
   
    st.dataframe(company_data, use_container_width=True, hide_index=True)

st.divider() # Adds a nice visual break
# --- NEW STRATEGIC SECTOR VIEW ---
st.subheader("🎯 Sector Intelligence: Where the Money Is")

# 1. Group and process the data
# Use 'clean_category' (the one you extracted in SQL)
sector_data = display_df.groupby('clean_category')['est_commission'].sum().sort_values(ascending=False).head(10).reset_index()

# 2. Create a horizontal bar chart for high readability
fig_sector = px.bar(
    sector_data, 
    x='est_commission', 
    y='clean_category', 
    orientation='h',
    color='est_commission',
    color_continuous_scale='GnBu', # Professional Green-Blue scale
    text_auto='.2s',
    labels={'est_commission': 'Potential Revenue ($)', 'clean_category': 'Industry Sector'}
)

# 3. Polish the layout
fig_sector.update_layout(
    yaxis={'categoryorder':'total ascending'}, # Puts highest revenue at the top
    showlegend=False,
    height=500, 
    xaxis_tickformat='$,.0f'
)

st.plotly_chart(fig_sector, use_container_width=True)

# --- 3. DATA DRILL-DOWN (FINAL POLISH FOR VISIBILITY) ---
st.subheader("🔍 Strategic Lead Explorer")

if not display_df.empty:
    # 1. Select the columns
    search_df = display_df[['clean_company', 'clean_title', 'business_tier', 'monthly_pay', 'est_commission', 'job_status']].head(100).copy()

    # 2. BEAUTY CLEAN: Explicitly convert to string to ensure visibility in the table
    # This removes extra info like "| junior" or "- west" and ensures the text is "solid"
    search_df['clean_title'] = search_df['clean_title'].astype(str).str.split('|').str[0]
    search_df['clean_title'] = search_df['clean_title'].str.split('-').str[0]
    search_df['clean_title'] = search_df['clean_title'].str.replace(r'\$?[\d,]+.*', '', regex=True)
    search_df['clean_title'] = search_df['clean_title'].str.replace('up to', '', case=False)
    search_df['clean_title'] = search_df['clean_title'].str.strip().str.title() # .title() makes it "Software Engineer" instead of "software engineer"

    # 3. Rename columns for the UI
    search_df.columns = ['Target Company', 'Verified Role', 'Career Tier', 'Monthly Pay', 'Est. Commission', 'Status']

    # 4. Format currency
    search_df['Monthly Pay'] = search_df['Monthly Pay'].map('${:,.0f}'.format)
    search_df['Est. Commission'] = search_df['Est. Commission'].map('${:,.0f}'.format)

    # 5. Display
    st.dataframe(search_df, use_container_width=True, hide_index=True)
else:
    st.warning("No leads found matching the selected filters.")



