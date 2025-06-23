from fastapi import FastAPI
from src.routes import base_router, research_router

app = FastAPI()

app.include_router(base_router)
app.include_router(research_router)
