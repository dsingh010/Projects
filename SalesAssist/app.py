"""
Claude-Powered Startup Insights + Engagement Bot
A Streamlit application for analyzing startup data and generating sales insights.
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import time
from typing import List, Dict
import io
import logging
import traceback

from sample_data import SAMPLE_STARTUPS, get_sample_data, get_startup_by_name, get_top_claude_fits
from claude_analyzer import ClaudeAnalyzer

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Page configuration
st.set_page_config(
    page_title="Claude Startup Insights Bot",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .sub-header {
        font-size: 1.5rem;
        color: #2c3e50;
        margin-bottom: 1rem;
    }
    .metric-card {
        background-color: #f8f9fa;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #1f77b4;
    }
    .chat-message {
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 0.5rem 0;
    }
    .user-message {
        background-color: #e3f2fd;
        border-left: 4px solid #2196f3;
    }
    .bot-message {
        background-color: #f3e5f5;
        border-left: 4px solid #9c27b0;
    }
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
    }
    .stTabs [data-baseweb="tab"] {
        height: 50px;
        white-space: pre-wrap;
        background-color: #f0f2f6;
        border-radius: 4px 4px 0px 0px;
        gap: 1px;
        padding-top: 10px;
        padding-bottom: 10px;
    }
    .stTabs [aria-selected="true"] {
        background-color: #1f77b4;
        color: white;
    }
</style>
""", unsafe_allow_html=True)

def load_data():
    """Load the sample startup data as a list of dictionaries."""
    # The process_data_with_claude function expects a list of dicts, not a DataFrame.
    # By returning the raw list, we avoid the ValueError and subsequent data format issues.
    return SAMPLE_STARTUPS

def get_analyzer():
    """Get or create the Claude analyzer instance."""
    try:
        # Check if analyzer already exists in session state
        if 'analyzer' not in st.session_state:
            logger.info("Creating new ClaudeAnalyzer instance")
            analyzer = ClaudeAnalyzer()
            st.session_state.analyzer = analyzer
        else:
            logger.info("Using existing ClaudeAnalyzer instance")
            analyzer = st.session_state.analyzer
        
        return analyzer
    except ValueError as e:
        logger.error(f"Configuration error: {e}")
        st.error(f"Configuration Error: {e}")
        st.info("Please create a `.env` file in your project directory with your ANTHROPIC_API_KEY.")
        st.code("ANTHROPIC_API_KEY=your_key_here")
        return None
    except Exception as e:
        logger.error(f"Failed to create analyzer: {e}")
        logger.error(f"Full traceback: {traceback.format_exc()}")
        st.error(f"Failed to initialize AI analyzer: {str(e)}")
        return None

def validate_api_configuration():
    """Validate API configuration and return status."""
    try:
        import os
        from dotenv import load_dotenv
        load_dotenv()
        
        api_key = os.getenv('ANTHROPIC_API_KEY')
        if not api_key:
            return False, "ANTHROPIC_API_KEY not found in environment variables"
        
        if api_key == "your_anthropic_api_key_here" or api_key.strip() == "":
            return False, "ANTHROPIC_API_KEY is not properly set"
        
        # Test the API key by creating a minimal client
        try:
            from anthropic import Anthropic
            client = Anthropic(api_key=api_key)
            # Try a simple test call
            response = client.messages.create(
                model="claude-3-5-sonnet-20241022",
                max_tokens=10,
                messages=[{"role": "user", "content": "Hello"}]
            )
            return True, "API key is valid and working"
        except Exception as api_error:
            return False, f"API key validation failed: {str(api_error)}"
            
    except Exception as e:
        return False, f"Configuration validation error: {str(e)}"

