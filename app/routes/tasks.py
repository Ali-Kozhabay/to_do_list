from fastapi import APIRouter, Depends, HTTPException,  Path
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime

from app.crud import crud 
from app.models import models
from app.schemas import schemas
from app.database import get_db
from app.auth.deps import get_current_active_user


router = APIRouter(
    prefix="/tasks",
    tags=["tasks"]
)

@router.post("/", response_model=schemas.TaskResponse, status_code=201)
async def create_task(
    task: schemas.TaskCreate,
    db: Session = Depends(get_db),
    user: models.User = Depends(get_current_active_user)
):

    return await crud.create_task(db=db, task=task, user_id=user.id)

@router.get("/{task_name}", response_model=schemas.TaskResponse)
async def read_task(
    task_name: str = Path(..., title="The name of the task to get"),
    db: Session = Depends(get_db)
):
    db_task = await crud.get_task(db=db, task_name=task_name)
    if db_task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return db_task

@router.get("/", response_model=List[schemas.TaskResponse])
async def read_tasks(

    db: Session = Depends(get_db)
):
    tasks = await crud.get_tasks(db=db)
    return tasks

@router.patch("/{task_id}", response_model=schemas.TaskResponse)
async def update_task(
    task_id: int = Path(..., title="The ID of the task to update"),
    task: schemas.TaskUpdate = None,
    db: Session = Depends(get_db)
):
    db_task = await crud.get_task(db=db, task_id=task_id)
    if db_task is None:
        raise HTTPException(status_code=404, detail="Task not found")

    updated_task = await crud.update_task(db=db, task_id=task_id, task_data=task)
    return updated_task 

@router.delete("/{task_id}", status_code=204)
async def delete_task(
    task_id: int = Path(..., title="The ID of the task to delete"),
    db: Session = Depends(get_db)
):
    db_task = await crud.get_task(db=db, task_id=task_id)
    if db_task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    
    deleted = await crud.delete_task(db=db, task_id=task_id)
    if not deleted:
        raise HTTPException(status_code=500, detail="Failed to delete task")
    return {'message': 'Task deleted successfully'}

@router.delete("/{task_id}/hard", status_code=204)
async def hard_delete_task(
    task_id: int = Path(..., title="The ID of the task to permanently delete"),
    db: Session = Depends(get_db)
):

    db_task = await crud.get_task(db=db, task_id=task_id)
    if db_task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    deleted = await crud.hard_delete_task(db=db, task_id=task_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Task not found")
    return None

@router.get("/statistics/summary", response_model=schemas.TaskStats)
async def get_task_statistics(db: Session = Depends(get_db)):
    return await crud.get_task_stats(db=db)