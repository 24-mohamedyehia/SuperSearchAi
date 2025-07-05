from pydantic import BaseModel, Field, field_validator
from typing import Literal


class AnswerItem(BaseModel):
    """Answer item for clarification questions."""
    question_id: str = Field(...,
                             description="Unique identifier for the question.")
    choice: str = Field(..., description="The chosen answer.")


class SearchRequest(BaseModel):
    """SearchRequest model for initiating a search request.
    Attributes:
        session_id (str): Unique identifier for the search session.
        search_mode (Literal["quick", "deep"]): Mode of the search.
        query (str): The search query provided by the user.
        answers (list[AnswerItem]): List of answers to clarification questions.
    """
    session_id: str = Field(...,
                            description="Unique identifier for the search session.")
    search_mode: Literal["quick", "deep"] = Field(...,
                                                  description="Mode of the search.")
    query: str = Field(...,
                       description="The search query provided by the user.")
    answers: list[AnswerItem] = Field(
        ..., description="List of answers to clarification questions.")

    @field_validator("session_id", "query")
    def not_empty(value, info):
        if isinstance(value, str) and not value.strip():
            raise ValueError(f"{info.field_name} must be a non-empty string.")
        return value