def parse_uploaded_file(uploaded_file):
    """Parse uploaded Excel or CSV file."""
    try:
        if uploaded_file.name.endswith('.csv'):
            df = pd.read_csv(uploaded_file)
        elif uploaded_file.name.endswith(('.xlsx', '.xls')):
            df = pd.read_excel(uploaded_file)
        else:
            st.error("Please upload a CSV or Excel file.")
            return None
        
        # Show the actual columns for debugging
        st.info(f"📊 Found columns: {list(df.columns)}")
        st.info(f"📊 Total rows: {len(df)}")
        
        # Convert DataFrame to list of dictionaries
        data = df.to_dict('records')
        
        # Map common column variations to standard names
        column_mapping = {
            'company': ['company', 'Company', 'COMPANY', 'name', 'Name', 'NAME', 'startup', 'Startup', 'STARTUP', 'Startup Name', 'startup_name'],
            'industry': ['industry', 'Industry', 'INDUSTRY', 'sector', 'Sector', 'SECTOR', 'category', 'Category', 'CATEGORY', 'Industry Vertical'],
            'business_model': ['business_model', 'Business Model', 'BUSINESS_MODEL', 'model', 'Model', 'MODEL', 'business type', 'Business Type', 'Business Type'],
            'target_audience': ['target_audience', 'Target Audience', 'TARGET_AUDIENCE', 'audience', 'Audience', 'AUDIENCE', 'customer', 'Customer', 'CUSTOMER', 'Target Market'],
            'pain_point': ['pain_point', 'Pain Point', 'PAIN_POINT', 'problem', 'Problem', 'PROBLEM', 'challenge', 'Challenge', 'CHALLENGE', 'Problem Statement', 'Pain', 'pain', 'The Problem', 'Painpoint', 'Customer Pain'],
            'solution': ['solution', 'Solution', 'SOLUTION', 'product', 'Product', 'PRODUCT', 'offering', 'Offering', 'OFFERING', 'Product Description', 'desc', 'description', 'Description', 'Company Description', 'company_description'],
        }
        
        # Standardize column names
        standardized_data = []
        discarded_rows = []
        for index, item in enumerate(data):
            standardized_item = {}
            
            # Map each field
            for standard_name, possible_names in column_mapping.items():
                value = None
                for possible_name in possible_names:
                    if possible_name in item:
                        value = item[possible_name]
                        break
                
                if value is not None:
                    # Clean the value
                    if isinstance(value, str):
                        value = value.strip()
                        if value == '' or value.lower() in ['nan', 'none', 'null']:
                            value = None
                    
                    standardized_item[standard_name] = value
                else:
                    # Set a default for any mapped column that isn't found
                    standardized_item[standard_name] = 'N/A'
            
            # Ensure a default fit score exists before AI analysis
            if 'claude_fit_score' not in standardized_item:
                standardized_item['claude_fit_score'] = 5
            
            # Only add if we have at least a company name
            if standardized_item.get('company') and standardized_item['company'] != 'N/A':
                standardized_data.append(standardized_item)
            else:
                # Keep track of the original row data for debugging
                discarded_rows.append(item)
        
        st.success(f"✅ Successfully parsed {len(standardized_data)} startups from {len(data)} rows")
        if discarded_rows:
            st.warning(f"⚠️ Discarded {len(discarded_rows)} rows. This is usually because they were empty or did not have a company name.")
            with st.expander("🔍 View Discarded Rows"):
                st.dataframe(pd.DataFrame(discarded_rows))
        
        # --- New: Add a check for mapping failures to guide the user ---
        if standardized_data:
            df_check = pd.DataFrame(standardized_data)
            original_columns = list(df.columns)
            
            # Check for columns that are critical for the app's value
            essential_columns = {
                'pain_point': 'Pain Point Addressed',
                'solution': 'Description'
            }
            
            for standard_name, display_name in essential_columns.items():
                if (df_check[standard_name] == 'N/A').all():
                    st.warning(f"""
                    **Having trouble finding the '{display_name}' column.**

                    We couldn't automatically detect this data from your file. Please ensure your spreadsheet has a column for this information.
                    
                    **The columns we found in your file are:** `{original_columns}`
                    
                    *Tip: For best results, rename your column to be one of: `Problem`, `Challenge`, `Pain Point`, `Solution`, or `Description`.*
                    """)
        
        # Show sample of parsed data for debugging
        if len(standardized_data) > 0:
            with st.expander("🔍 Sample of parsed data"):
                sample_df = pd.DataFrame(standardized_data[:3])
                st.dataframe(sample_df)
        
        return standardized_data
    except Exception as e:
        st.error(f"Error parsing file: {str(e)}")
        st.error(f"File type: {uploaded_file.name}")
        return None

