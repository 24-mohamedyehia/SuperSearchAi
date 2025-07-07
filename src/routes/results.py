from fastapi import APIRouter, HTTPException
from models import SearchResult
import os
import json

results_router = APIRouter(
    prefix="/results",
    tags=["results"]
)


@results_router.get("/{session_id}", response_model=SearchResult)
async def get_search_results(session_id: str):
    """Get search results for a specific session."""
    try:
        session_file = f"./src/Research_crew/research/session_{session_id}.json"

        if not os.path.exists(session_file):
            raise HTTPException(status_code=404, detail="Session not found")

        with open(session_file, 'r', encoding='utf-8') as f:
            session_data = json.load(f)

        # Handle the case where search_results might be in different format
        if 'search_results' in session_data and isinstance(session_data['search_results'], dict):
            # If search_results is a dict with 'results' key, extract the results
            if 'results' in session_data['search_results']:
                session_data['search_results'] = session_data['search_results']['results']
            else:
                # If it's just a dict, convert to list
                session_data['search_results'] = [
                    session_data['search_results']]

        # Ensure all required fields have default values
        session_data.setdefault('search_results', [])
        session_data.setdefault('report', None)
        session_data.setdefault('created_at', None)
        session_data.setdefault('completed_at', None)
        session_data.setdefault('error', None)

        return SearchResult(**session_data)

    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="Session not found")
    except json.JSONDecodeError as e:
        raise HTTPException(
            status_code=500, detail=f"Invalid session data: {str(e)}")
    except UnicodeDecodeError as e:
        raise HTTPException(
            status_code=500, detail=f"Unicode encoding error: {str(e)}")
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Error retrieving results: {str(e)}")
