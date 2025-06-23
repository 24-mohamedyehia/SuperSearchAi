from enum import Enum

class ResponseSignal(Enum):

    VALID_INPUT = "valid_input"
    RESEARCH_STARTED = "research_started"
    RESEARCH_COMPLETED = "research_completed"   
    INVALID_INPUT = "invalid_input"
    INVALID_TOPIC = "invalid_topic"
    INVALID_SEARCH_WAY = "invalid_search_way"