def process_data_with_claude(analyzer, data):
    """
    Process the parsed data to add Claude-generated fit scores.
    This is a separate function to allow for a progress bar.
    """
    if not analyzer:
        logger.error("Analyzer is None, cannot process data")
        st.error("AI analyzer not available. Please check your API configuration.")
        return data
    
    if not data:
        logger.warning("No data provided to process")
        return []
    
    processed_data = []
    progress_bar = st.progress(0, text="Analyzing startups with Claude...")
    total_items = len(data)

    # --- New: Add a live log to see the data as it's processed ---
    log_expander = st.expander("🔬 Live Analysis Log", expanded=False)
    
    for i, item in enumerate(data):
        company_name = item.get('company', f'Startup {i+1}')
        
        with log_expander:
            st.write(f"**Analyzing {i+1}/{total_items}:** `{company_name}`")
        
        try:
            # Input validation
            if not isinstance(item, dict):
                logger.error(f"Item {i+1} is not a dict: {type(item)}")
                with log_expander:
                    st.error(f"Invalid data format for item {i+1}")
                continue
            
            # Check for required fields
            if not item.get('company'):
                logger.warning(f"Item {i+1} missing company name")
                item['company'] = f'Unknown Company {i+1}'
            
            logger.info(f"Processing startup {i+1}/{total_items}: {company_name}")
            
            # Call the analyzer with error handling
            fit_score_data = analyzer.get_claude_fit_score(item)
            
            if not fit_score_data:
                logger.error(f"No fit score data returned for {company_name}")
                fit_score_data = {
                    "claude_fit_score": 5,
                    "claude_fit_justification": "Analysis failed - no data returned"
                }
            
            # Validate the returned data
            if not isinstance(fit_score_data, dict):
                logger.error(f"Invalid fit score data type for {company_name}: {type(fit_score_data)}")
                fit_score_data = {
                    "claude_fit_score": 5,
                    "claude_fit_justification": "Analysis failed - invalid data format"
                }
            
            # Ensure required fields exist
            if 'claude_fit_score' not in fit_score_data:
                logger.warning(f"Missing claude_fit_score for {company_name}")
                fit_score_data['claude_fit_score'] = 5
            
            if 'claude_fit_justification' not in fit_score_data:
                logger.warning(f"Missing claude_fit_justification for {company_name}")
                fit_score_data['claude_fit_justification'] = "Justification not provided"
            
            with log_expander:
                st.json(fit_score_data) # Display the raw JSON response from the analyzer

            # Update the item with the analysis results
            item.update(fit_score_data)
            processed_data.append(item)
            
            logger.info(f"Successfully processed {company_name}: score={fit_score_data.get('claude_fit_score', 'N/A')}")
            
        except Exception as e:
            logger.error(f"Error processing startup {i+1}/{total_items} ({company_name}): {e}")
            logger.error(f"Full traceback: {traceback.format_exc()}")
            
            with log_expander:
                st.error(f"❌ Failed to analyze {company_name}: {str(e)}")
            
            # Add error data to the item
            error_data = {
                "claude_fit_score": 5,
                "claude_fit_justification": f"Analysis failed: {str(e)}"
            }
            item.update(error_data)
            processed_data.append(item)
        
        # Update progress bar
        progress_text = f"Analyzing startup {i+1}/{total_items}: {company_name}"
        progress_bar.progress((i + 1) / total_items, text=progress_text)
        
        # Add a small delay to avoid overwhelming the API and hitting rate limits
        time.sleep(0.5)

    progress_bar.empty()
    
    logger.info(f"Completed processing {len(processed_data)} startups")
    return processed_data

