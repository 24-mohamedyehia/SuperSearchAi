from .BaseController import BaseController
from models import ResponseSignal
from helpers.ask_user import ask_user_for_clarification

class StartController(BaseController):
    def __init__(self, query: str, llm_provider: str, llm_api_key: str,base_url: str, model_name: str ,session_id: str):
        super().__init__()
        self.query = query
        self.llm_provider = llm_provider
        self.llm_api_key = llm_api_key
        self.base_url = base_url
        self.model_name = model_name
        self.session_id = session_id
        self.related_questions = None

    def start(self):
        
        if self.llm_provider.lower() not in self.app_settings.LLM_PROVIDER_SUPPORT:
            return False, ResponseSignal.LLM_PROVIDER_NOT_SUPPORT.value
        
        self.llm_setting.set_llm_provider(self.llm_provider)
        self.llm_setting.set_llm_api_key(self.llm_api_key)
        self.llm_setting.set_llm_base_url(self.base_url)
        self.llm_setting.set_llm_model(self.model_name)

        related_questions = ask_user_for_clarification(self.query, self.llm_setting)
        if related_questions is None:
            return False, ResponseSignal.NO_RELATED_QUESTIONS.value
        else:
            self.related_questions = related_questions
            return True, related_questions
    
    def get_llm_settings(self):
        return self.llm_setting
