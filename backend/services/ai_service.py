import google.generativeai as genai
import os
import json
import logging
from typing import Dict, List, Any, Optional
from dotenv import load_dotenv

load_dotenv()

logger = logging.getLogger(__name__)

class AIService:
    def __init__(self):
        api_key = os.getenv("GOOGLE_API_KEY")
        if not api_key:
            logger.warning("GOOGLE_API_KEY not found in environment variables. Using mock data for development.")
            self.mock_mode = True
            return
        
        try:
            genai.configure(api_key=api_key)
            
            # List available models to see what's accessible
            available_models = genai.list_models()
            logger.info(f"Available models: {[model.name for model in available_models]}")
            
            # Try to use the available model - common names for Gemini
            model_names_to_try = [
                'models/gemini-pro',
                'models/gemini-1.0-pro',
                'gemini-pro',
                'gemini-1.0-pro'
            ]
            
            self.model = None
            for model_name in model_names_to_try:
                try:
                    self.model = genai.GenerativeModel(model_name)
                    logger.info(f"Successfully loaded model: {model_name}")
                    break
                except Exception as e:
                    logger.warning(f"Failed to load model {model_name}: {str(e)}")
                    continue
            
            if self.model is None:
                logger.warning("Could not load any Gemini model. Using mock mode.")
                self.mock_mode = True
            else:
                self.mock_mode = False
                
        except Exception as e:
            logger.error(f"Error initializing AI service: {str(e)}")
            self.mock_mode = True
        
        # Initialize with project scoping context
        self.system_prompt = """
        You are ScopeAI, an expert project scoping assistant for Sigmoid. 
        Your role is to analyze project requirements and generate comprehensive project scopes including:
        - Activity breakdown with dependencies
        - Resource allocation by role
        - Timeline with milestones
        - Cost estimates
        
        Always respond in structured JSON format.
        """
    
    def _generate_mock_scope(self, project_description: str, industry: str, 
                           project_type: str, tech_stack: List[str], 
                           complexity: str, compliance: List[str]) -> Dict[str, Any]:
        """Generate mock project scope for development when AI is not available"""
        logger.info("Generating mock project scope")
        
        # Base effort multipliers based on complexity
        complexity_multiplier = {
            "low": 0.7,
            "medium": 1.0,
            "high": 1.5
        }
        
        multiplier = complexity_multiplier.get(complexity, 1.0)
        
        # Define billing rates for roles
        billing_rates = {
            "Project Manager": 150,
            "Business Analyst": 120,
            "Solution Architect": 180,
            "Frontend Developer": 130,
            "Backend Developer": 140,
            "UI/UX Designer": 125,
            "QA Engineer": 110,
            "DevOps Engineer": 150,
            "Technical Lead": 160,
            "API Developer": 140,
            "Test Analyst": 100,
            "Release Manager": 145,
            "Support Engineer": 120
        }
        
        # Define resource plan with hours
        resource_plan = [
            {"role": "Project Manager", "total_hours": int(80 * multiplier)},
            {"role": "Business Analyst", "total_hours": int(60 * multiplier)},
            {"role": "Solution Architect", "total_hours": int(60 * multiplier)},
            {"role": "Frontend Developer", "total_hours": int(120 * multiplier)},
            {"role": "Backend Developer", "total_hours": int(160 * multiplier)},
            {"role": "UI/UX Designer", "total_hours": int(40 * multiplier)},
            {"role": "QA Engineer", "total_hours": int(80 * multiplier)},
            {"role": "DevOps Engineer", "total_hours": int(40 * multiplier)}
        ]
        
        # Calculate cost breakdown
        cost_breakdown = []
        total_cost = 0
        
        for resource in resource_plan:
            role = resource["role"]
            hours = resource["total_hours"]
            rate = billing_rates.get(role, 100)
            cost = hours * rate
            
            cost_breakdown.append({
                "role": role,
                "hours": hours,
                "rate": rate,
                "cost": cost
            })
            total_cost += cost
        
        mock_scope = {
            "activities": [
                {
                    "phase": "Discovery & Design",
                    "name": "Requirements Gathering",
                    "description": "Conduct workshops to gather business and technical requirements",
                    "effort_hours": int(40 * multiplier),
                    "dependencies": [],
                    "required_roles": ["Business Analyst", "Project Manager"]
                },
                {
                    "phase": "Discovery & Design", 
                    "name": "Technical Architecture",
                    "description": "Design the system architecture and technical blueprint",
                    "effort_hours": int(60 * multiplier),
                    "dependencies": ["Requirements Gathering"],
                    "required_roles": ["Solution Architect", "Technical Lead"]
                },
                {
                    "phase": "Development",
                    "name": "Frontend Development",
                    "description": "Develop user interface and frontend components",
                    "effort_hours": int(120 * multiplier),
                    "dependencies": ["Technical Architecture"],
                    "required_roles": ["Frontend Developer", "UI/UX Designer"]
                },
                {
                    "phase": "Development",
                    "name": "Backend Development", 
                    "description": "Develop server-side logic and APIs",
                    "effort_hours": int(160 * multiplier),
                    "dependencies": ["Technical Architecture"],
                    "required_roles": ["Backend Developer", "API Developer"]
                },
                {
                    "phase": "Testing & QA",
                    "name": "Quality Assurance",
                    "description": "Comprehensive testing including unit, integration, and user acceptance testing",
                    "effort_hours": int(80 * multiplier),
                    "dependencies": ["Frontend Development", "Backend Development"],
                    "required_roles": ["QA Engineer", "Test Analyst"]
                },
                {
                    "phase": "Deployment",
                    "name": "Production Deployment",
                    "description": "Deploy application to production environment",
                    "effort_hours": int(24 * multiplier),
                    "dependencies": ["Quality Assurance"],
                    "required_roles": ["DevOps Engineer", "Release Manager"]
                },
                {
                    "phase": "Post-Launch Support",
                    "name": "Post-Launch Support",
                    "description": "Provide support and maintenance after launch",
                    "effort_hours": int(40 * multiplier),
                    "dependencies": ["Production Deployment"],
                    "required_roles": ["Support Engineer", "DevOps Engineer"]
                }
            ],
            "resource_plan": resource_plan,
            "timeline": {
                "total_weeks": max(8, int(16 * multiplier)),
                "milestones": [
                    {"name": "Requirements Complete", "week": 2},
                    {"name": "Design Complete", "week": 4},
                    {"name": "Development Complete", "week": 10},
                    {"name": "Testing Complete", "week": 14},
                    {"name": "Production Launch", "week": 16}
                ]
            },
            "cost_estimate": {
                "total_cost": total_cost,
                "breakdown": cost_breakdown
            }
        }
        
        return mock_scope
    
    def generate_project_scope(self, project_description: str, industry: str, 
                             project_type: str, tech_stack: List[str], 
                             complexity: str, compliance: List[str]) -> Dict[str, Any]:
        """
        Generate complete project scope using AI or mock data
        """
        # If in mock mode or no API key, use mock data
        if hasattr(self, 'mock_mode') and self.mock_mode:
            return self._generate_mock_scope(project_description, industry, project_type, tech_stack, complexity, compliance)
        
        prompt = f"""
        {self.system_prompt}
        
        Project Requirements:
        - Description: {project_description}
        - Industry: {industry}
        - Project Type: {project_type}
        - Tech Stack: {', '.join(tech_stack)}
        - Complexity: {complexity}
        - Compliance: {', '.join(compliance)}
        
        Please generate a comprehensive project scope including:
        
        1. Activity Breakdown (grouped by phases):
           - Discovery & Design
           - Development
           - Testing & QA
           - Deployment
           - Post-Launch Support
        
        2. For each activity include:
           - Name
           - Description
           - Estimated effort in hours
           - Dependencies (other activities that must complete first)
           - Required roles
        
        3. Resource Plan with roles and total effort
        
        4. Timeline with milestones and sequencing
        
        5. Cost estimate based on standard billing rates
        
        Return ONLY valid JSON with this structure:
        {{
            "activities": [
                {{
                    "phase": "string",
                    "name": "string", 
                    "description": "string",
                    "effort_hours": number,
                    "dependencies": ["string"],
                    "required_roles": ["string"]
                }}
            ],
            "resource_plan": [
                {{
                    "role": "string",
                    "total_hours": number
                }}
            ],
            "timeline": {{
                "total_weeks": number,
                "milestones": [
                    {{
                        "name": "string",
                        "week": number
                    }}
                ]
            }},
            "cost_estimate": {{
                "total_cost": number,
                "breakdown": [
                    {{
                        "role": "string",
                        "hours": number,
                        "rate": number,
                        "cost": number
                    }}
                ]
            }}
        }}
        """
        
        try:
            response = self.model.generate_content(prompt)
            response_text = response.text.strip()
            
            # Clean the response (remove markdown code blocks if present)
            if response_text.startswith('```json'):
                response_text = response_text[7:]
            if response_text.endswith('```'):
                response_text = response_text[:-3]
            
            scope_data = json.loads(response_text)
            logger.info("Successfully generated project scope using AI")
            return scope_data
            
        except Exception as e:
            logger.error(f"Error generating project scope with AI: {str(e)}")
            logger.info("Falling back to mock data")
            return self._generate_mock_scope(project_description, industry, project_type, tech_stack, complexity, compliance)
    
    def adjust_scope_based_on_feedback(self, original_scope: Dict[str, Any], 
                                     feedback: str) -> Dict[str, Any]:
        """
        Adjust scope based on user feedback
        """
        # If in mock mode, just return the original scope with a note
        if hasattr(self, 'mock_mode') and self.mock_mode:
            logger.info("Mock mode: Returning original scope with feedback note")
            adjusted_scope = original_scope.copy()
            if "activities" in adjusted_scope:
                for activity in adjusted_scope["activities"]:
                    if "description" in activity:
                        activity["description"] += f" [Adjusted based on: {feedback}]"
            return adjusted_scope
        
        prompt = f"""
        {self.system_prompt}
        
        Original Scope: {json.dumps(original_scope, indent=2)}
        
        User Feedback: {feedback}
        
        Please adjust the project scope based on the feedback while maintaining consistency.
        Return the updated scope in the same JSON format.
        """
        
        try:
            response = self.model.generate_content(prompt)
            response_text = response.text.strip()
            
            if response_text.startswith('```json'):
                response_text = response_text[7:]
            if response_text.endswith('```'):
                response_text = response_text[:-3]
            
            updated_scope = json.loads(response_text)
            logger.info("Successfully adjusted project scope based on feedback")
            return updated_scope
            
        except Exception as e:
            logger.error(f"Error adjusting project scope: {str(e)}")
            logger.info("Returning original scope due to adjustment error")
            return original_scope

# Singleton instance
ai_service = AIService()