def display_startup_overview(df):
    """Display overview metrics and charts."""
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Startups", len(df))
    
    with col2:
        # Handle missing claude_fit_score column
        if 'claude_fit_score' in df.columns:
            avg_fit = df['claude_fit_score'].mean()
            st.metric("Avg Claude Fit Score", f"{avg_fit:.1f}/10")
        else:
            st.metric("Avg Claude Fit Score", "N/A")
    
    with col3:
        # Handle missing business_model column
        if 'business_model' in df.columns:
            b2b_count = len(df[df['business_model'].str.contains('B2B', case=False, na=False)])
            st.metric("B2B Companies", b2b_count)
        else:
            st.metric("B2B Companies", "N/A")
    
    with col4:
        # Handle missing industry column
        if 'industry' in df.columns:
            # Clean industry data and get top industry
            industries = df['industry'].dropna()
            if len(industries) > 0:
                top_industry = industries.mode().iloc[0] if not industries.mode().empty else "N/A"
                st.metric("Top Industry", top_industry)
            else:
                st.metric("Top Industry", "N/A")
        else:
            st.metric("Top Industry", "N/A")
    
    # Charts
    col1, col2 = st.columns(2)
    
    with col1:
        # Industry distribution
        if 'industry' in df.columns:
            # Clean industry data
            industry_data = df['industry'].dropna()
            if len(industry_data) > 0:
                industry_counts = industry_data.value_counts()
                fig_industry = px.bar(
                    x=industry_counts.values,
                    y=industry_counts.index,
                    orientation='h',
                    title="Startups by Industry",
                    labels={'x': 'Count', 'y': 'Industry'}
                )
                fig_industry.update_layout(height=400)
                st.plotly_chart(fig_industry, use_container_width=True)
            else:
                st.info("No industry data available for visualization")
        else:
            st.info("Industry data not available for visualization")
    
    with col2:
        # Claude fit score distribution
        if 'claude_fit_score' in df.columns:
            fig_fit = px.histogram(
                df, 
                x='claude_fit_score',
                nbins=10,
                title="Claude Fit Score Distribution",
                labels={'claude_fit_score': 'Claude Fit Score', 'count': 'Number of Startups'}
            )
            fig_fit.update_layout(height=400)
            st.plotly_chart(fig_fit, use_container_width=True)
        else:
            st.info("Claude fit score data not available for visualization")

def display_startup_table(df):
    """Display the startup data in the requested format."""
    st.subheader("📊 Startup Data Overview")
    
    # Define the desired columns and their corresponding names in the DataFrame
    column_config = {
        "Company": "company",
        "Description": "solution",
        "Industry": "industry",
        "Pain Point Addressed": "pain_point",
        "Target Audience": "target_audience",
        "Business Model": "business_model",
        "Challenges": "challenges",
        "Claude Integration Description": "claude_integration_description"
    }
    
    # Create a new DataFrame with only the desired columns, if they exist
    display_df = pd.DataFrame()
    for display_name, internal_name in column_config.items():
        if internal_name in df.columns:
            display_df[display_name] = df[internal_name]
        else:
            # Add an empty column if the data doesn't exist, so the table structure is consistent
            display_df[display_name] = "N/A"

    st.dataframe(display_df, use_container_width=True)

def chat_interface(analyzer, startups_data):
    """Main chat interface for asking questions about the data."""
    st.subheader("💬 Ask Claude About Your Startup Data")

    with st.expander("💡 Need inspiration? Click here for sample questions."):
        st.markdown("""
        - "Generate key talking points for a sales pitch to the top 3 startups."
        - "For startups in the 'SaaS' industry, what are their common pain points and which Claude features can help?"
        - "Which industry is growing the fastest based on this data?"
        - "Summarize the top 5 most promising startups and why they are a good fit for Claude."
        """)
    
    # Initialize chat history
    if "messages" not in st.session_state:
        st.session_state.messages = []
    
    # Display chat history
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
    
    # Chat input
    if prompt := st.chat_input("Ask a question about the startup data..."):
        # Add user message to chat history
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)
        
        # Get Claude's response
        with st.chat_message("assistant"):
            with st.spinner("Claude is analyzing..."):
                response = analyzer.analyze_startup_data(startups_data, prompt)
                st.markdown(response)
        
        # Add assistant response to chat history
        st.session_state.messages.append({"role": "assistant", "content": response})
    
    # Clear chat button
    if st.button("Clear Chat History"):
        st.session_state.messages = []
        st.rerun()

