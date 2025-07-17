from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    # MySQL connection details
    HOST_MYSQL: str = "localhost"
    USER_MYSQL: str = "root"
    PASSWORD_MYSQL: Optional[str] = None
    DATABASE_MYSQL: str
    PORT_MYSQL: str = "3306"
    
    # SQLAlchemy connection URL
    DATABASE_URL: str
    
    # Security
    SECRET_KEY: str
    DEBUG: bool = False

    model_config = {"env_file": ".env"}

settings = Settings()