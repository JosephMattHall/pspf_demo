from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    project_name: str = "StreamStock"
    
    # Database
    database_url: str
    
    # Redis / PSPF
    redis_url: str
    
    # App
    debug: bool = False
    log_level: str = "INFO"
    secret_key: str

    class Config:
        env_file = ".env"
        case_sensitive = False

settings = Settings()
