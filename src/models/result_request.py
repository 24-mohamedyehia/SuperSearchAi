from pydantic import BaseModel, Field

class ResultReuest(BaseModel):
    """Search result model for returning search results."""
    session_id: str = Field(...,description="Unique identifier for the search session")
