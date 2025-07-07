from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.routes import base_router, start_router, search_router, results_router
import agentops
agentops.init()

app = FastAPI()

# Add CORS middleware to handle OPTIONS requests
app.add_middleware(
    CORSMiddleware,
    # Allow all origins for development purposes
    # TODO: Restrict this in production to specific domains as needed
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(base_router)
app.include_router(start_router)
app.include_router(search_router)
app.include_router(results_router)
