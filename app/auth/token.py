from passlib import crypto
import secrets
import jwt
from jose import jwt
from datetime import datetime, timedelta


from app.schemas.schemas import TokenData
from app.config import get_settings


settings=get_settings(
)
SECRET_KEY=settings.jwt_secret_key
ALGORITHM=settings.jwt_algorithm
ACCESS_TOKEN_EXPIRE_MINUTES=settings.jwt_access_token_expire_minutes

def create_access_token(data: dict, expires_delta: int ) -> str:
    """
    Create a JWT access token.
    
    Args:
        data: Either a dictionary with payload data or a string (email)
        expires_delta: Optional expiration time in minutes
        
    Returns:
        JWT token as string
    """
    # Handle both string and dictionary input
    if isinstance(data, str):
        # If data is a string (email), create proper dictionary
        to_encode = {"sub": data}
    elif isinstance(data, dict):
        # If data is already a dictionary, make a copy
        to_encode = data.copy()
    else:
        raise ValueError("Data must be either a string or dictionary")
    # Set expiration time
    if expires_delta:
        expire = datetime.now() + timedelta(minutes=expires_delta)
    else:
        expire = datetime.now() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    # Add expiration to payload
    to_encode.update({"exp": expire})
    # Create and return the JWT token
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def decode_access_token(token: str) -> TokenData:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email = payload.get("sub")
        if email is None:
            raise ValueError("Invalid token")
        token_data = TokenData(email=email)
    except jwt.JWTError:
        raise ValueError("Invalid token")
    return token_data