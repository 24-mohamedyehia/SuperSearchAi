from fastapi import APIRouter
from models import StartRequest
from controllers import StartController
from fastapi.responses import JSONResponse
from fastapi import status
from providers import SettingsHolder
import uuid

start_router = APIRouter(
    prefix="/start",
    tags=["start"]
)

@start_router.post("/")
async def create_research(request: StartRequest): 
    session_id = str(uuid.uuid4())

    start_controller = StartController(
        query=request.query,
        llm_provider=request.LLM_PROVIDER,
        llm_api_key=request.LLM_API_KEY,
        session_id=session_id
    )
    is_valid, signal = start_controller.start()

    SettingsHolder.LLM_SETTINGS = start_controller.get_llm_settings()
        
    if not is_valid:
        return JSONResponse(
            status_code = status.HTTP_400_BAD_REQUEST,
            content = {
                "signal": signal
            }
        )
    
    return JSONResponse(
        status_code = status.HTTP_200_OK,
        content = {
            "session_id": start_controller.session_id,
            "clarification": signal
        }
    )

