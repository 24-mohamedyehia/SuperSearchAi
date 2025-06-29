from fastapi import FastAPI
from src.routes import base_router, start_router , search_router, results_router
import agentops
agentops.init()

app = FastAPI()

app.include_router(base_router)
app.include_router(start_router)
app.include_router(search_router)
app.include_router(results_router)

