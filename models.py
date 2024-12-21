from sqlalchemy import Column, Integer, String, Text, ForeignKey, Date
from sqlalchemy.orm import relationship
from database import Base

class User(Base):
    __tablename__ = "users"
    user_id = Column(Integer, primary_key=True, index=True)
    nom = Column(String, nullable=False)
    prenom = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    pwd = Column(String, nullable=False)
    role = Column(String, nullable=False)
    num_tlph = Column(String)

    tasks = relationship("EmployeeTask", back_populates="user")

class Task(Base):
    __tablename__ = "tasks"
    task_id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    description = Column(Text, nullable=False)
    status = Column(String, default="pending")
    delay = Column(Date)

    employees = relationship("EmployeeTask", back_populates="task")

class EmployeeTask(Base):
    __tablename__ = "employee_tasks"
    task_id = Column(Integer, ForeignKey("tasks.task_id"), primary_key=True)
    user_id = Column(Integer, ForeignKey("users.user_id"), primary_key=True)

    user = relationship("User", back_populates="tasks")
    task = relationship("Task", back_populates="employees")