def claude_fit_analyzer(analyzer, startups_data):
    """Interface for detailed Claude fit analysis."""
    st.subheader("🎯 Claude Fit Analyzer")
    
    # Get list of startup names
    startup_names = [startup['company'] for startup in startups_data]
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        selected_startup = st.selectbox("Select a startup to analyze:", startup_names)
        
        if st.button("Analyze Claude Fit", type="primary"):
            with st.spinner("Analyzing Claude fit..."):
                analysis = analyzer.get_claude_fit_analysis(selected_startup, startups_data)
                st.session_state.claude_fit_analysis = analysis
    
    with col2:
        if 'claude_fit_analysis' in st.session_state:
            st.markdown("### Claude Fit Analysis")
            st.markdown(st.session_state.claude_fit_analysis)

def sales_brief_generator(analyzer, startups_data):
    """Interface for generating sales briefs."""
    st.subheader("📝 Sales Brief Generator")
    
    # Get list of startup names
    startup_names = [startup['company'] for startup in startups_data]
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        selected_startup = st.selectbox("Select a startup for sales brief:", startup_names, key="sales_brief")
        
        if st.button("Generate Sales Brief", type="primary"):
            with st.spinner("Generating sales brief..."):
                brief = analyzer.generate_sales_brief(selected_startup, startups_data)
                st.session_state.sales_brief = brief
    
    with col2:
        if 'sales_brief' in st.session_state:
            st.markdown("### Sales Brief")
            st.markdown(st.session_state.sales_brief)

def prompt_generator(analyzer, startups_data):
    """Interface for generating Claude prompt ideas."""
    st.subheader("🤖 Claude Prompt Generator")
    
    # Get list of startup names
    startup_names = [startup['company'] for startup in startups_data]
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        selected_startup = st.selectbox("Select a startup for prompt ideas:", startup_names, key="prompt_gen")
        
        if st.button("Generate Prompt Ideas", type="primary"):
            with st.spinner("Generating prompt ideas..."):
                prompts = analyzer.generate_prompt_ideas(selected_startup, startups_data)
                st.session_state.prompt_ideas = prompts
    
    with col2:
        if 'prompt_ideas' in st.session_state:
            st.markdown("### Claude Prompt Ideas")
            st.markdown(st.session_state.prompt_ideas)

def quick_insights(df):
    """Display quick insights and top performers."""
    st.subheader("🚀 Quick Insights")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### Top Claude Fit Startups")
        if 'claude_fit_score' in df.columns:
            # Sort by Claude fit score
            sorted_df = df.sort_values('claude_fit_score', ascending=False).head(5)
            for i, (_, row) in enumerate(sorted_df.iterrows(), 1):
                company = row.get('company', 'Unknown')
                score = row.get('claude_fit_score', 'N/A')
                industry = row.get('industry', 'N/A')
                pain_point = row.get('pain_point', 'N/A')
                features = row.get('claude_features', ['General AI'])
                
                if isinstance(features, str):
                    features = [features]
                
                st.markdown(f"""
                **{i}. {company}** ({score}/10)
                - Industry: {industry}
                - Pain Point: {pain_point}
                - Claude Features: {', '.join(features)}
                """)
        else:
            st.info("Claude fit score data not available")
    
    with col2:
        st.markdown("### Industry Breakdown")
        if 'industry' in df.columns and 'claude_fit_score' in df.columns:
            industry_stats = df.groupby('industry').agg({
                'claude_fit_score': ['mean', 'count']
            }).round(1)
            industry_stats.columns = ['Avg Fit Score', 'Count']
            industry_stats = industry_stats.sort_values('Avg Fit Score', ascending=False)
            st.dataframe(industry_stats, use_container_width=True)
        elif 'industry' in df.columns:
            # Just show industry counts
            industry_counts = df['industry'].value_counts()
            st.dataframe(industry_counts, use_container_width=True)
        else:
            st.info("Industry data not available for breakdown")

