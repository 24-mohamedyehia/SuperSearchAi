from enum import Enum

class ResponseSignal(Enum):

    VALID_INPUT = "valid_input"
    RESEARCH_STARTED = "research_started"
    RESEARCH_COMPLETED = "research_completed"
    LLM_PROVIDER_NOT_SUPPORT = "llm_provider_not_support"
    INVALID_SEARCH_MODE = "invalid_search_mode"
    NO_RELATED_QUESTIONS = "no_related_questions"
    STARTED_SEARCH = "started_search"
    NOT_YET_IMPLEMENTED = "not_yet_implemented_search_mode"
    NO_RESULTS_FOUND = "no_results_found"
