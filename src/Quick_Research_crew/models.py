from pydantic import BaseModel, Field
from typing import List

class SingleSearchResult(BaseModel):
    title: str
    url: str = Field(..., title="The URL of the web page")
    content: str = Field(..., title="Content of the page")
    score: float
    search_query: str = Field(..., title="The search query used to get this result")

class AllSearchResults(BaseModel):
    results: List[SingleSearchResult]

class QuickReport(BaseModel):
    title: str
    answer: str
