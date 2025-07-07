from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional
from datetime import datetime


class SearchResult(BaseModel):
    """Search result model for returning search results."""
    session_id: str = Field(...,
                            description="Unique identifier for the search session")
    status: str = Field(...,
                        description="Status of the search (completed, in_progress, failed)")
    search_mode: str = Field(...,
                             description="Mode of the search (quick, deep)")
    query: str = Field(..., description="The original search query")
    user_details: str = Field(..., description="Formatted user answers")
    search_results: List[Dict[str, Any]] = Field(
        default=[], description="List of search results")
    report: Optional[str] = Field(default=None, description="Generated report")
    created_at: Optional[str] = Field(
        default=None, description="When the search was created")
    completed_at: Optional[str] = Field(
        default=None, description="When the search was completed")
    error: Optional[str] = Field(
        default=None, description="Error message if search failed")
