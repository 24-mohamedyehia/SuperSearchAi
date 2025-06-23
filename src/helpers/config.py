from pydantic_settings import BaseSettings

class Settings(BaseSettings):

    APP_NAME: str
    APP_VERSION: str
    
    class Config:
        env_file = "/.env"

def get_settings():
    return Settings()