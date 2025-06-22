# Claude Startup Insights Bot

This project is an AI-powered sales tool built with Streamlit and Anthropic's Claude API. It helps sales teams analyze startup data to identify high-potential leads, understand their needs, and generate tailored outreach strategies.

## How It Works

The application functions as a data enrichment and analysis pipeline. It takes a list of startups (either from sample data or a user-uploaded file), sends each startup's information to the Claude API for analysis, and then displays the enriched data in an interactive dashboard. The user can then chat with an AI assistant to ask further questions about the analyzed data.

### Core Workflow

1.  **Initialization**: When the app starts (`streamlit run app.py`), it first validates the `ANTHROPIC_API_KEY` from the `.env` file.
2.  **Initial Data Processing**: On the first load, the app takes the sample data from `sample_data.py`, sends it to the `ClaudeAnalyzer` for scoring and justification, and stores the results.
3.  **Display**: The processed data is displayed in a visual dashboard with metrics, charts, and a detailed table.
4.  **User Upload**: A user can upload their own CSV or Excel file. The app parses this file, standardizes column names, and sends the data through the same Claude analysis pipeline.
5.  **Interactive Chat**: The user can ask natural language questions about the data, which are answered by Claude using the context of the analyzed startups.

## File Breakdown

Here is a description of the key files and directories in the project:

| File / Directory      | Description                                                                                                                                                                                            |
| --------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| `app.py`              | **Main Application File**. This is the entry point for the Streamlit app. It defines the entire user interface (UI), handles data loading and uploading, orchestrates the analysis process, and displays all tables and charts. |
| `claude_analyzer.py`  | **The AI Engine**. This file contains the `ClaudeAnalyzer` class, which manages all communication with the Claude API. It includes methods for calculating fit scores, enriching data, and handling API errors and retries. |
| `sample_data.py`      | **Sample Dataset**. Provides a default list of startups so the application can be used immediately without requiring a file upload.                                                                    |
| `test_error_handling.py` | **Testing Script**. A utility script used during development to verify that the error handling and logging in `claude_analyzer.py` and `app.py` work as expected.                                    |
| `requirements.txt`    | **Dependencies**. Lists all the Python libraries needed to run the project. You install these using `pip install -r requirements.txt`.                                                                    |
| `.env`                | **Environment Variables**. A local, private file (not committed to version control) where the `ANTHROPIC_API_KEY` is securely stored.                                                                   |
| `README.md`           | **Project Documentation**. This file, which you are currently reading.                                                                                                                                      |

## How to Set Up and Run

Follow these steps to get the application running on your local machine.

### 1. Prerequisites

-   Python 3.8+
-   An API key from [Anthropic](https://www.anthropic.com/)

### 2. Installation

Clone the repository and install the required dependencies.

```bash
# Clone the repository (if you haven't already)
git clone <repository_url>
cd <repository_directory>

# Install Python packages
pip install -r requirements.txt
```

### 3. Set Up Your API Key

Create a file named `.env` in the root of the project directory and add your Anthropic API key to it:

```
ANTHROPIC_API_KEY=your_key_here
```

### 4. Run the Application

Launch the Streamlit app from your terminal:

```bash
streamlit run app.py
```

The application should open automatically in your web browser. The first time it runs, it will analyze the built-in sample data, which may take a few moments.

## 🚀 Features

### 📊 Data Analysis & Insights
- **Natural Language Queries**: Ask questions about startup data in plain English
- **Statistical Analysis**: Get insights on trends, patterns, and distributions
- **Interactive Visualizations**: Charts and graphs for data exploration
- **Filtering & Sorting**: Explore data by industry, business model, Claude fit score, etc.

### 🎯 Claude Product Strategy
- **Claude Fit Analysis**: Detailed analysis of which Claude products would benefit each startup
- **Feature Mapping**: Match startup pain points to specific Claude capabilities
- **Implementation Suggestions**: Technical recommendations for Claude integration
- **Discovery Questions**: Tailored questions for sales calls

### 📝 Sales & Engagement Tools
- **Sales Brief Generator**: Create personalized outreach strategies
- **Email Templates**: Ready-to-use introduction emails
- **Call Preparation**: Talking points and objection handling
- **Follow-up Strategies**: Next steps and engagement plans

### 🧠 AI-Powered Intelligence
- **Claude API Integration**: Leverages Claude 3.5 Sonnet for analysis
- **Contextual Understanding**: Deep analysis of startup data and needs
- **Structured Output**: Organized, actionable insights
- **Multi-turn Conversations**: Maintains context across interactions

## 🛠️ Installation & Setup

### Prerequisites
- Python 3.8+
- Anthropic API key

### 1. Clone the Repository
```bash
git clone <repository-url>
cd SalesAssistant
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Set Up Environment Variables
Create a `.env` file in the project root:
```bash
ANTHROPIC_API_KEY=your_anthropic_api_key_here
```

### 4. Run the Application
```bash
streamlit run app.py
```

The application will open in your browser at `http://localhost:8501`

## 📖 Usage Guide

### 🏠 Overview Dashboard
- **Metrics Overview**: Key statistics about the startup dataset
- **Interactive Charts**: Industry distribution and Claude fit scores
- **Filterable Data Table**: Explore startups with various filters

### 💬 Chat Analysis
Ask natural language questions like:
- "Which 5 startups are best positioned for Claude-powered customer support?"
- "What's the most common industry in this dataset?"
- "Which startups would benefit most from Claude API?"
- "Rank companies by their potential for Claude integration"
- "What are the top pain points across all startups?"

### 🎯 Claude Fit Analyzer
1. Select a startup from the dropdown
2. Click "Analyze Claude Fit"
3. Get detailed recommendations including:
   - Specific Claude products to recommend
   - Feature mapping to pain points
   - Implementation strategy
   - Discovery questions for sales calls
   - Sample Claude prompts

### 📝 Sales Brief Generator
1. Select a startup for outreach
2. Click "Generate Sales Brief"
3. Receive a comprehensive brief with:
   - Email introduction template
   - Key talking points
   - Value propositions
   - Objection handling
   - Follow-up strategy

### 🚀 Quick Insights
- **Top Performers**: Startups with highest Claude fit scores
- **Industry Breakdown**: Average fit scores by industry
- **Trend Analysis**: Patterns and insights at a glance
