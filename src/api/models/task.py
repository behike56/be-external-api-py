from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from src.api.db import Base

class Task(Base):
    """タスク"""
    __tablename__ = "tasks"
    
    id = Column(Integer, primary_key=True)
    title = Column(String(1024))
    created_at = Column(DateTime, nullable=False, default=func.now())
    updated_at = Column(DateTime, nullable=False, default=func.now(), onupdate=func.now())
    
    done = relationship("Done", back_populates="task", cascade="delete")

class Done(Base):
    """完了"""
    __tablename__ = "dones"
    
    id = Column(Integer, ForeignKey("tasks.id"), primary_key=True)
    
    task = relationship("Task", back_populates="done"   )
