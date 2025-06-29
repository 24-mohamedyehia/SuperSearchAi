from .StartController import BaseController 
from ..Research_crew import ResearchCrew
from ..Report_crew import ReportCrew
from ..models import ResponseSignal
from datetime import datetime
import os

class SearchController(BaseController):
        def __init__(self, query: str, search_mode: str, answers: str, session_id: str, clarification: list[dict[str, str]]):
            super().__init__()
            self.query = query
            self.search_mode = search_mode
            self.answers = answers
            self.session_id = session_id
            self.user_details = str(clarification) + "\nUser Answers: \n" + self.answers

        def search(self):
            if self.search_mode.lower() == "quick":
                return True, ResponseSignal.STARTED_SEARCH.value
            elif self.search_mode.lower() == "deep":
                return False, ResponseSignal.NOT_YET_IMPLEMENTED.value
            else:
                return False, ResponseSignal.INVALID_SEARCH_MODE.value
            

        def run_background_tasks(self):
            ResearchCrew().crew().kickoff(inputs={
                'user_query': self.query,
                'user_details': self.user_details,
                'current_date': datetime.now().strftime("%Y-%m-%d"),
                'no_keywords': 5,
                'search_queries': os.path.join('./src/Research_crew/research/step_one_search_queries.json')
            })

            ReportCrew().crew().kickoff(inputs={
                'search_results': os.path.join('./src/Research_crew/research/all_search_results.json'),
                'user_query': self.query
            })
