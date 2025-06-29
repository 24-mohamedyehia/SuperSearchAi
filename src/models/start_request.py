from pydantic import BaseModel, Field, field_validator

class StartRequest(BaseModel):
    """    StartRequest model for initiating a search request.
    Attributes:
        query (str): The query to search. Must be a non-empty string.
        llm_provider (str): The LLM provider to use. Must be a non-empty string.
        api_key (str): API key for the provider. Must be a non-empty string.
    Validators:
        Ensures that all string fields are non-empty."""

    query: str = Field(..., description="The query to search")
    llm_provider: str = Field(..., description="The LLM provider")
    llm_api_key: str = Field(..., description="API key of provider")

    @field_validator("query", "llm_provider", "llm_api_key")
    def not_empty(value, info):
        if isinstance(value, str) and not value.strip():
            raise ValueError(f"{info.field_name} must be a non-empty string.")
        return value