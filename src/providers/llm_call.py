from crewai import LLM
from .llm_config import get_provider_config

class InintLMM():
    def __init__(self):
        self._llm_provider = ""
        self._llm_api_key = ""
        self._llm_base_url = ""
        self._llm_model = ""
    
    def set_llm_provider(self, llm_provider: str):
        self._llm_provider = llm_provider

    def get_llm_provider(self):
        return self._llm_provider
    
    def set_llm_api_key(self, llm_api_key: str):
        self._llm_api_key = llm_api_key
    
    def get_llm_api_key(self):
        return self._llm_api_key
    
    def set_llm_base_url(self, llm_base_url: str):
        self._llm_base_url = llm_base_url
    
    def get_llm_base_url(self):
        return self._llm_base_url
    
    def set_llm_model(self, llm_model: str):
        self._llm_model = llm_model
    
    def get_llm_model(self):
        return self._llm_model

class SettingsHolder: 
    LLM_SETTINGS = None

class MakeLLM:
    def __init__(self, llm_setting: InintLMM):
        self._provider = llm_setting.get_llm_provider()
        self._api_key = llm_setting.get_llm_api_key()
        self._base_url = llm_setting.get_llm_base_url()
        self._model = llm_setting.get_llm_model()

    def get_llm(self):
        config = get_provider_config(self._provider, self._model, self._base_url).get_config()
        return LLM(
            model=f"{self._provider}/{config['model']}",
            base_url=config['base_url'],
            api_key=self._api_key,
            temperature=config['temperature']
        )
