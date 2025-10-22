import sys
import os
sys.path.append(os.getcwd())

from models.database import SessionLocal, BillingRate

def check_billing_rates():
    db = SessionLocal()
    try:
        rates = db.query(BillingRate).all()
        print("Current billing rates in database:")
        for rate in rates:
            print(f"  - {rate.role}: ${rate.rate_per_hour}/hour")
        
        if not rates:
            print("No billing rates found! Adding default rates...")
            default_rates = [
                {"role": "Project Manager", "rate_per_hour": 150},
                {"role": "Business Analyst", "rate_per_hour": 120},
                {"role": "Solution Architect", "rate_per_hour": 180},
                {"role": "Frontend Developer", "rate_per_hour": 130},
                {"role": "Backend Developer", "rate_per_hour": 140},
                {"role": "Full Stack Developer", "rate_per_hour": 145},
                {"role": "DevOps Engineer", "rate_per_hour": 150},
                {"role": "QA Engineer", "rate_per_hour": 110},
                {"role": "Data Scientist", "rate_per_hour": 160},
                {"role": "Data Engineer", "rate_per_hour": 150},
                {"role": "ML Engineer", "rate_per_hour": 170},
                {"role": "UI/UX Designer", "rate_per_hour": 125},
                {"role": "Security Engineer", "rate_per_hour": 175}
            ]
            
            for rate_data in default_rates:
                rate = BillingRate(**rate_data)
                db.add(rate)
            
            db.commit()
            print("Default billing rates added successfully!")
            
    except Exception as e:
        print(f"Error: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    check_billing_rates()
