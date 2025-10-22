import sys
import os
sys.path.append(os.getcwd())

from models.database import SessionLocal, Project

def fix_existing_projects():
    db = SessionLocal()
    try:
        projects = db.query(Project).all()
        fixed_count = 0
        
        for project in projects:
            needs_update = False
            
            # Fix activities if it's a list instead of dict
            if isinstance(project.activities, list):
                project.activities = {"activities": project.activities}
                needs_update = True
                print(f"Fixed activities for project {project.id}")
            
            # Fix resource_plan if it's a list instead of dict
            if isinstance(project.resource_plan, list):
                project.resource_plan = {"resources": project.resource_plan}
                needs_update = True
                print(f"Fixed resource_plan for project {project.id}")
            
            if needs_update:
                db.commit()
                fixed_count += 1
        
        print(f"Fixed {fixed_count} projects")
        
    except Exception as e:
        print(f"Error fixing projects: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    fix_existing_projects()
