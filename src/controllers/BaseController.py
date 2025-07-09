from helpers import get_base_settings
from providers import InintLMM
import os

class BaseController:
    
    def __init__(self):
        self.app_settings = get_base_settings()
        self.llm_setting = InintLMM()
        self.all_result_dir = os.path.join(
            os.path.dirname(__file__),
            "../Quick_Research_crew/research/all_search_results.json"
        )
        self.report_content = os.path.join(
            os.path.dirname(__file__),
            "../Quick_Research_crew/research/Research_Report.json"
        )