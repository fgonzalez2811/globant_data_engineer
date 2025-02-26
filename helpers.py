"""
Helper functions are defined in this separate and 
imported into main.py file to improve 
maintainability and readibility

"""
from database import SessionLocal
import pandas as pd
import numpy as np


def get_db():
    # Create session:
    db = SessionLocal()
    
    # yield session and wait until transaction ends, then close session:
    try:
        yield db
    finally:
        db.close()
        
def get_invalid_rows(df):

    # Get rows with missing names
    if 'name' in df.columns:
        no_name_rows = df[df['name'].isnull()]
    else:
        no_name_rows = pd.DataFrame()

    # Get rows with missing datetime, job_id or department_id:
    required_columns = ['datetime', 'job_id', 'department_id']

    if set(required_columns).issubset(df.columns):  
        incomplete_rows = df[df[required_columns].isnull().any(axis=1)]
    else:
        incomplete_rows = pd.DataFrame()

    # Replace NaN and Infinity with None
    no_name_rows = no_name_rows.replace({np.nan: None, np.inf: None, -np.inf: None})
    incomplete_rows = incomplete_rows.replace({np.nan: None, np.inf: None, -np.inf: None})

    # convert dataframes to dict
    no_name_rows = no_name_rows.to_dict(orient='records')
    incomplete_rows = incomplete_rows.to_dict(orient='records')

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
    df['name'] = df['name'].str.strip()
    
    return df