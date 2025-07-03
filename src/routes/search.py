from fastapi import APIRouter , BackgroundTasks
from models import SearchRequest
from controllers import SearchController
from fastapi.responses import JSONResponse
from fastapi import status
from providers import SettingsHolder

search_router = APIRouter(
    prefix="/search",
    tags=["search"]
)

@search_router.post("/")
async def create_search(request: SearchRequest, background_tasks: BackgroundTasks): 

    search_controller = SearchController(
        search_mode=request.search_mode,
        answers=request.answers,
        session_id=request.session_id,
        clarification=request.clarification,
        query=request.query,
        llm_setting=SettingsHolder.LLM_SETTINGS
    )
    is_valid, signal = search_controller.search()
        
    if not is_valid:
        return JSONResponse(
            status_code = status.HTTP_400_BAD_REQUEST,
            content = {
                "signal": signal
            }
        )
    
    background_tasks.add_task(search_controller.run_background_tasks)
    
    return JSONResponse(
        status_code = status.HTTP_200_OK,
        content = {
            "session_id": search_controller.session_id,
            "status": signal
        }
    )

