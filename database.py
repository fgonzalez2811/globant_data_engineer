from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy import create_engine
import os

# Set up database connection:
DATABASE_URL = os.getenv("DATABASE_URL")

engine = create_engine(DATABASE_URL) 
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create base model:
Base = declarative_base() 
