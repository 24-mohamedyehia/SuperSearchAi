from fastapi import APIRouter
from controllers import ResultsController
from models import ResultReuest
from fastapi.responses import JSONResponse
from fastapi import status

results_router = APIRouter(
    prefix="/results",
    tags=["results"]
)

@results_router.get("/")
async def get_results(request: ResultReuest): 

    results_controller = ResultsController(
        session_id=request.session_id
    )
    is_valid, signal = results_controller.get_results()

    if not is_valid:
        return JSONResponse(
            status_code = status.HTTP_400_BAD_REQUEST,
            content = {
                "signal": signal
            }
        )
    
    return JSONResponse(
        status_code = status.HTTP_200_OK,
        content = signal
    )

