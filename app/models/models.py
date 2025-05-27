import enum
from typing import Optional
from datetime import datetime
from sqlalchemy import String, Integer, Column, Text, Boolean, DateTime, Enum, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import Mapped, mapped_column
from app.database import Base
from sqlalchemy.orm import relationship, mapped_column, Mapped


class TaskStatus(str, enum.Enum):
    TODO = "todo"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    CANCELLED = "cancelled"

class TaskPriority(str, enum.Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    URGENT = "urgent"

class Task(Base):
    __tablename__ = "tasks"
    
    id :Mapped[int] = mapped_column(primary_key=True, index=True)

    title:Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    description:Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    status:Mapped[TaskStatus] = mapped_column(Enum(TaskStatus), default=TaskStatus.TODO, nullable=False)
    priority:Mapped[TaskPriority] = mapped_column(Enum(TaskPriority), default=TaskPriority.MEDIUM, nullable=False)
    due_date:Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
    is_deleted:Mapped[bool] = mapped_column(Boolean, default=False)
    created_at:Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at:Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), onupdate=func.now())
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    owner = relationship("User", back_populates="tasks")




class User(Base):
    __tablename__ = "users"
    id:Mapped[int] = mapped_column(primary_key=True, index=True)
    username:Mapped[str] = mapped_column(String(50), unique=True, index=True)
    email:Mapped[str] = mapped_column(String(100), unique=True, index=True)
    password:Mapped[str] = mapped_column(String(255))
    tasks = relationship("Task", back_populates="owner", cascade="all, delete-orphan")