def data_upload_section():
    """Section for uploading custom startup data."""
    st.subheader("📁 Upload Your Own Startup Data")
    
    uploaded_file = st.file_uploader(
        "Choose a CSV or Excel file with startup data",
        type=['csv', 'xlsx', 'xls'],
        help="Upload a spreadsheet with columns: company, industry, business_model, target_audience, pain_point, solution, stage, team_size, tech_stack, use_case"
    )
    
    if uploaded_file is not None:
        # Check if this file has been processed already
        if st.session_state.get('last_uploaded_file') != uploaded_file.name:
            data = parse_uploaded_file(uploaded_file)
            if data:
                st.info(f"File '{uploaded_file.name}' loaded. Now analyzing with Claude...")
                processed_data = process_data_with_claude(get_analyzer(), data)
                st.session_state.startups_data = processed_data
                st.session_state.last_uploaded_file = uploaded_file.name
                st.success("✅ Claude analysis complete!")
                st.rerun()
    
    return None

def display_visual_dashboard(df):
    """Display the visual dashboard with metrics and charts."""
    st.subheader("📊 Visual Dashboard")
    
    # --- Metrics Row ---
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Total Startups", len(df))
    with col2:
        if 'claude_fit_score' in df.columns:
            st.metric("Avg. Claude Fit", f"{df['claude_fit_score'].mean():.1f}/10")
        else:
            st.metric("Avg. Claude Fit", "N/A")
    with col3:
        if 'business_model' in df.columns:
            b2b_count = df['business_model'].str.contains('B2B', case=False, na=False).sum()
            st.metric("B2B Companies", b2b_count)
        else:
            st.metric("B2B Companies", "N/A")
    with col4:
        if 'industry' in df.columns and not df['industry'].dropna().empty:
            st.metric("Top Industry", df['industry'].mode()[0])
        else:
            st.metric("Top Industry", "N/A")

    # --- Charts Row ---
    col1, col2 = st.columns(2)
    with col1:
        if 'industry' in df.columns and not df['industry'].dropna().empty:
            st.markdown("##### Startups by Industry")
            industry_counts = df['industry'].value_counts()
            fig = px.bar(industry_counts, x=industry_counts.values, y=industry_counts.index, orientation='h', labels={'x':'Count', 'y':''})
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("No industry data to display.")
            
    with col2:
        if 'claude_fit_score' in df.columns:
            st.markdown("##### Claude Fit Score Distribution")
            fig = px.histogram(df, x='claude_fit_score', nbins=10, labels={'claude_fit_score':'Claude Fit Score'})
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("No Claude Fit Score data to display.")

def display_detailed_table(df):
    """Display a detailed table with custom columns, ensuring all columns exist."""
    st.subheader("📑 Detailed Startup Data")

    # Define the full set of columns we expect to see in the final table.
    all_columns = {
        "Company": "company",
        "Description": "solution",
        "Industry": "industry",
        "Pain Point Addressed": "pain_point",
        "Claude Fit Score": "claude_fit_score",
        "Claude Fit Justification": "claude_fit_justification",
        "Target Audience": "target_audience",
        "Business Model": "business_model",
    }
    
    display_df = df.copy()

    # Ensure all expected columns exist, filling with descriptive errors if they don't.
    for display_name, internal_name in all_columns.items():
        if internal_name not in display_df.columns:
            # The column is missing entirely, which means a step failed.
            # Provide a helpful default message.
            if 'justification' in internal_name or 'score' in internal_name:
                display_df[internal_name] = "AI analysis did not run or failed."
            else:
                display_df[internal_name] = "Column not found in source file."

    # Select and rename columns for the final display order.
    final_display_df = pd.DataFrame()
    for display_name, internal_name in all_columns.items():
        final_display_df[display_name] = display_df[internal_name]

    st.dataframe(final_display_df, use_container_width=True)

