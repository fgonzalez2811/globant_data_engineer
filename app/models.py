from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.database import Base


class Department(Base):
    __tablename__= "departments"

    id = Column(Integer, primary_key=True, autoincrement=False)
    name = Column(String, nullable=False, unique=True)

    hired_employees = relationship("HiredEmployee", back_populates= "department_rel")

class Job(Base):
    __tablename__= "jobs"

    id = Column(Integer, primary_key=True, autoincrement=False)
    name = Column(String, nullable=False)

    hired_employees = relationship("HiredEmployee", back_populates="job_rel")

class HiredEmployee(Base):
    __tablename__= "hired_employees"

    id = Column(Integer, primary_key=True, autoincrement=False)
    name = Column(String, nullable=False)
    datetime = Column(DateTime, nullable=False)
    department_id = Column(Integer, ForeignKey("departments.id"), nullable=False)
    job_id = Column(Integer, ForeignKey("jobs.id"), nullable=False)

    department_rel = relationship("Department", back_populates="hired_employees")
    job_rel = relationship("Job", back_populates="hired_employees")