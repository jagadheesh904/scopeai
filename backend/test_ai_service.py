import sys
import os
sys.path.append(os.getcwd())

from services.ai_service import AIService

def test_ai_service():
    ai_service = AIService()
    
    test_data = {
        "project_description": "Build a e-commerce website for retail business",
        "industry": "Retail", 
        "project_type": "Web Application",
        "tech_stack": ["React", "Node.js", "MongoDB"],
        "complexity": "medium",
        "compliance": ["GDPR"]
    }
    
    print("Testing AI Service...")
    print(f"Mock mode: {getattr(ai_service, 'mock_mode', 'Unknown')}")
    
    try:
        scope = ai_service.generate_project_scope(**test_data)
        print("✅ Scope generated successfully!")
        print(f"Activities: {len(scope.get('activities', []))}")
        print(f"Timeline: {scope.get('timeline', {}).get('total_weeks', 'N/A')} weeks")
        print(f"Resource roles: {len(scope.get('resource_plan', []))}")
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    test_ai_service()
