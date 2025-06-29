from pydantic import BaseModel, Field, field_validator

class SearchRequest(BaseModel):
    """SearchRequest model for initiating a search request.
    Attributes:
        session_id (str): Unique identifier for the search session.
        search_mode (str): Mode of the search (e.g., "quick" or "deep").
        answers (str): Answers to clarification questions.
        query (str): The search query provided by the user.
        clarification (list[dict[str, str]]): List of clarification questions and answers.
    """
    session_id: str = Field(..., description="Unique identifier for the search session.")
    search_mode: str = Field(..., description="Mode of the search (e.g., 'quick' or 'deep').")
    answers: str = Field(..., description="Answers to clarification questions.")
    query: str = Field(..., description="The search query provided by the user.")
    clarification: list[dict[str, str]] = Field(..., description="List of clarification questions and answers.")

    @field_validator("session_id", "search_mode", "answers", "query", "clarification")
    def not_empty(value, info):
        if isinstance(value, str) and not value.strip():
            raise ValueError(f"{info.field_name} must be a non-empty string.")
        return value