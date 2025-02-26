"""
Helper functions are defined in this separate and 
imported into main.py file to improve 
maintainability and readibility
"""
from database import SessionLocal


def get_db():
    # Create session:
    db = SessionLocal()
    
    # yield session and wait until transaction ends, then close session:
    try:
        yield db
    finally:
        db.close()
        
        
def clean_data(df):
    # Drop rows with missing values in essential columns:
    df = df.dropna(subset=['name'])
