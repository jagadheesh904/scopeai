from sqlalchemy import create_engine, Column, Integer, String, Float, Text, Boolean, DateTime, JSON, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.sql import func
import os
from dotenv import load_dotenv

load_dotenv()

SQLALCHEMY_DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./scopeai.db")

engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False} if SQLALCHEMY_DATABASE_URL.startswith("sqlite") else {})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    full_name = Column(String)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class Project(Base):
    __tablename__ = "projects"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    description = Column(Text)
    industry = Column(String)
    project_type = Column(String)
    tech_stack = Column(JSON)
    complexity = Column(String)  # low, medium, high
    compliance_requirements = Column(JSON)
    duration_weeks = Column(Integer)
    status = Column(String, default="draft")  # draft, in_review, finalized
    
    # Generated scope data
    activities = Column(JSON)
    timeline = Column(JSON)
    resource_plan = Column(JSON)
    cost_estimate = Column(JSON)
    
    created_by = Column(Integer, ForeignKey("users.id"))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

class ActivityTemplate(Base):
    __tablename__ = "activity_templates"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    description = Column(Text)
    phase = Column(String)  # discovery, design, development, testing, deployment, support
    effort_hours_min = Column(Float)
    effort_hours_max = Column(Float)
    dependencies = Column(JSON)  # List of activity IDs this depends on
    required_roles = Column(JSON)  # List of roles needed
    industry_focus = Column(JSON)  # Specific industries this applies to
    tech_stack_relevance = Column(JSON)  # Tech stacks this applies to

class HistoricalProject(Base):
    __tablename__ = "historical_projects"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    industry = Column(String)
    project_type = Column(String)
    actual_effort = Column(JSON)  # {role: hours}
    actual_timeline = Column(JSON)
    lessons_learned = Column(Text)
    success_metrics = Column(JSON)

class BillingRate(Base):
    __tablename__ = "billing_rates"
    
    id = Column(Integer, primary_key=True, index=True)
    role = Column(String, unique=True, index=True)
    rate_per_hour = Column(Float)
    currency = Column(String, default="USD")

def create_db_and_tables():
    Base.metadata.create_all(bind=engine)
    print("✅ Database tables created successfully")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
