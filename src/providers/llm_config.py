
class BaseLLMConfig:
    def get_config(self):
        raise NotImplementedError

class OpenRouterConfig(BaseLLMConfig):
    def __init__(self, model_name: str):
        self._model_name = model_name
    
    def get_config(self):
        return {
            "base_url": "https://openrouter.ai/api/v1",
            "model": self._model_name,
            "temperature": 0,
        }

class OllamaConfig(BaseLLMConfig):
    def __init__(self, model_name: str, base_url: str):
        self._model_name = model_name
        self._base_url = base_url
    
    def get_config(self):
        return {
            "base_url": self._base_url,
            "model": self._model_name,
            "temperature": 0,
        }

def get_provider_config(provider_name: str, model_name: str, base_url: str):
    if provider_name == "openrouter":
        return OpenRouterConfig(model_name)
    elif provider_name == "ollama":
        if base_url == "":
            base_url = "http://localhost:11434"
        return OllamaConfig(model_name, base_url)
    else:
        raise ValueError("Unsupported provider")