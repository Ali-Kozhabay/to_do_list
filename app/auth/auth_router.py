from fastapi import APIRouter, Depends, HTTPException ,Form
from fastapi.security import HTTPAuthorizationCredentials ,HTTPBearer
from passlib.context import CryptContext

from app.schemas.schemas import UserCreate,UserLogin
from sqlalchemy.orm import Session  
from app.database import get_db
from app.auth import auth_crud
from app.auth.token import create_access_token,ACCESS_TOKEN_EXPIRE_MINUTES

auth = APIRouter(prefix="/auth", tags=["auth"])

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

security = HTTPBearer()

@auth.post("/register")
async def register_user(user: UserCreate=Depends(), db: Session = Depends(get_db)):
    db_user_email = await auth_crud.get_user_by_email(db=db, email=user.email)
    db_user_name = await auth_crud.get_user_by_name(db=db, name=user.username)

    if not db_user_email or not db_user_name:
        raise HTTPException(status_code=400, detail="User already registered")
    return await auth_crud.create_user(db=db, user=user)

@auth.post("/login")
async def login_user(user: UserLogin=Depends(), db: Session = Depends(get_db)):
    db_user = await auth_crud.user_login(db=db, user=user)
    if not db_user:
        raise HTTPException(status_code=400, detail="User not found")
    token=create_access_token(db_user,ACCESS_TOKEN_EXPIRE_MINUTES)
    return {'token':token}

