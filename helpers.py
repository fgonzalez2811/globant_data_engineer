"""
Helper functions are defined in this separate and 
imported into main.py file to improve 
maintainability and readibility

"""
from database import SessionLocal
import pandas as pd


def get_db():
    # Create session:
    db = SessionLocal()
    
    # yield session and wait until transaction ends, then close session:
    try:
        yield db
    finally:
        db.close()
        
def get_invalid_rows(df):
    no_name_rows = df[df[['name']].isnull().any(axis=1)]
    
    if {'datetime', 'job_id', 'department_id'}.issubset(df.columns):  
        incomplete_rows = df[df[['datetime', 'job_id', 'department_id']].isnull().any(axis=1)] 
    
    return {'no_name_rows' : no_name_rows, 'incomplete_rows': incomplete_rows}
        
def clean_data(df):
    # Drop rows with missing values in name columns:
    df = df.dropna(subset=['name'])

    # Drop rows with missing values in name, datetime, job_id, department_id and store them
    if {'datetime', 'job_id', 'department_id'}.issubset(df.columns):        
        df = df.dropna(subset=['datetime', 'job_id', 'department_id'])
            
    # convert to date format
    if 'datetime' in df.columns:
        df['datetime'] = pd.to_datetime(df['datetime'], errors='coerce')
    
    # convert id's to numbers:
    if {'job_id', 'department_id'}.issubset(df.columns):
        df['job_id'] = pd.to_numeric(df['job_id'], errors='coerce')
        df['department_id'] = pd.to_numeric(df['department_id'], errors='coerce')
        
    # Remove duplicates
    df.drop_duplicates(inplace=True)

    # Trim whitespace and standardize text
    df['name'] = df['name'].str.strip().str.title()
    
    return df