from fastapi import APIRouter, Depends
from helpers import get_base_settings , Settings

base_router = APIRouter()

@base_router.get("/")
async def index(app_settings: Settings = Depends(get_base_settings)):

    app_name = app_settings.APP_NAME
    app_version = app_settings.APP_VERSION
    
    return {
        "app_name": app_name,
        "app_version": app_version,
    }
