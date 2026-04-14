import pandas as pd
import os
import sys

# Add the project root to sys.path to allow imports
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from sqlalchemy.orm import Session
from db.database import SessionLocal, engine
from db import models

def seed_database():
    DATA_PATH = os.path.join(os.path.dirname(__file__), '../final_dataset.csv')
    
    if not os.path.exists(DATA_PATH):
        print(f"Dataset not found at {DATA_PATH}")
        return

    # Create tables
    print("Creating tables...")
    models.Base.metadata.create_all(bind=engine)

    db = SessionLocal()
    try:
        # Check if already seeded to avoid duplicates
        count = db.query(models.ClinicalInteraction).count()
        if count > 0:
            print(f"Database already contains {count} interactions. Skipping seed.")
            return

        print("Reading CSV data (this may take a moment)...")
        df = pd.read_csv(DATA_PATH, keep_default_na=False)
        
        print(f"Importing {len(df)} records into the database...")
        
        # Batch insert for better performance
        batch_size = 1000
        for i in range(0, len(df), batch_size):
            batch_df = df.iloc[i:i+batch_size]
            interactions = [
                models.ClinicalInteraction(
                    drug_a=str(row['drug_a']).lower(),
                    drug_b=str(row['drug_b']).lower(),
                    severity=str(row['severity']),
                    description=str(row['description'])
                )
                for _, row in batch_df.iterrows()
            ]
            db.bulk_save_objects(interactions)
            db.commit()
            print(f"Imported {min(i + batch_size, len(df))}/{len(df)}...")

        print("Seeding complete!")
    except Exception as e:
        print(f"Error during seeding: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    seed_database()
