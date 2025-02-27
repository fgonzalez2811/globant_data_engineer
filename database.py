from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy import create_engine
import os

# Set up database connection from environment variables:
DATABASE_URL = os.getenv("DATABASE_URL")

# Create SQLAlchemy engine to connect to the database:
engine = create_engine(DATABASE_URL)

# Define SessionLocal to hanlde database transactions
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Creates declarative class to define ORM models:
Base = declarative_base() 
