from crewai import LLM
from .helpers import get_settings
app_settings = get_settings()

LLM_PROVIDER= app_settings.LLM_PROVIDER
LLM_API_KEY= app_settings.LLM_API_KEY
BASE_URL= "https://openrouter.ai/api/v1"

deepseek_v3 = LLM(
    model= f"{LLM_PROVIDER}/deepseek/deepseek-chat-v3-0324:free",
    base_url=BASE_URL,
    api_key=LLM_API_KEY,
    temperature=0.5
)

mistral_small = LLM(
    model= f"{LLM_PROVIDER}/mistralai/mistral-small-3.1-24b-instruct:free",
    base_url=BASE_URL,
    api_key=LLM_API_KEY,
    temperature=0
)