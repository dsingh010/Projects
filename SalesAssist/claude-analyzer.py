"""
Claude-powered startup analysis engine.
Handles API calls to Claude for startup insights and sales strategy.
"""

import os
import json
import pandas as pd
from typing import List, Dict, Any, Optional
from anthropic import Anthropic
from dotenv import load_dotenv
import logging
import traceback

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

load_dotenv()

class ClaudeAnalyzer:
    def __init__(self):
        """Initialize the Claude analyzer with API key from environment."""
        try:
            api_key = os.getenv('ANTHROPIC_API_KEY')
            if not api_key:
                raise ValueError("ANTHROPIC_API_KEY not found in environment variables")
            
            self.client = Anthropic(api_key=api_key)
            self.model = "claude-3-5-sonnet-20241022"
            logger.info("ClaudeAnalyzer initialized successfully")
        except Exception as e:
            logger.error(f"Failed to initialize ClaudeAnalyzer: {e}")
            raise

    def test_api_connection(self):
        """Make a small test call to verify the API key and connection."""
        try:
            self.client.messages.create(
                model=self.model,
                max_tokens=10,
                messages=[{"role": "user", "content": "Hello"}]
            )
            return True, "API Key is valid and connection is successful."
        except Exception as e:
            # Catch specific error types if possible, e.g., authentication errors
            error_message = f"API Key is invalid or connection failed: {e}"
            return False, error_message
    
    def analyze_startup_data(self, startups_data: List[Dict], query: str) -> str:
        """
        Analyze startup data using Claude based on user query.
        
        Args:
            startups_data: List of startup dictionaries
            query: User's question about the data
            
        Returns:
            Claude's analysis response
        """
        # Convert data to a more readable format for Claude
        data_summary = self._format_data_for_claude(startups_data)
        
        system_prompt = self._get_system_prompt()
        
        user_message = f"""
Data about {len(startups_data)} startups:

{data_summary}

User Question: {query}

Please provide a comprehensive analysis. Format your response in a clear, structured way.
"""
        
        try:
            response = self.client.messages.create(
                model=self.model,
                max_tokens=4000,
                system=system_prompt,
                messages=[{"role": "user", "content": user_message}]
            )
            return response.content[0].text
        except Exception as e:
            return f"Error communicating with Claude API: {str(e)}"
    
    def get_claude_fit_analysis(self, startup_name: str, startups_data: List[Dict]) -> str:
        """
        Get detailed Claude fit analysis for a specific startup.
        
        Args:
            startup_name: Name of the startup to analyze
            startups_data: List of all startup data
            
        Returns:
            Detailed Claude fit analysis
        """
        startup = None
        for s in startups_data:
            if s["company"].lower() == startup_name.lower():
                startup = s
                break
        
        if not startup:
            return f"Startup '{startup_name}' not found in the data."
        
        system_prompt = self._get_claude_fit_prompt()
        
        user_message = f"""
Analyze this startup for Claude product fit:

Company: {startup['company']}
Industry: {startup['industry']}
Business Model: {startup['business_model']}
Target Audience: {startup['target_audience']}
Pain Point: {startup['pain_point']}
Solution: {startup['solution']}
Use Case: {startup['use_case']}
Tech Stack: {startup['tech_stack']}

Current Claude Fit Score: {startup['claude_fit_score']}/10
Current Claude Features: {', '.join(startup['claude_features'])}

Please provide:
1. Detailed Claude product recommendations
2. Specific Claude features that would benefit them most
3. Discovery questions for sales calls
4. Sample Claude prompts they could use
5. Implementation suggestions
"""
        
        try:
            response = self.client.messages.create(
                model=self.model,
                max_tokens=3000,
                system=system_prompt,
                messages=[{"role": "user", "content": user_message}]
            )
            return response.content[0].text
        except Exception as e:
            return f"Error analyzing Claude fit: {str(e)}"
    
    def generate_sales_brief(self, startup_name: str, startups_data: List[Dict]) -> str:
        """
        Generate a sales brief for outreach to a specific startup.
        
        Args:
            startup_name: Name of the startup
            startups_data: List of all startup data
            
        Returns:
            Sales brief with outreach strategy
        """
        startup = None
        for s in startups_data:
            if s["company"].lower() == startup_name.lower():
                startup = s
                break
        
        if not startup:
            return f"Startup '{startup_name}' not found in the data."
        
        system_prompt = self._get_sales_brief_prompt()
        
        user_message = f"""
Create a sales brief for outreach to this startup:

Company: {startup['company']}
Industry: {startup['industry']}
Business Model: {startup['business_model']}
Target Audience: {startup['target_audience']}
Pain Point: {startup['pain_point']}
Solution: {startup['solution']}
Stage: {startup['stage']}
Team Size: {startup['team_size']}
Claude Fit Score: {startup['claude_fit_score']}/10

Please provide:
1. Email introduction template
2. Key talking points for initial call
3. Specific Claude value propositions
4. Potential objections and responses
5. Next steps and follow-up strategy
"""
        
        try:
            response = self.client.messages.create(
                model=self.model,
                max_tokens=3000,
                system=system_prompt,
                messages=[{"role": "user", "content": user_message}]
            )
            return response.content[0].text
        except Exception as e:
            return f"Error generating sales brief: {str(e)}"
    
    def generate_prompt_ideas(self, startup_name: str, startups_data: List[Dict]) -> str:
        """
        Generate Claude prompt ideas for a specific startup.
        
        Args:
            startup_name: Name of the startup
            startups_data: List of all startup data
            
        Returns:
            Prompt ideas and examples
        """
        startup = None
        for s in startups_data:
            if s["company"].lower() == startup_name.lower():
                startup = s
                break
        
        if not startup:
            return f"Startup '{startup_name}' not found in the data."
        
        system_prompt = """You are a Claude prompt engineering expert helping startups create effective prompts for their use cases.

For each startup, create:
1. **Industry-Specific Prompts**: Prompts tailored to their business domain
2. **Workflow Prompts**: Prompts for their specific pain points
3. **Role-Based Prompts**: Prompts for different team members
4. **Integration Prompts**: Prompts for their tech stack
5. **Advanced Prompts**: Complex prompts for sophisticated use cases

Make prompts practical, specific, and ready-to-use."""
        
        user_message = f"""
Generate Claude prompt ideas for this startup:

Company: {startup['company']}
Industry: {startup['industry']}
Business Model: {startup['business_model']}
Target Audience: {startup['target_audience']}
Pain Point: {startup['pain_point']}
Solution: {startup['solution']}
Use Case: {startup['use_case']}
Tech Stack: {startup['tech_stack']}

Please provide:
1. 5-10 specific Claude prompts they could use immediately
2. Prompts for different use cases (customer support, data analysis, content creation, etc.)
3. Prompts tailored to their industry and pain points
4. Advanced prompts for complex workflows
5. Tips for optimizing these prompts
"""
        
        try:
            response = self.client.messages.create(
                model=self.model,
                max_tokens=3000,
                system=system_prompt,
                messages=[{"role": "user", "content": user_message}]
            )
            return response.content[0].text
        except Exception as e:
            return f"Error generating prompt ideas: {str(e)}"
    
    def enrich_startup_data(self, startup_info: Dict) -> Dict:
        """
        Enrich startup data with inferred challenges and Claude integration ideas,
        role-playing as a senior Anthropic Sales Engineer.
        """
        # Input validation
        if not startup_info:
            logger.error("startup_info is None or empty in enrich_startup_data")
            return {
                'challenges': "No startup data provided for enrichment.",
                'claude_integration_description': "No startup data provided for enrichment."
            }
        
        if not isinstance(startup_info, dict):
            logger.error(f"startup_info is not a dict in enrich_startup_data, got {type(startup_info)}")
            return {
                'challenges': "Invalid startup data format for enrichment.",
                'claude_integration_description': "Invalid startup data format for enrichment."
            }
        
        # Validate required fields
        company = startup_info.get('company', '')
        if not company or company == 'N/A':
            logger.warning("Company name is missing or invalid in enrich_startup_data")
            company = "Unknown Company"
        
        logger.info(f"Starting data enrichment for: {company}")
        
        system_prompt = """
You are a top-tier, senior Sales Engineer at Anthropic. Your expertise lies in deeply understanding a startup's business and technical landscape and identifying the most valuable and impactful ways they can leverage Claude. You have a master-level understanding of all Claude models and features.

Your task is to analyze a startup based on limited data and provide two key insights. Your response MUST be a valid JSON object with ONLY two keys: "challenges" and "claude_integration_description".

1.  **challenges**: In 1-2 sentences, identify the most critical business or technical challenge this startup likely faces. Be sharp, insightful, and specific. Think about market competition, technical debt, user adoption, or scaling issues.

2.  **claude_integration_description**: In 2-3 sentences, propose a specific, high-value integration using a concrete Claude model.
    *   **Name the Model:** Explicitly recommend **Claude 3.5 Sonnet**, **Claude 3 Opus**, or **Claude 3 Haiku**.
    *   **Justify Your Choice:** Briefly explain *why* that model is the best fit (e.g., "due to its state-of-the-art intelligence for complex analysis," or "for its industry-leading speed in real-time applications").
    *   **Describe the Use Case:** Detail a compelling use case that solves their core pain point or addresses one of their challenges. Mention advanced features like **Tool Use** if it allows them to connect Claude to their existing systems.

Example Response:
{
    "challenges": "The startup likely faces intense competition in the QA automation space and may struggle to differentiate from established players. Their core challenge is proving a significant leap in efficiency over traditional testing frameworks.",
    "claude_integration_description": "We recommend integrating **Claude 3.5 Sonnet** to power their AI agents. Due to its sophisticated reasoning and code generation capabilities, it can analyze requirement specs and auto-generate comprehensive QA test suites, drastically reducing manual effort. Using **Tool Use**, they could connect Claude to their CI/CD pipeline to automatically run tests and report results."
}
"""
        
        # Create a clean summary of the startup for the prompt
        valid_info = {k: v for k, v in startup_info.items() if v and v != 'N/A' and str(v).strip()}
        if not valid_info:
            logger.warning(f"No valid data found for {company} in enrichment, using minimal info")
            valid_info = {'company': company}
        
        info_str = "\n".join([f"- {key}: {value}" for key, value in valid_info.items()])
        user_message = f"Analyze the following startup and provide your response as a single, valid JSON object.\n\nStartup Information:\n{info_str}"
        
        try:
            logger.info(f"Making enrichment API call for {company}")
            response = self.client.messages.create(
                model=self.model,
                max_tokens=1024,
                system=system_prompt,
                messages=[{"role": "user", "content": user_message}]
            )
            
            if not response or not response.content:
                logger.error(f"Empty response from enrichment API for {company}")
                startup_info['challenges'] = "Received empty response from AI model."
                startup_info['claude_integration_description'] = "Received empty response from AI model."
                return startup_info
            
            response_text = response.content[0].text
            logger.info(f"Received enrichment response for {company}: {response_text[:100]}...")
            
            json_start = response_text.find('{')
            json_end = response_text.rfind('}') + 1
            if json_start != -1 and json_end != -1:
                json_str = response_text[json_start:json_end]
                try:
                    enriched_data = json.loads(json_str)
                    
                    # Validate the parsed data
                    if not isinstance(enriched_data, dict):
                        logger.error(f"Parsed enrichment data is not a dict for {company}: {type(enriched_data)}")
                        startup_info['challenges'] = "Could not parse enrichment data - unexpected format."
                        startup_info['claude_integration_description'] = "Could not parse enrichment data - unexpected format."
                        return startup_info
                    
                    # Validate required fields
                    challenges = enriched_data.get('challenges')
                    if not challenges or not str(challenges).strip():
                        logger.warning(f"No challenges found in enrichment for {company}")
                        challenges = "Could not identify specific challenges."
                    
                    integration_desc = enriched_data.get('claude_integration_description')
                    if not integration_desc or not str(integration_desc).strip():
                        logger.warning(f"No integration description found in enrichment for {company}")
                        integration_desc = "Could not provide integration description."
                    
                    startup_info['challenges'] = str(challenges).strip()
                    startup_info['claude_integration_description'] = str(integration_desc).strip()
                    
                    logger.info(f"Successfully enriched data for {company}")
                    
                except json.JSONDecodeError as json_err:
                    logger.error(f"JSON decode error in enrichment for {company}: {json_err}. Response: {json_str}")
                    startup_info['challenges'] = "Could not parse enrichment data from model - invalid JSON."
                    startup_info['claude_integration_description'] = "Could not parse enrichment data from model - invalid JSON."
            else:
                logger.error(f"Could not find JSON in enrichment response for {company}: {response_text}")
                startup_info['challenges'] = "Could not parse enrichment data from model - invalid JSON format."
                startup_info['claude_integration_description'] = "Could not parse enrichment data from model - invalid JSON format."
            
            return startup_info

        except anthropic.RateLimitError as e:
            logger.error(f"Rate limit exceeded in enrichment for {company}: {e}")
            startup_info['challenges'] = "Enrichment rate limited - please try again later."
            startup_info['claude_integration_description'] = "Enrichment rate limited - please try again later."
            return startup_info
        
        except anthropic.AuthenticationError as e:
            logger.error(f"Authentication error in enrichment for {company}: {e}")
            startup_info['challenges'] = "Enrichment authentication failed - check API key."
            startup_info['claude_integration_description'] = "Enrichment authentication failed - check API key."
            return startup_info
        
        except anthropic.APIError as e:
            logger.error(f"API error in enrichment for {company}: {e}")
            startup_info['challenges'] = f"Enrichment API error: {str(e)}"
            startup_info['claude_integration_description'] = f"Enrichment API error: {str(e)}"
            return startup_info
        
        except Exception as e:
            logger.error(f"Unexpected error in enrichment for {company}: {e}")
            logger.error(f"Full traceback: {traceback.format_exc()}")
            startup_info['challenges'] = f"Could not enrich data: {str(e)}"
            startup_info['claude_integration_description'] = f"Could not enrich data: {str(e)}"
            return startup_info
    
    def get_claude_fit_score(self, startup_info: Dict) -> Dict:
        """
        Analyzes a startup to generate a Claude fit score and justification.
        """
        # Input validation
        if not startup_info:
            logger.error("startup_info is None or empty")
            return {"claude_fit_score": 5, "claude_fit_justification": "No startup data provided for analysis."}
        
        if not isinstance(startup_info, dict):
            logger.error(f"startup_info is not a dict, got {type(startup_info)}")
            return {"claude_fit_score": 5, "claude_fit_justification": "Invalid startup data format."}
        
        # Validate required fields
        company = startup_info.get('company', '')
        if not company or company == 'N/A':
            logger.warning("Company name is missing or invalid")
            company = "Unknown Company"
        
        logger.info(f"Starting Claude fit analysis for: {company}")
        
        system_prompt = """
You are a senior Sales Engineer at Anthropic. Your task is to analyze a startup and determine a "Claude Fit Score" from 1 to 10. The score represents how much value the startup could derive from integrating a Claude model into their core business or operations.

Your response MUST be a valid JSON object with ONLY two keys: "claude_fit_score" (an integer) and "claude_fit_justification" (a 1-2 sentence string).

- A score of 1-3 means a poor fit, where Claude offers little to no advantage.
- A score of 4-6 indicates a moderate fit, with potential for some specific, non-critical use cases.
- A score of 7-8 signifies a strong fit, where Claude could become a key part of their product or a significant operational accelerator.
- A score of 9-10 represents an exceptional fit, where Claude could be a transformative, strategic technology for the company.

Base your score on factors like their industry (e.g., SaaS, fintech are often high-fit), their business model, the problems they solve, and their likely need for advanced language processing, reasoning, or content generation.

Example Response:
{
    "claude_fit_score": 8,
    "claude_fit_justification": "As a B2B SaaS in the legal tech space, this company has a strong need for document analysis and summarization, making it a prime candidate for leveraging Claude for core product features."
}
"""
        
        # Create input string with validation
        valid_info = {k: v for k, v in startup_info.items() if v and v != 'N/A' and str(v).strip()}
        if not valid_info:
            logger.warning(f"No valid data found for {company}, using minimal info")
            valid_info = {'company': company}
        
        info_str = "\n".join([f"- {key}: {value}" for key, value in valid_info.items()])
        user_message = f"Analyze the following startup and provide your response as a single, valid JSON object.\n\nStartup Information:\n{info_str}"

        try:
            logger.info(f"Making API call for {company}")
            response = self.client.messages.create(
                model=self.model,
                max_tokens=512,
                system=system_prompt,
                messages=[{"role": "user", "content": user_message}]
            )
            
            if not response or not response.content:
                logger.error(f"Empty response from API for {company}")
                return {"claude_fit_score": 5, "claude_fit_justification": "Received empty response from AI model."}
            
            response_text = response.content[0].text
            logger.info(f"Received response for {company}: {response_text[:100]}...")
            
            # Parse JSON response
            json_start = response_text.find('{')
            json_end = response_text.rfind('}') + 1
            
            if json_start == -1 or json_end == -1:
                logger.error(f"Could not find JSON in response for {company}: {response_text}")
                return {"claude_fit_score": 5, "claude_fit_justification": "Could not parse score from model - invalid JSON format."}
            
            json_str = response_text[json_start:json_end]
            
            try:
                fit_data = json.loads(json_str)
            except json.JSONDecodeError as json_err:
                logger.error(f"JSON decode error for {company}: {json_err}. Response: {json_str}")
                return {"claude_fit_score": 5, "claude_fit_justification": "Could not parse score from model - invalid JSON."}
            
            # Validate the parsed data
            if not isinstance(fit_data, dict):
                logger.error(f"Parsed data is not a dict for {company}: {type(fit_data)}")
                return {"claude_fit_score": 5, "claude_fit_justification": "Could not parse score from model - unexpected data format."}
            
            # Extract and validate score
            score = fit_data.get('claude_fit_score')
            if score is None:
                logger.warning(f"No claude_fit_score found in response for {company}")
                score = 5
            else:
                try:
                    score = int(score)
                    if not (1 <= score <= 10):
                        logger.warning(f"Score out of range for {company}: {score}, clamping to 5")
                        score = 5
                except (ValueError, TypeError):
                    logger.warning(f"Invalid score format for {company}: {score}, using default 5")
                    score = 5
            
            # Extract and validate justification
            justification = fit_data.get('claude_fit_justification')
            if not justification or not str(justification).strip():
                logger.warning(f"No justification found for {company}")
                justification = "Justification not provided by model."
            
            final_data = {
                'claude_fit_score': score,
                'claude_fit_justification': str(justification).strip()
            }
            
            logger.info(f"Successfully analyzed {company}: score={score}")
            return final_data
            
        except anthropic.RateLimitError as e:
            logger.error(f"Rate limit exceeded for {company}: {e}")
            return {"claude_fit_score": 5, "claude_fit_justification": "AI analysis rate limited - please try again later."}
        
        except anthropic.AuthenticationError as e:
            logger.error(f"Authentication error for {company}: {e}")
            return {"claude_fit_score": 5, "claude_fit_justification": "AI analysis authentication failed - check API key."}
        
        except anthropic.APIError as e:
            logger.error(f"API error for {company}: {e}")
            return {"claude_fit_score": 5, "claude_fit_justification": f"AI analysis API error: {str(e)}"}
        
        except Exception as e:
            logger.error(f"Unexpected error analyzing {company}: {e}")
            logger.error(f"Full traceback: {traceback.format_exc()}")
            return {"claude_fit_score": 5, "claude_fit_justification": f"An error occurred during analysis: {str(e)}"}
    
    def _format_data_for_claude(self, startups_data: List[Dict]) -> str:
        """Format startup data in a readable way for Claude."""
        formatted_data = []
        for startup in startups_data:
            # Robustness check to prevent crashes on malformed data
            if not isinstance(startup, dict):
                continue
            
            s_info = {
                "Company": startup.get('company', 'N/A'),
                "Industry": startup.get('industry', 'N/A'),
                "Description": startup.get('solution', 'N/A'),
                "Pain Point": startup.get('pain_point', 'N/A')
            }
            formatted_startup = "\n".join([f"- {key}: {value}" for key, value in s_info.items()])
            formatted_data.append(f"Startup:\n{formatted_startup}")
        
        return "\n\n".join(formatted_data)
    
    def _get_system_prompt(self) -> str:
        """Get the main system prompt for general analysis."""
        return """You are a Claude-powered startup analysis assistant for Anthropic's sales team. 

Your role is to:
1. Analyze startup data to answer questions about trends, patterns, and insights.
2. Identify which startups would benefit most from Claude products.
3. Provide strategic recommendations for sales outreach.
4. Suggest specific Claude features and use cases for each startup.

When asked to generate a sales brief or suggest questions for a specific company, please do so.
Always provide actionable insights that would help a sales team prioritize and engage with prospects.

IMPORTANT: Focus on direct analysis of the provided data. Do not include generic recommendations like "Top candidates for Claude's prompt generation" or similar boilerplate text. Instead, provide specific, contextual insights based on the actual startup data provided."""
    
    def _get_claude_fit_prompt(self) -> str:
        """Get the system prompt for Claude fit analysis."""
        return """You are a Claude product specialist helping to identify the best Claude solutions for startups.

For each startup, analyze:
1. **Claude Product Recommendations**: Which specific Claude products would be most valuable
2. **Feature Mapping**: Which Claude features align with their pain points
3. **Implementation Strategy**: How they could integrate Claude into their workflow
4. **Discovery Questions**: Questions to ask during sales calls to uncover needs
5. **Sample Prompts**: Example Claude prompts they could use immediately

Consider Claude's strengths:
- Long context understanding
- Safe reasoning and compliance
- Structured output generation
- Multi-agent orchestration
- Document analysis and summarization
- Tone control and empathy

Provide specific, actionable recommendations that demonstrate deep understanding of both the startup's needs and Claude's capabilities."""
    
    def _get_sales_brief_prompt(self) -> str:
        """Get the system prompt for sales brief generation."""
        return """You are a senior sales strategist creating outreach briefs for Claude prospects.

For each startup, create:
1. **Email Introduction**: A compelling, personalized email template
2. **Call Talking Points**: Key points to cover in initial discovery calls
3. **Value Propositions**: Specific Claude benefits relevant to their business
4. **Objection Handling**: Common objections and how to address them
5. **Next Steps**: Clear follow-up actions and timeline

Focus on:
- Their specific pain points and how Claude solves them
- Industry-specific use cases and examples
- Technical integration possibilities
- ROI and business impact
- Risk mitigation and safety features

Make the brief practical and ready-to-use for a sales representative.""" 
