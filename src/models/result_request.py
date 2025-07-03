from pydantic import BaseModel, Field, field_validator

class ResultReuest(BaseModel):
    """ResultReuest model to get a search results.
    Attributes:
        session_id (str): Unique identifier for the search session.
    """
    session_id: str = Field(..., description="Unique identifier for the search session.")
    
    @field_validator("session_id")
    def not_empty(value, info):
        if isinstance(value, str) and not value.strip():
            raise ValueError(f"{info.field_name} must be a non-empty string.")
        return value