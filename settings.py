from pydantic import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    USER_DB: str = "postgres"
    PASSWORD_DB: str = "postgres"
    HOST_DB: str = "localhost"
    PORT_DB: str = "5432"
    
    # databases
    NAME_DB_1: str = "database1"
    NAME_DB_2: str = "database2"
    
    # sqlalchemy
    ENGINE_1: str = f"postgresql+asyncpg://{USER_DB}:{PASSWORD_DB}@{HOST_DB}:{PORT_DB}/{NAME_DB_1}"
    ENGINE_2: str = f"postgresql+asyncpg://{USER_DB}:{PASSWORD_DB}@{HOST_DB}:{PORT_DB}/{NAME_DB_2}"
        

@lru_cache()
def get_settings() -> Settings:
    return Settings()

settings = get_settings()