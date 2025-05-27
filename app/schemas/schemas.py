
from pydantic import BaseModel, Field, EmailStr
from typing import Optional
from fastapi import Depends
from datetime import datetime
from app.models.models import TaskStatus, TaskPriority




class TaskBase(BaseModel):

    title: str = Field(..., min_length=1, max_length=255)
    description: Optional[str] = None
    status: TaskStatus = TaskStatus.TODO
    priority: TaskPriority = TaskPriority.MEDIUM
    due_date: Optional[datetime] = None


class TaskCreate(TaskBase):

    # is_deleted: bool = False
    # created_at: datetime = Field(default_factory=datetime.now)
    pass

class TaskUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=1, max_length=255)
    description: Optional[str] = None
    status: Optional[TaskStatus] = None
    priority: Optional[TaskPriority] = None
    due_date: Optional[datetime] = None

class TaskResponse(TaskBase):
    id: int
    is_deleted: bool
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True

class TaskStats(BaseModel):
    total: int
    completed: int
    in_progress: int
    todo: int
    cancelled: int
    overdue: int


class UserCreate(BaseModel):

    username: str
    email: EmailStr
    password: str

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str
class TokenData(BaseModel):
    email: EmailStr
