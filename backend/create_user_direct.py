#!/usr/bin/env python3
import sys
import os

# Add current directory to Python path
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, current_dir)

import bcrypt
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Boolean, DateTime
from sqlalchemy.sql import func

# Database setup
SQLALCHEMY_DATABASE_URL = "sqlite:///./scopeai.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
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

# Create tables if they don't exist
Base.metadata.create_all(bind=engine)

def create_test_user():
    db = SessionLocal()
    try:
        # Check if test user already exists
        test_user = db.query(User).filter(User.email == "demo@scopeai.com").first()
        if test_user:
            print("✅ Test user already exists")
            return
        
        # Create test user
        password = "demo123"
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        
        test_user = User(
            email="demo@scopeai.com",
            hashed_password=hashed_password,
            full_name="Demo User"
        )
        
        db.add(test_user)
        db.commit()
        print("✅ Test user created successfully!")
        print("   Email: demo@scopeai.com")
        print("   Password: demo123")
        
    except Exception as e:
        print(f"❌ Error creating test user: {str(e)}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    create_test_user()
