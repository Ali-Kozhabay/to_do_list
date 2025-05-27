from fastapi import HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import select
from passlib.context import CryptContext
from app.schemas.schemas import UserCreate , UserLogin
from app.models.models import User
from app.auth.token import create_access_token, ACCESS_TOKEN_EXPIRE_MINUTES

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

async def create_user(db: Session, user: UserCreate):
    user_add=User(**user.model_dump())
    user_add.password = pwd_context.hash(user.password)
    db.add(user_add)
    await db.commit()
    await db.refresh(user_add)
    return {'message':'User is created'}

async def get_user_by_email(db: Session, email: str):
    db_user = await db.execute(select(User).filter(email == User.email))

    if db_user :
        return False
    return True


async def get_user_by_name(db: Session, name: str):
    db_user = await db.execute(select(User).filter(name == User.username))
    if db_user :
        return False
    return True

async def user_login(db: Session, user: UserLogin):
    db_res = await  db.execute(select(User.password).filter(user.email == User.email))
    db_user = db_res.scalars().first()
    if db_user is None:
        raise HTTPException(status_code=400, detail="User is not existed")
    if not pwd_context.verify(user.password, db_user):
        raise HTTPException(status_code=400, detail="Incorrect password")
    token=create_access_token(user.email, expires_delta=ACCESS_TOKEN_EXPIRE_MINUTES)
    return {'token':token}