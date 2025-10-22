import sys
import os
sys.path.append(os.getcwd())

from models.database import SessionLocal, engine, Project, User
from sqlalchemy import inspect

def check_schema():
    inspector = inspect(engine)
    
    print("=== Database Tables ===")
    tables = inspector.get_table_names()
    for table in tables:
        print(f"Table: {table}")
        columns = inspector.get_columns(table)
        for column in columns:
            print(f"  - {column['name']}: {column['type']}")
        print()
    
    # Check if we can create a session
    db = SessionLocal()
    try:
        user_count = db.query(User).count()
        project_count = db.query(Project).count()
        print(f"Users in database: {user_count}")
        print(f"Projects in database: {project_count}")
    except Exception as e:
        print(f"Error querying database: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    check_schema()
