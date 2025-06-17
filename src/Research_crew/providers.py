from crewai import LLM
import os
from dotenv import load_dotenv
load_dotenv()

ollama_base_url = os.getenv("OLLAMA_BASE_URL")
open_router_api_key = os.getenv("OPEN_ROUTER_API_KEY")

ollama = LLM(
    model= 'ollama/hf.co/Triangle104/Mistral-Small-3.1-24B-Instruct-2503-Q4_K_M-GGUF:Q4_K_M',
    base_url= ollama_base_url,
    temperature=0
)

# deepseek_v3 = LLM(
#     model="openrouter/deepseek/deepseek-chat-v3-0324:free",
#     base_url="https://openrouter.ai/api/v1",
#     api_key=open_router_api_key,
#     temperature=0.5
# )

mistral_small = LLM(
    model="openrouter/mistralai/mistral-small-3.1-24b-instruct:free",
    base_url="https://openrouter.ai/api/v1",
    api_key=open_router_api_key,
    temperature=0
)