def main():
    """Main application function."""
    st.markdown('<h1 class="main-header">🤖 Claude Startup Insights Bot</h1>', unsafe_allow_html=True)
    st.markdown("### Your AI-powered sales strategist for startup analysis and Claude product recommendations")

    # --- Initialization and API Key Check ---
    logger.info("Starting application")
    
    # Validate API configuration first
    is_valid, validation_message = validate_api_configuration()
    if not is_valid:
        st.error(f"❌ API Configuration Error: {validation_message}")
        st.info("Please check your `.env` file and ensure your ANTHROPIC_API_KEY is properly set.")
        st.code("ANTHROPIC_API_KEY=your_key_here")
        st.stop()
    
    # Get analyzer
    analyzer = get_analyzer()
    if analyzer is None:
        st.error("❌ Failed to initialize AI analyzer. Please check your configuration and try again.")
        st.stop()

    # Perform a one-time API connection test per session.
    if 'api_connection_tested' not in st.session_state:
        logger.info("Testing API connection")
        success, message = analyzer.test_api_connection()
        if success:
            st.toast(f"✅ {message}", icon="✅")
            st.session_state.api_connection_tested = True
            logger.info("API connection test successful")
        else:
            st.error(f"❌ API Connection Failed: {message}")
            logger.error(f"API connection test failed: {message}")
            st.stop()

    # --- Data Loading and Processing ---
    # This block runs only once when the app starts or when the session is new.
    if 'startups_data' not in st.session_state:
        logger.info("Loading and processing initial sample data.")
        info_message = st.info("Analyzing sample startup data with Claude... this may take a moment.")
        
        initial_data_list = load_data()  # Returns a list of dicts
        
        if initial_data_list: # Check if the list is not empty
            processed_data = process_data_with_claude(analyzer, initial_data_list)
            st.session_state.startups_data = processed_data
            logger.info("Initial data processing complete.")
            
            # Clear the info message and rerun to refresh the page
            info_message.empty()
            st.rerun()
        else:
            st.session_state.startups_data = []
            logger.warning("Initial data loading returned no data.")
            info_message.empty()

    # --- File Uploader ---
    uploaded_file = st.file_uploader(
        "Upload a CSV or Excel file to analyze your own startup data",
        type=['csv', 'xlsx', 'xls'],
        help="Upload a spreadsheet with columns like: company, industry, pain_point, solution, etc."
    )

    if uploaded_file is not None:
        # Check if this file has been processed already to avoid reprocessing on every interaction
        if st.session_state.get('last_uploaded_file') != uploaded_file.name:
            logger.info(f"Processing uploaded file: {uploaded_file.name}")
            data = parse_uploaded_file(uploaded_file)
            if data:
                st.info(f"📁 File '{uploaded_file.name}' loaded. Now analyzing with Claude...")
                logger.info(f"Starting Claude analysis for {len(data)} startups")
                processed_data = process_data_with_claude(analyzer, data)
                st.session_state.startups_data = processed_data
                st.session_state.last_uploaded_file = uploaded_file.name
                st.success("✅ Claude analysis complete!")
                logger.info("Claude analysis completed successfully")
                st.rerun()
            else:
                st.error("❌ Failed to parse uploaded file. Please check the file format.")
                logger.error(f"Failed to parse uploaded file: {uploaded_file.name}")
    
    # --- Display Data ---
    # Ensure dataframe is not created with empty data if something went wrong
    if not st.session_state.get('startups_data'):
        st.warning("No startup data to display. Please upload a file or check your sample data.")
        st.stop()
        
    df = pd.DataFrame(st.session_state.startups_data)
    logger.info(f"Displaying data for {len(df)} startups")

    # --- Main Layout ---
    display_visual_dashboard(df)
    st.markdown("---")
    display_detailed_table(df)

    # --- Chat Section ---
    st.markdown("---")
    chat_interface(analyzer, st.session_state.startups_data)

if __name__ == "__main__":
    main() 
