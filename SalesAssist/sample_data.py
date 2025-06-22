"""
Sample YC-style startup dataset for the Claude-powered insights bot.
This simulates the kind of data a sales team might have about potential customers.
"""

SAMPLE_STARTUPS = [
    {
        "company": "Lapel",
        "industry": "Customer Operations",
        "business_model": "B2B SaaS",
        "target_audience": "Internet businesses",
        "pain_point": "Fragmented customer ops tools",
        "solution": "Unified customer operations platform",
        "stage": "Series A",
        "team_size": "15-25",
        "tech_stack": "React, Node.js, PostgreSQL",
        "use_case": "Customer support automation, ticket management",
        "claude_fit_score": 9,
        "claude_features": ["Long context", "Safe reasoning", "Tone control"],
        "discovery_questions": [
            "How do you handle escalations or tone control in AI-driven support today?",
            "How much of your current CX knowledge base could be used to power an AI assistant?",
            "What's your current process for training support agents on new products?"
        ]
    },
    {
        "company": "Cohesive",
        "industry": "CRM",
        "business_model": "B2B SaaS",
        "target_audience": "Blue-collar businesses",
        "pain_point": "Manual follow-up processes",
        "solution": "AI-powered CRM for service businesses",
        "stage": "Seed",
        "team_size": "5-15",
        "tech_stack": "Python, Django, AWS",
        "use_case": "Automated follow-ups, lead management",
        "claude_fit_score": 8,
        "claude_features": ["Structured output", "Multi-agent orchestration"],
        "discovery_questions": [
            "How do you currently handle follow-up timing and personalization?",
            "What types of customer interactions require the most manual work?",
            "How do you ensure consistency across different team members?"
        ]
    },
    {
        "company": "Zero",
        "industry": "Productivity",
        "business_model": "B2B SaaS",
        "target_audience": "Knowledge workers",
        "pain_point": "Email overload and information chaos",
        "solution": "AI-powered email and information management",
        "stage": "Series B",
        "team_size": "25-50",
        "tech_stack": "TypeScript, React, GraphQL",
        "use_case": "Email summarization, sentiment detection",
        "claude_fit_score": 9,
        "claude_features": ["Summarization", "Sentiment analysis", "Long context"],
        "discovery_questions": [
            "How do you currently prioritize which emails need immediate attention?",
            "What percentage of emails could be auto-responded to or summarized?",
            "How do you handle sensitive information in automated processing?"
        ]
    },
    {
        "company": "Milo",
        "industry": "Productivity",
        "business_model": "B2C SaaS",
        "target_audience": "Parents",
        "pain_point": "Overwhelming task management",
        "solution": "AI assistant for parent productivity",
        "stage": "Seed",
        "team_size": "5-15",
        "tech_stack": "React Native, Firebase",
        "use_case": "Task automation, safety-aware assistance",
        "claude_fit_score": 7,
        "claude_features": ["Safety controls", "Task planning"],
        "discovery_questions": [
            "How do you ensure AI suggestions are appropriate for family contexts?",
            "What types of tasks do parents struggle with most?",
            "How do you handle privacy concerns with family data?"
        ]
    },
    {
        "company": "Aegis",
        "industry": "Healthcare",
        "business_model": "B2B SaaS",
        "target_audience": "Insurance companies",
        "pain_point": "Manual insurance claim processing",
        "solution": "AI-powered insurance claims automation",
        "stage": "Series A",
        "team_size": "15-25",
        "tech_stack": "Python, FastAPI, PostgreSQL",
        "use_case": "Claim analysis, appeal generation",
        "claude_fit_score": 8,
        "claude_features": ["Document analysis", "Structured reasoning"],
        "discovery_questions": [
            "How do you currently handle claim denial appeals?",
            "What types of documents are most time-consuming to process?",
            "How do you ensure compliance with healthcare regulations?"
        ]
    },
    {
        "company": "Docket",
        "industry": "Legal Tech",
        "business_model": "B2B SaaS",
        "target_audience": "Law firms",
        "pain_point": "Manual legal document processing",
        "solution": "AI-powered legal document automation",
        "stage": "Seed",
        "team_size": "5-15",
        "tech_stack": "Python, Django, Redis",
        "use_case": "Document analysis, contract review",
        "claude_fit_score": 9,
        "claude_features": ["Document understanding", "Legal reasoning"],
        "discovery_questions": [
            "What types of documents are most repetitive or error-prone?",
            "How do you ensure tone compliance in AI-generated legal comms?",
            "How much manual summarization happens in your current workflows?"
        ]
    },
    {
        "company": "Blueshoe",
        "industry": "Legal Tech",
        "business_model": "B2B SaaS",
        "target_audience": "Small law firms",
        "pain_point": "Manual back-office operations",
        "solution": "AI-native legal back office platform",
        "stage": "Series A",
        "team_size": "15-25",
        "tech_stack": "TypeScript, Node.js, MongoDB",
        "use_case": "Legal document generation, compliance",
        "claude_fit_score": 8,
        "claude_features": ["Document generation", "Compliance checking"],
        "discovery_questions": [
            "What types of documents are most repetitive or error-prone?",
            "How do you ensure tone compliance in AI-generated legal comms?",
            "How much manual summarization happens in your current workflows?"
        ]
    },
    {
        "company": "SecureFlow",
        "industry": "Cybersecurity",
        "business_model": "B2B SaaS",
        "target_audience": "Enterprise companies",
        "pain_point": "Complex security log analysis",
        "solution": "AI-powered security log analysis",
        "stage": "Series B",
        "team_size": "25-50",
        "tech_stack": "Python, Go, Elasticsearch",
        "use_case": "Threat detection, audit logging",
        "claude_fit_score": 7,
        "claude_features": ["Log analysis", "Explainability"],
        "discovery_questions": [
            "How do you currently identify false positives in security alerts?",
            "What types of security events require the most manual investigation?",
            "How do you ensure AI explanations are understandable to security teams?"
        ]
    },
    {
        "company": "DataVault",
        "industry": "Data Analytics",
        "business_model": "B2B SaaS",
        "target_audience": "Data teams",
        "pain_point": "Manual data pipeline monitoring",
        "solution": "AI-powered data pipeline monitoring",
        "stage": "Seed",
        "team_size": "5-15",
        "tech_stack": "Python, Apache Airflow, Snowflake",
        "use_case": "Pipeline monitoring, anomaly detection",
        "claude_fit_score": 6,
        "claude_features": ["Data analysis", "Anomaly detection"],
        "discovery_questions": [
            "How do you currently identify data quality issues?",
            "What types of pipeline failures are most costly?",
            "How do you communicate data issues to stakeholders?"
        ]
    },
    {
        "company": "HealthSync",
        "industry": "Healthcare",
        "business_model": "B2B SaaS",
        "target_audience": "Healthcare providers",
        "pain_point": "Patient data integration",
        "solution": "AI-powered patient data integration platform",
        "stage": "Series A",
        "team_size": "15-25",
        "tech_stack": "Python, FastAPI, HL7 FHIR",
        "use_case": "Patient data processing, compliance",
        "claude_fit_score": 8,
        "claude_features": ["Data integration", "Compliance checking"],
        "discovery_questions": [
            "How do you handle data from different EHR systems?",
            "What compliance challenges do you face with patient data?",
            "How do you ensure data accuracy across different sources?"
        ]
    }
]

def get_sample_data():
    """Return the sample startup data as a pandas DataFrame."""
    import pandas as pd
    return pd.DataFrame(SAMPLE_STARTUPS)

def get_startup_by_name(name):
    """Get a specific startup by name."""
    for startup in SAMPLE_STARTUPS:
        if startup["company"].lower() == name.lower():
            return startup
    return None

def get_startups_by_industry(industry):
    """Get all startups in a specific industry."""
    return [startup for startup in SAMPLE_STARTUPS 
            if startup["industry"].lower() == industry.lower()]

def get_top_claude_fits(limit=5):
    """Get startups with the highest Claude fit scores."""
    sorted_startups = sorted(SAMPLE_STARTUPS, 
                           key=lambda x: x["claude_fit_score"], 
                           reverse=True)
    return sorted_startups[:limit] 
