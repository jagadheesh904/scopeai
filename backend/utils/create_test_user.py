import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from models.database import SessionLocal, User
import bcrypt

def create_test_user():
    db = SessionLocal()
    try:
        # Check if test user already exists
        test_user = db.query(User).filter(User.email == "demo@scopeai.com").first()
        if test_user:
            print("✅ Test user already exists")
            return
        
        # Create test user with bcrypt hashing
        password = "demo123"
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        
        test_user = User(
            email="demo@scopeai.com",
            hashed_password=hashed_password,
            full_name="Demo User"
        )
        
        db.add(test_user)
        db.commit()
        print("✅ Test user created successfully")
        print("   Email: demo@scopeai.com")
        print("   Password: demo123")
        
    except Exception as e:
        print(f"❌ Error creating test user: {str(e)}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    create_test_user()
