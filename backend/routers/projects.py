from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional, Any, Dict
from pydantic import BaseModel
import json
from datetime import datetime
import logging

from models.database import get_db, Project, User
from routers.auth import get_current_user

router = APIRouter()
logger = logging.getLogger(__name__)

class ProjectCreate(BaseModel):
    name: str
    description: str
    industry: str
    project_type: str
    tech_stack: List[str]
    complexity: str
    compliance_requirements: List[str]
    duration_weeks: int

class ProjectUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    industry: Optional[str] = None
    project_type: Optional[str] = None
    tech_stack: Optional[List[str]] = None
    complexity: Optional[str] = None
    compliance_requirements: Optional[List[str]] = None
    duration_weeks: Optional[int] = None
    activities: Optional[Dict[str, Any]] = None
    timeline: Optional[Dict[str, Any]] = None
    resource_plan: Optional[Dict[str, Any]] = None
    cost_estimate: Optional[Dict[str, Any]] = None
    status: Optional[str] = None

class ProjectResponse(BaseModel):
    id: int
    name: str
    description: str
    industry: str
    project_type: str
    tech_stack: List[str]
    complexity: str
    compliance_requirements: List[str]
    duration_weeks: int
    status: str
    activities: Optional[Dict[str, Any]] = None
    timeline: Optional[Dict[str, Any]] = None
    resource_plan: Optional[Dict[str, Any]] = None
    cost_estimate: Optional[Dict[str, Any]] = None
    created_by: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True

@router.post("/", response_model=ProjectResponse)
def create_project(
    project: ProjectCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    try:
        logger.info(f"Creating project for user {current_user.id}: {project.name}")
        
        # Convert to dict and ensure JSON serializable data
        project_data = project.dict()
        
        db_project = Project(
            **project_data,
            created_by=current_user.id,
            activities={},  # Changed from [] to {}
            timeline={},
            resource_plan={},  # Changed from [] to {}
            cost_estimate={},
            status="draft"
        )
        
        db.add(db_project)
        db.commit()
        db.refresh(db_project)
        
        logger.info(f"Project created successfully with ID: {db_project.id}")
        return db_project
        
    except Exception as e:
        db.rollback()
        logger.error(f"Error creating project: {str(e)}")
        logger.error(f"Project data: {project.dict()}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to create project: {str(e)}"
        )

@router.get("/", response_model=List[ProjectResponse])
def get_projects(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    try:
        projects = db.query(Project).filter(Project.created_by == current_user.id).offset(skip).limit(limit).all()
        return projects
    except Exception as e:
        logger.error(f"Error fetching projects: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to fetch projects"
        )

@router.get("/{project_id}", response_model=ProjectResponse)
def get_project(
    project_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    try:
        project = db.query(Project).filter(Project.id == project_id, Project.created_by == current_user.id).first()
        if not project:
            raise HTTPException(status_code=404, detail="Project not found")
        return project
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error fetching project {project_id}: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to fetch project"
        )

@router.put("/{project_id}", response_model=ProjectResponse)
def update_project(
    project_id: int,
    project_update: ProjectUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    try:
        project = db.query(Project).filter(Project.id == project_id, Project.created_by == current_user.id).first()
        if not project:
            raise HTTPException(status_code=404, detail="Project not found")
        
        update_data = project_update.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(project, field, value)
        
        project.updated_at = datetime.utcnow()
        db.commit()
        db.refresh(project)
        return project
        
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        logger.error(f"Error updating project {project_id}: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to update project"
        )

@router.delete("/{project_id}")
def delete_project(
    project_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    try:
        project = db.query(Project).filter(Project.id == project_id, Project.created_by == current_user.id).first()
        if not project:
            raise HTTPException(status_code=404, detail="Project not found")
        
        db.delete(project)
        db.commit()
        return {"message": "Project deleted successfully"}
        
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        logger.error(f"Error deleting project {project_id}: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to delete project"
        )
