from ..helpers import get_settings 
import os

class BaseController:
    
    def __init__(self):
        self.app_settings = get_settings()
        self.all_search_result_dir = os.path.join(
            os.path.dirname(__file__),
            "../Research_crew/research/all_search_results.json"
        )
        self.content_dir = os.path.join(
            os.path.dirname(__file__),
            "../Report_crew/final_report/Deep_Research_Report.html"
        )
