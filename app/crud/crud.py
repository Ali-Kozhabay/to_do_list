from typing import Annotated
from sqlalchemy import select, update, delete, func
from sqlalchemy.orm import Session
from typing import List, Optional, Dict, Any
from datetime import datetime

from app.models.models import Task, TaskStatus
from app.schemas.schemas import TaskCreate, TaskUpdate, TaskStats,TaskStatus
from app.auth.deps import get_current_user_id

async def create_task(db: Session, task: TaskCreate) -> Task:
    db_task = Task(**task.model_dump())
    db_task.user_id=get_current_user_id()
    db.add(db_task)
    await db.commit()
    await db.refresh(db_task)
    return  db_task

async def get_task(db: Session, task_id: int) -> Optional[Task]:
    result= await db.execute(
        select(Task).filter(Task.id == task_id, Task.is_deleted == False)
    )
    return result.scalars().first()

async def get_tasks(
    db: Session, 
) -> List[Task]:
    query = await  db.execute(
        select(Task).filter(Task.is_deleted == False)
    )
    tasks=query.scalars().all()
    return tasks

async def update_task(
    db: Session, 
    task_id: int, 
    task_data: TaskUpdate
) -> Optional[Task]:
    # Filter out None values
    update_data = {k: v for k, v in task_data.model_dump().items() if v is not None}
    
    if not update_data:
        # Return existing task if no updates
        return await get_task(db, task_id)
    
    task = await get_task(db, task_id)
    if task:
        for key, value in update_data.items():
            setattr(task, key, value)
        await db.commit()
        await db.refresh(task)
        return task
    return None

async def delete_task(db: Session, task_id: int) -> bool:
    task = await get_task(db, task_id)
    if task:
        task.is_deleted = True
        await db.commit()
        return True
    return False

async def hard_delete_task(db: Session, task_id: int) -> bool:
    task = await db.execute(select(Task).filter(Task.id == task_id))
    if task:
        await db.delete(task.scalars().first())
        await db.commit()
        return True
    return False

async  def get_task_stats(db: Session) -> TaskStats:
    # Get current date for overdue calculation
    current_date = datetime.now()
    
    total = await db.execute(select(func.count(Task.id)).filter(Task.is_deleted == False))
    completed = await db.execute(select(func.count(Task.id)).filter(
        Task.status == TaskStatus.COMPLETED,
        Task.is_deleted == False
    ))
    in_progress = await db.execute(select(func.count(Task.id)).filter(
        Task.status == TaskStatus.IN_PROGRESS,
        Task.is_deleted == False
    ))
    todo = await db.execute(select(func.count(Task.id)).filter(
        Task.status == TaskStatus.TODO,
        Task.is_deleted == False
    ))
    cancelled = await db.execute(select(func.count(Task.id)).filter(
        Task.status == TaskStatus.CANCELLED,
        Task.is_deleted == False
    ))
    overdue = await db.execute(select(func.count(Task.id)).filter(
        Task.due_date < current_date,
        Task.status != TaskStatus.COMPLETED,
        Task.status != TaskStatus.CANCELLED,
        Task.is_deleted == False
    ))
    return TaskStats(
        total=total.scalar(),
        completed=completed.scalar(),
        in_progress=in_progress.scalar(),
        todo=todo.scalar(),
        cancelled=cancelled.scalar(),
        overdue=overdue.scalar()
    )