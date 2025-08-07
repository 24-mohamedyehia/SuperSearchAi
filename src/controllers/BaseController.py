from helpers import get_base_settings
from providers import InintLMM
import os

class BaseController:
    
    def __init__(self):
        self.app_settings = get_base_settings()
        self.llm_setting = InintLMM()
