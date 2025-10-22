import google.generativeai as genai
import os
import json
import logging
from typing import Dict, List, Any, Optional
from dotenv import load_dotenv

load_dotenv()

logger = logging.getLogger(__name__)

class ChatbotService:
    def __init__(self):
        api_key = os.getenv("GOOGLE_API_KEY")
        if not api_key:
            logger.warning("GOOGLE_API_KEY not found. Using mock chatbot mode.")
            self.mock_mode = True
            return
        
        try:
            genai.configure(api_key=api_key)
            
            # Try to find available model
            available_models = genai.list_models()
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
                    logger.info(f"Chatbot using model: {model_name}")
                    break
                except Exception as e:
                    logger.warning(f"Failed to load model {model_name}: {str(e)}")
                    continue
            
            if self.model is None:
                logger.warning("Could not load any Gemini model. Using mock chatbot mode.")
                self.mock_mode = True
            else:
                self.mock_mode = False
                
        except Exception as e:
            logger.error(f"Error initializing chatbot: {str(e)}")
            self.mock_mode = True
        
        # System prompt for project scoping focus
        self.system_prompt = """
        You are ScopeAI Assistant, an expert AI assistant specialized in project scoping and planning.
        
        YOUR ROLE:
        - Help users with project scope definition, activity planning, resource allocation, and cost estimation
        - Provide guidance on project management methodologies and best practices
        - Assist with breaking down complex projects into manageable activities
        - Help estimate effort, timelines, and resource requirements
        - Suggest appropriate tech stacks and architectures based on project requirements
        
        RESTRICTIONS:
        - ONLY answer questions related to project scoping, planning, estimation, and management
        - If asked about unrelated topics, politely decline and redirect to project scoping
        - Do not provide advice on non-project-related technical issues, personal matters, or other domains
        - Focus exclusively on software development, IT projects, and digital transformation initiatives
        
        RESPONSE STYLE:
        - Be professional, helpful, and concise
        - Provide practical, actionable advice
        - Use bullet points or numbered lists when appropriate
        - Reference industry best practices and standards
        - If uncertain about specifics, suggest common approaches
        
        Always maintain focus on project scoping and planning topics.
        """
    
    def _is_scope_related(self, question: str) -> bool:
        """Check if the question is related to project scoping"""
        scope_keywords = [
            'project', 'scope', 'planning', 'estimation', 'timeline', 'budget', 'cost',
            'resource', 'team', 'deadline', 'milestone', 'deliverable', 'requirement',
            'specification', 'architecture', 'design', 'development', 'testing',
            'deployment', 'agile', 'waterfall', 'sprint', 'iteration', 'backlog',
            'user story', 'epic', 'task', 'activity', 'effort', 'hour', 'day', 'week',
            'month', 'duration', 'complexity', 'risk', 'dependency', 'constraint',
            'assumption', 'stakeholder', 'client', 'business', 'technical', 'functional',
            'non-functional', 'sprint planning', 'gantt', 'critical path', 'wbs',
            'work breakdown', 'estimation technique', 'plan', 'schedule', 'timeline',
            'resource allocation', 'team structure', 'role', 'responsibility', 'rasci',
            'budgeting', 'cost estimation', 'roi', 'business case', 'feasibility',
            'analysis', 'design', 'implementation', 'maintenance', 'lifecycle', 'sdlc',
            'methodology', 'framework', 'best practice', 'standard', 'guideline',
            'template', 'tool', 'software', 'application', 'system', 'platform',
            'website', 'mobile', 'web', 'cloud', 'database', 'api', 'integration',
            'migration', 'transformation', 'digital', 'automation', 'optimization'
        ]
        
        question_lower = question.lower()
        return any(keyword in question_lower for keyword in scope_keywords)
    
    def _get_mock_response(self, question: str) -> Dict[str, Any]:
        """Get mock response for development when AI is not available"""
        if not self._is_scope_related(question):
            return {
                "response": "I specialize in project scoping and planning. Please ask me about project scope, timelines, resource planning, cost estimation, or related project management topics.",
                "is_scope_related": False
            }
        
        # Provide helpful mock responses for common scoping questions
        mock_responses = {
            "how to estimate project timeline": "For timeline estimation:\n\n1. Break down the project into activities\n2. Estimate effort for each activity\n3. Consider dependencies between activities\n4. Account for resource availability\n5. Add buffer for risks and uncertainties\n6. Use historical data from similar projects\n\nA typical web application takes 12-20 weeks depending on complexity.",
            
            "what should be included in project scope": "A comprehensive project scope should include:\n\n• Project objectives and goals\n• Deliverables and acceptance criteria\n• Features and functionality\n• Technical requirements\n• Constraints and assumptions\n• Timeline and milestones\n• Resource requirements\n• Budget and cost estimates\n• Risks and mitigation strategies",
            
            "how to create a resource plan": "Creating a resource plan:\n\n1. Identify required roles (developers, designers, QA, etc.)\n2. Estimate effort hours for each role\n3. Consider skill levels and experience\n4. Plan for onboarding and knowledge transfer\n5. Account for meetings and administrative tasks\n6. Include contingency for unexpected changes",
            
            "cost estimation techniques": "Common cost estimation techniques:\n\n• **Bottom-up**: Estimate each activity and sum up\n• **Analogous**: Compare with similar past projects\n• **Parametric**: Use statistical models and parameters\n• **Three-point**: Optimistic, pessimistic, most likely estimates\n• **Expert judgment**: Consult domain experts\n\nAlways include contingency (15-25%) for uncertainties."
        }
        
        # Find the best matching mock response
        question_lower = question.lower()
        for key, response in mock_responses.items():
            if key in question_lower:
                return {
                    "response": response,
                    "is_scope_related": True
                }
        
        # Default response for scope-related questions
        return {
            "response": "I'd be happy to help with project scoping! For accurate guidance, please provide more details about:\n\n• Your project type and industry\n• Key requirements and objectives\n• Technical constraints or preferences\n• Timeline expectations\n• Budget considerations\n\nThis will help me provide more specific recommendations for your project scope.",
            "is_scope_related": True
        }
    
    def get_response(self, question: str, context: Dict[str, Any] = None) -> Dict[str, Any]:
        """
        Get AI response for project scoping questions
        """
        # Check if question is scope-related
        if not self._is_scope_related(question):
            return {
                "response": "I specialize exclusively in project scoping and planning topics. Please ask me about:\n\n• Project scope definition\n• Activity planning and breakdown\n• Resource allocation and team structure\n• Timeline and milestone planning\n• Cost estimation and budgeting\n• Risk assessment and mitigation\n• Project methodology selection\n\nI'll be happy to help with any of these project scoping areas!",
                "is_scope_related": False
            }
        
        # Use mock responses if AI is not available
        if hasattr(self, 'mock_mode') and self.mock_mode:
            return self._get_mock_response(question)
        
        try:
            # Build context-aware prompt
            prompt = f"""
            {self.system_prompt}
            
            User Question: {question}
            
            {"Project Context: " + json.dumps(context, indent=2) if context else "No specific project context provided."}
            
            Please provide a helpful, professional response focused on project scoping and planning.
            """
            
            response = self.model.generate_content(prompt)
            response_text = response.text.strip()
            
            return {
                "response": response_text,
                "is_scope_related": True
            }
            
        except Exception as e:
            logger.error(f"Error getting chatbot response: {str(e)}")
            # Fall back to mock response
            return self._get_mock_response(question)

# Singleton instance
chatbot_service = ChatbotService()
