from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import List, Dict, Any
import logging

from models.database import get_db, Project, BillingRate, User
from routers.auth import get_current_user
from services.ai_service import ai_service
from services.vector_db import vector_db_service

router = APIRouter()
logger = logging.getLogger(__name__)

class ScopeGenerationRequest(BaseModel):
    project_id: int
    project_description: str
    industry: str
    project_type: str
    tech_stack: List[str]
    complexity: str
    compliance_requirements: List[str]

class ScopeAdjustmentRequest(BaseModel):
    project_id: int
    feedback: str

@router.post("/generate-draft")
async def generate_draft_scope(
    request: ScopeGenerationRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    try:
        # Get project
        project = db.query(Project).filter(
            Project.id == request.project_id, 
            Project.created_by == current_user.id
        ).first()
        
        if not project:
            raise HTTPException(status_code=404, detail="Project not found")
        
        # Get similar historical projects for context
        similar_projects = vector_db_service.find_similar_projects(
            query=request.project_description,
            industry=request.industry
        )
        
        logger.info(f"Found {len(similar_projects)} similar historical projects")
        
        # Generate scope using AI or mock data
        scope_data = ai_service.generate_project_scope(
            project_description=request.project_description,
            industry=request.industry,
            project_type=request.project_type,
            tech_stack=request.tech_stack,
            complexity=request.complexity,
            compliance=request.compliance_requirements
        )
        
        # Apply billing rates to cost estimate
        billing_rates = db.query(BillingRate).all()
        rate_map = {rate.role: rate.rate_per_hour for rate in billing_rates}
        
        # Always recalculate cost to ensure consistency with database rates
        total_cost = 0
        cost_breakdown = []
        
        # Calculate cost from resource plan
        resource_plan_data = scope_data.get("resource_plan", [])
        if isinstance(resource_plan_data, dict) and "resources" in resource_plan_data:
            resource_plan_data = resource_plan_data["resources"]
        
        for resource in resource_plan_data:
            role = resource["role"]
            hours = resource["total_hours"]
            rate = rate_map.get(role, 100)  # Default rate if role not found
            cost = hours * rate
            
            cost_breakdown.append({
                "role": role,
                "hours": hours,
                "rate": rate,
                "cost": cost
            })
            total_cost += cost
        
        # Update the cost estimate in scope data
        scope_data["cost_estimate"] = {
            "total_cost": total_cost,
            "breakdown": cost_breakdown
        }
        
        # Ensure proper data types for the response model
        # Convert lists to dictionaries if needed
        if "activities" in scope_data and isinstance(scope_data["activities"], list):
            scope_data["activities"] = {"activities": scope_data["activities"]}
        
        if "resource_plan" in scope_data and isinstance(scope_data["resource_plan"], list):
            scope_data["resource_plan"] = {"resources": scope_data["resource_plan"]}
        
        # Update project with generated scope
        project.activities = scope_data.get("activities", {})
        project.timeline = scope_data.get("timeline", {})
        project.resource_plan = scope_data.get("resource_plan", {})
        project.cost_estimate = scope_data.get("cost_estimate", {})
        project.status = "draft"
        
        db.commit()
        
        # Add mock mode indicator to response
        response_data = {
            "message": "Scope generated successfully",
            "scope": scope_data,
            "similar_projects": similar_projects
        }
        
        if hasattr(ai_service, 'mock_mode') and ai_service.mock_mode:
            response_data["message"] = "Scope generated successfully (using demo data)"
            response_data["mock_mode"] = True
        
        return response_data
        
    except Exception as e:
        logger.error(f"Error generating draft scope: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to generate scope: {str(e)}")

@router.post("/adjust-scope")
async def adjust_scope(
    request: ScopeAdjustmentRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    try:
        # Get project
        project = db.query(Project).filter(
            Project.id == request.project_id, 
            Project.created_by == current_user.id
        ).first()
        
        if not project:
            raise HTTPException(status_code=404, detail="Project not found")
        
        if not project.activities:
            raise HTTPException(status_code=400, detail="No existing scope to adjust")
        
        # Adjust scope based on feedback
        original_scope = {
            "activities": project.activities,
            "timeline": project.timeline,
            "resource_plan": project.resource_plan,
            "cost_estimate": project.cost_estimate
        }
        
        adjusted_scope = ai_service.adjust_scope_based_on_feedback(
            original_scope=original_scope,
            feedback=request.feedback
        )
        
        # Ensure proper data types
        if "activities" in adjusted_scope and isinstance(adjusted_scope["activities"], list):
            adjusted_scope["activities"] = {"activities": adjusted_scope["activities"]}
        
        if "resource_plan" in adjusted_scope and isinstance(adjusted_scope["resource_plan"], list):
            adjusted_scope["resource_plan"] = {"resources": adjusted_scope["resource_plan"]}
        
        # Recalculate costs for adjusted scope
        billing_rates = db.query(BillingRate).all()
        rate_map = {rate.role: rate.rate_per_hour for rate in billing_rates}
        
        total_cost = 0
        cost_breakdown = []
        
        resource_plan_data = adjusted_scope.get("resource_plan", [])
        if isinstance(resource_plan_data, dict) and "resources" in resource_plan_data:
            resource_plan_data = resource_plan_data["resources"]
        
        for resource in resource_plan_data:
            role = resource["role"]
            hours = resource["total_hours"]
            rate = rate_map.get(role, 100)
            cost = hours * rate
            
            cost_breakdown.append({
                "role": role,
                "hours": hours,
                "rate": rate,
                "cost": cost
            })
            total_cost += cost
        
        adjusted_scope["cost_estimate"] = {
            "total_cost": total_cost,
            "breakdown": cost_breakdown
        }
        
        # Update project with adjusted scope
        project.activities = adjusted_scope.get("activities", {})
        project.timeline = adjusted_scope.get("timeline", {})
        project.resource_plan = adjusted_scope.get("resource_plan", {})
        project.cost_estimate = adjusted_scope.get("cost_estimate", {})
        
        db.commit()
        
        response_data = {
            "message": "Scope adjusted successfully",
            "scope": adjusted_scope
        }
        
        if hasattr(ai_service, 'mock_mode') and ai_service.mock_mode:
            response_data["message"] = "Scope adjusted successfully (using demo data)"
            response_data["mock_mode"] = True
        
        return response_data
        
    except Exception as e:
        logger.error(f"Error adjusting scope: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to adjust scope: {str(e)}")

@router.get("/similar-projects")
async def get_similar_projects(
    industry: str,
    project_type: str,
    current_user: User = Depends(get_current_user)
):
    try:
        query = f"{industry} {project_type} project"
        similar_projects = vector_db_service.find_similar_projects(
            query=query,
            industry=industry
        )
        
        return {
            "similar_projects": similar_projects
        }
        
    except Exception as e:
        logger.error(f"Error finding similar projects: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to find similar projects: {str(e)}")
