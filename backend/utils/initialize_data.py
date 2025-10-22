import sys
import os

# Add the parent directory to Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from models.database import create_db_and_tables, SessionLocal, BillingRate, ActivityTemplate
import json

def initialize_sample_data():
    # First, create all database tables
    create_db_and_tables()
    print("✅ Database tables created")
    
    db = SessionLocal()
    
    try:
        # Initialize billing rates
        if db.query(BillingRate).count() == 0:
            billing_rates = [
                {"role": "Project Manager", "rate_per_hour": 150},
                {"role": "Business Analyst", "rate_per_hour": 120},
                {"role": "Solution Architect", "rate_per_hour": 180},
                {"role": "Frontend Developer", "rate_per_hour": 130},
                {"role": "Backend Developer", "rate_per_hour": 140},
                {"role": "Full Stack Developer", "rate_per_hour": 145},
                {"role": "DevOps Engineer", "rate_per_hour": 150},
                {"role": "QA Engineer", "rate_per_hour": 110},
                {"role": "Data Scientist", "rate_per_hour": 160},
                {"role": "Data Engineer", "rate_per_hour": 150},
                {"role": "ML Engineer", "rate_per_hour": 170},
                {"role": "UI/UX Designer", "rate_per_hour": 125},
                {"role": "Security Engineer", "rate_per_hour": 175}
            ]
            
            for rate_data in billing_rates:
                rate = BillingRate(**rate_data)
                db.add(rate)
            
            db.commit()
            print("✅ Billing rates initialized")
        else:
            print("✅ Billing rates already exist")
        
        # Initialize activity templates
        if db.query(ActivityTemplate).count() == 0:
            activity_templates = [
                {
                    "name": "Stakeholder Interviews",
                    "description": "Conduct interviews with key stakeholders to gather business requirements",
                    "phase": "Discovery & Design",
                    "effort_hours_min": 16,
                    "effort_hours_max": 40,
                    "dependencies": [],
                    "required_roles": ["Business Analyst", "Project Manager"],
                    "industry_focus": ["all"],
                    "tech_stack_relevance": ["all"]
                },
                {
                    "name": "Technical Architecture Design",
                    "description": "Design the technical architecture and solution blueprint",
                    "phase": "Discovery & Design", 
                    "effort_hours_min": 40,
                    "effort_hours_max": 80,
                    "dependencies": ["Stakeholder Interviews"],
                    "required_roles": ["Solution Architect", "Technical Lead"],
                    "industry_focus": ["all"],
                    "tech_stack_relevance": ["all"]
                },
                {
                    "name": "Frontend Development",
                    "description": "Develop user interface components and frontend application",
                    "phase": "Development",
                    "effort_hours_min": 80,
                    "effort_hours_max": 200,
                    "dependencies": ["Technical Architecture Design", "UI/UX Design"],
                    "required_roles": ["Frontend Developer", "UI/UX Designer"],
                    "industry_focus": ["all"],
                    "tech_stack_relevance": ["React", "Angular", "Vue", "JavaScript"]
                },
                {
                    "name": "API Development",
                    "description": "Develop backend APIs and services",
                    "phase": "Development",
                    "effort_hours_min": 100,
                    "effort_hours_max": 240,
                    "dependencies": ["Technical Architecture Design", "Database Design"],
                    "required_roles": ["Backend Developer", "API Designer"],
                    "industry_focus": ["all"],
                    "tech_stack_relevance": ["Node.js", "Python", "Java", "C#", "Go"]
                },
                {
                    "name": "Unit Testing",
                    "description": "Write and execute unit tests for developed components",
                    "phase": "Testing & QA", 
                    "effort_hours_min": 40,
                    "effort_hours_max": 100,
                    "dependencies": ["Frontend Development", "API Development"],
                    "required_roles": ["QA Engineer", "Developer"],
                    "industry_focus": ["all"],
                    "tech_stack_relevance": ["all"]
                },
                {
                    "name": "Integration Testing",
                    "description": "Test integration between different system components",
                    "phase": "Testing & QA",
                    "effort_hours_min": 24,
                    "effort_hours_max": 60,
                    "dependencies": ["Unit Testing"],
                    "required_roles": ["QA Engineer", "Integration Specialist"],
                    "industry_focus": ["all"],
                    "tech_stack_relevance": ["all"]
                },
                {
                    "name": "Production Deployment",
                    "description": "Deploy application to production environment",
                    "phase": "Deployment",
                    "effort_hours_min": 16,
                    "effort_hours_max": 32,
                    "dependencies": ["Integration Testing", "Security Testing"],
                    "required_roles": ["DevOps Engineer", "Release Manager"],
                    "industry_focus": ["all"],
                    "tech_stack_relevance": ["all"]
                },
                {
                    "name": "Post-Launch Support",
                    "description": "Provide support and maintenance after launch",
                    "phase": "Post-Launch Support",
                    "effort_hours_min": 40,
                    "effort_hours_max": 160,
                    "dependencies": ["Production Deployment"],
                    "required_roles": ["Support Engineer", "DevOps Engineer"],
                    "industry_focus": ["all"],
                    "tech_stack_relevance": ["all"]
                }
            ]
            
            for template_data in activity_templates:
                template = ActivityTemplate(**template_data)
                db.add(template)
            
            db.commit()
            print("✅ Activity templates initialized")
        else:
            print("✅ Activity templates already exist")
        
        print("✅ Sample data initialization completed successfully!")
        
    except Exception as e:
        print(f"❌ Error initializing sample data: {str(e)}")
        import traceback
        traceback.print_exc()
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    initialize_sample_data()
