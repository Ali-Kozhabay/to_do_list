from pydantic import BaseSettings
from functools import lru_cache
class Settings(BaseSettings):
    """Application settings loaded from environment variables"""
    
    # Database settings
    database_url: str
    db_host: str
    db_port: int 
    db_name: str
    db_user: str
    db_password: str
    
    # JWT settings
    jwt_secret_key: str
    jwt_algorithm: str 
    jwt_access_token_expire_minutes:int

    class Config:
        env_file='.env'


@lru_cache()
def get_settings():
    """Get cached settings instance"""
    return Settings()
