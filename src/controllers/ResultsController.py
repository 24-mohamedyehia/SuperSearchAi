from .BaseController import BaseController
from models import ResponseSignal
import os
import json

class ResultsController(BaseController):
    def __init__(self, session_id: str):
        super().__init__()
        self.session_id = session_id
    
    def get_results(self):
        final_report = self._get_final_report()

        if final_report is None:
            return False, ResponseSignal.NO_RESULTS_FOUND.value
        else:
            return True, final_report
    def _get_final_report(self):

        file_path = os.path.join(
            os.path.dirname(__file__),
            f"../Quick_Research_crew/research/session_{self.session_id}.json"
        )  

        try:
            with open(file_path, "r", encoding="utf-8") as f:
                data = json.load(f)
            return data
        except Exception as e:
            print(e)
            return None