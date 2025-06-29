from .BaseController import BaseController
from ..models import ResponseSignal
from ..helpers import ask_user_for_clarification

class StartController(BaseController):
    def __init__(self, query: str, llm_provider: str, llm_api_key: str, session_id: str):
        super().__init__()
        self.query = query
        self.__llm_provider = llm_provider
        self.__llm_api_key = llm_api_key
        self.session_id = session_id
        self.related_questions = None

    def start(self):
        
        if self.__llm_provider.lower() not in self.app_settings.LLM_PROVIDER_SUPPORT:
            return False, ResponseSignal.LLM_PROVIDER_NOT_SUPPORT.value

        self.app_settings.LLM_PROVIDER = self.__llm_provider
        self.app_settings.LLM_API_KEY = self.__llm_api_key

        related_questions = ask_user_for_clarification(self.query)
        if not related_questions:
            return False, ResponseSignal.NO_RELATED_QUESTIONS.value
        else:
            self.related_questions = related_questions
            return True, related_questions
