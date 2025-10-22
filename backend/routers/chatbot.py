from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import Dict, Any, Optional
import logging

from models.database import get_db, Project, User
from routers.auth import get_current_user
from services.chatbot_service import chatbot_service

router = APIRouter()
logger = logging.getLogger(__name__)

class ChatMessage(BaseModel):
    message: str
    project_id: Optional[int] = None

class ChatResponse(BaseModel):
    response: str
    is_scope_related: bool

@router.post("/chat", response_model=ChatResponse)
async def chat_with_bot(
    chat_message: ChatMessage,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    try:
        # Build context if project_id is provided
        context = None
        if chat_message.project_id:
            project = db.query(Project).filter(
                Project.id == chat_message.project_id, 
                Project.created_by == current_user.id
            ).first()
            
            if project:
                context = {
                    "project_name": project.name,
                    "industry": project.industry,
                    "project_type": project.project_type,
                    "tech_stack": project.tech_stack,
                    "complexity": project.complexity,
                    "duration_weeks": project.duration_weeks,
                    "description": project.description
                }
        
        # Get response from chatbot service
        result = chatbot_service.get_response(chat_message.message, context)
        
        logger.info(f"Chatbot response generated for user {current_user.id}")
        return result
        
    except Exception as e:
        logger.error(f"Error in chatbot: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Chatbot error: {str(e)}")

@router.get("/suggestions")
async def get_chat_suggestions():
    """Get suggested questions for the chatbot"""
    suggestions = [
        "How do I estimate project timeline?",
        "What should be included in project scope?",
        "How to create a resource plan?",
        "What are common cost estimation techniques?",
        "How to break down a complex project?",
        "What roles are needed for a software project?",
        "How to identify project risks?",
        "What's the difference between agile and waterfall?",
        "How to create a work breakdown structure?",
        "What are typical project milestones?"
    ]
    
    return {"suggestions": suggestions}
