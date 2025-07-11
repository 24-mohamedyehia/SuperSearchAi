from pydantic_settings import BaseSettings
from typing import List

class Settings(BaseSettings):

    APP_NAME: str
    APP_VERSION: str
    LLM_PROVIDER_SUPPORT: List[str] = ['openrouter', 'ollama']
    class Config:
        env_file = "/.env"

def get_base_settings():
    return Settings()