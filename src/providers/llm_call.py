from crewai import LLM

class InintLMM():
    def __init__(self):
        self._llm_provider = ""
        self._llm_api_key = ""
    
    def set_llm_provider(self, llm_provider: str):
        self._llm_provider = llm_provider

    def get_llm_provider(self):
        return self._llm_provider
    
    def set_llm_api_key(self, llm_api_key: str):
        self._llm_api_key = llm_api_key
    
    def get_llm_api_key(self):
        return self._llm_api_key

class SettingsHolder:
    LLM_SETTINGS = None

def get_mistral_small(llm_setting: InintLMM) -> LLM:
    return LLM(
        model= f"{llm_setting.get_llm_provider()}/mistralai/mistral-small-3.1-24b-instruct-2503:free",
        base_url= "https://openrouter.ai/api/v1",
        api_key=llm_setting.get_llm_api_key(),
        temperature=0
        )

def get_deepseek_v3(llm_setting: InintLMM) -> LLM:
    return LLM(
        model= f"{llm_setting.get_llm_provider()}/deepseek/deepseek-chat-v3-0324:free",
        base_url= "https://openrouter.ai/api/v1",
        api_key=llm_setting.get_llm_api_key(),
        temperature=0.5
        )