from helpers import get_base_settings
from providers import InintLMM
import os

class BaseController:
    
    def __init__(self):
        self.app_settings = get_base_settings()
        self.llm_setting = InintLMM()
        self.all_search_result_dir = os.path.join(
            os.path.dirname(__file__),
            "../Research_crew/research/all_search_results.json"
        )
        self.content_dir = os.path.join(
            os.path.dirname(__file__),
            "../Report_crew/final_report/Deep_Research_Report.html"
        )
