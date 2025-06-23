from fastapi import APIRouter, Depends
from ..models import ResearchRequest
from ..controllers import ResearchController
from fastapi.responses import JSONResponse
from ..models import ResponseSignal
from fastapi import status

research_router = APIRouter(
    prefix="/api/v1/research",
    tags=["research"]
)

@research_router.post("/")
async def create_research(request: ResearchRequest): 

    data_controller = ResearchController()
    is_valid, signal = data_controller.get_user_input(request.topic, request.search_way)
    
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
            "signal": signal
        }
    )

