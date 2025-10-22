import chromadb
import os
import json
import logging
from typing import List, Dict, Any, Optional
from models.database import SessionLocal, HistoricalProject, ActivityTemplate

logger = logging.getLogger(__name__)

class VectorDBService:
    def __init__(self):
        self.db_path = os.getenv("CHROMA_DB_PATH", "./data/chroma_db")
        self.client = chromadb.PersistentClient(path=self.db_path)
        
        # Create collections
        self.historical_projects_collection = self.client.get_or_create_collection(
            name="historical_projects",
            metadata={"description": "Historical project data for RAG"}
        )
        
        self.activity_templates_collection = self.client.get_or_create_collection(
            name="activity_templates", 
            metadata={"description": "Activity templates for project scoping"}
        )
        
        self._initialize_with_sample_data()
    
    def _initialize_with_sample_data(self):
        """Initialize with sample historical data and templates"""
        # Check if collections are empty
        if self.historical_projects_collection.count() == 0:
            self._add_sample_historical_projects()
        
        if self.activity_templates_collection.count() == 0:
            self._add_sample_activity_templates()
    
    def _add_sample_historical_projects(self):
        """Add sample historical project data"""
        sample_projects = [
            {
                "id": "1",
                "name": "E-commerce Platform Migration",
                "industry": "Retail",
                "project_type": "Platform Migration",
                "actual_effort": {"Project Manager": 200, "Frontend Developer": 400, "Backend Developer": 600, "QA Engineer": 300},
                "actual_timeline": {"weeks": 16, "milestones": ["Discovery Complete", "Development Complete", "QA Complete", "Launch"]},
                "content": "Migrated legacy e-commerce platform to modern microservices architecture"
            },
            {
                "id": "2", 
                "name": "Healthcare Data Analytics",
                "industry": "Healthcare",
                "project_type": "Data Analytics",
                "actual_effort": {"Data Scientist": 500, "Data Engineer": 400, "ML Engineer": 300, "DevOps Engineer": 200},
                "actual_timeline": {"weeks": 20, "milestones": ["Data Pipeline Complete", "Model Development", "Validation Complete", "Deployment"]},
                "content": "Built healthcare data analytics platform with predictive modeling"
            }
        ]
        
        for project in sample_projects:
            self.historical_projects_collection.add(
                documents=[project["content"]],
                metadatas=[{
                    "name": project["name"],
                    "industry": project["industry"],
                    "project_type": project["project_type"],
                    "effort": json.dumps(project["actual_effort"]),
                    "timeline": json.dumps(project["actual_timeline"])
                }],
                ids=[project["id"]]
            )
    
    def _add_sample_activity_templates(self):
        """Add sample activity templates"""
        sample_templates = [
            {
                "id": "1",
                "name": "Requirements Gathering",
                "phase": "Discovery & Design",
                "description": "Conduct workshops to gather and document business and technical requirements",
                "effort_hours": 40,
                "dependencies": [],
                "required_roles": ["Business Analyst", "Project Manager"],
                "content": "Requirements gathering workshop facilitation and documentation"
            },
            {
                "id": "2",
                "name": "API Development",
                "phase": "Development", 
                "description": "Design and implement RESTful APIs with proper documentation",
                "effort_hours": 120,
                "dependencies": ["Technical Design", "Database Design"],
                "required_roles": ["Backend Developer", "API Designer"],
                "content": "RESTful API development with documentation and testing"
            }
        ]
        
        for template in sample_templates:
            self.activity_templates_collection.add(
                documents=[template["content"]],
                metadatas=[{
                    "name": template["name"],
                    "phase": template["phase"],
                    "description": template["description"],
                    "effort_hours": template["effort_hours"],
                    "dependencies": json.dumps(template["dependencies"]),
                    "required_roles": json.dumps(template["required_roles"])
                }],
                ids=[template["id"]]
            )
    
    def find_similar_projects(self, query: str, industry: str, n_results: int = 3) -> List[Dict[str, Any]]:
        """Find similar historical projects using vector search"""
        try:
            results = self.historical_projects_collection.query(
                query_texts=[query],
                n_results=n_results,
                where={"industry": industry} if industry else None
            )
            
            similar_projects = []
            for i, (doc, metadata) in enumerate(zip(results['documents'][0], results['metadatas'][0])):
                similar_projects.append({
                    "name": metadata["name"],
                    "industry": metadata["industry"],
                    "project_type": metadata["project_type"],
                    "actual_effort": json.loads(metadata["effort"]),
                    "actual_timeline": json.loads(metadata["timeline"]),
                    "content": doc
                })
            
            return similar_projects
        except Exception as e:
            logger.error(f"Error finding similar projects: {str(e)}")
            return []
    
    def get_relevant_templates(self, query: str, phase: str = None) -> List[Dict[str, Any]]:
        """Get relevant activity templates using vector search"""
        try:
            where_clause = {"phase": phase} if phase else None
            results = self.activity_templates_collection.query(
                query_texts=[query],
                n_results=10,
                where=where_clause
            )
            
            templates = []
            for i, (doc, metadata) in enumerate(zip(results['documents'][0], results['metadatas'][0])):
                templates.append({
                    "name": metadata["name"],
                    "phase": metadata["phase"],
                    "description": metadata["description"],
                    "effort_hours": metadata["effort_hours"],
                    "dependencies": json.loads(metadata["dependencies"]),
                    "required_roles": json.loads(metadata["required_roles"])
                })
            
            return templates
        except Exception as e:
            logger.error(f"Error getting relevant templates: {str(e)}")
            return []

# Singleton instance
vector_db_service = VectorDBService()
