from pydantic import BaseModel, Field

class ResearchRequest(BaseModel):
    topic: str = Field(..., description="The topic to research")
    search_way: int = Field(..., description="The search way")