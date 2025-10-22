import sys
import os
sys.path.append(os.getcwd())

from models.database import SessionLocal, User
import bcrypt

def check_users():
    db = SessionLocal()
    try:
        users = db.query(User).all()
        print(f"Total users in database: {len(users)}")
        for user in users:
            print(f"ID: {user.id}, Email: {user.email}, Name: {user.full_name}")
            
        # Check if our test user exists
        test_user = db.query(User).filter(User.email == "demo@scopeai.com").first()
        if test_user:
            print(f"\n✅ Test user found: {test_user.email}")
            # Test password verification
            test_password = "demo123"
            if bcrypt.checkpw(test_password.encode('utf-8'), test_user.hashed_password.encode('utf-8')):
                print("✅ Password verification successful")
            else:
                print("❌ Password verification failed")
        else:
            print("\n❌ Test user not found in database")
            
    except Exception as e:
        print(f"Error checking users: {str(e)}")
    finally:
        db.close()

if __name__ == "__main__":
    check_users()
