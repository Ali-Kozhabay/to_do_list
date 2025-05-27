from typing import Annotated

from fastapi import Depends, HTTPException
from fastapi.security import  HTTPAuthorizationCredentials , HTTPBearer,OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select


from app.database  import get_db
from app.auth.token import decode_access_token
from app.models.models import User


security = HTTPBearer()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

async def get_current_user(
    token: Annotated[str, Depends(oauth2_scheme)],
    session: AsyncSession = Depends(get_db)
):
    token_data = decode_access_token(token)
    if not token_data.email:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    result = await session.execute(select(User).filter(User.email == token_data.email))
    user = result.scalar_one_or_none()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user



async def get_current_user_id(
    current_user: User = Depends(get_current_user),
):
    if not current_user:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    return current_user.id

async def get_current_active_user(
    current_user: User = Depends(get_current_user),
    token:str = Depends
):
    if not current_user.disabled  :
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user