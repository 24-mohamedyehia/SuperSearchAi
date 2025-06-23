from .BaseController import BaseController
from ..Research_crew import ResearchCrew
from ..Report_crew import ReportCrew
from datetime import datetime
import os
from ..models import ResponseSignal

class ResearchController(BaseController):
    def __init__(self):
        super().__init__()

    def get_user_input(self, topic: str, search_way: int):

        if topic.strip() == "":
            return False, ResponseSignal.INVALID_TOPIC.value
        if search_way not in [1, 2]:
            return False, ResponseSignal.INVALID_SEARCH_WAY.value

        if search_way == 1:
            # ResearchCrew().crew().kickoff(inputs={
            #     'user_query': topic,
            #     'no_keywords': 2,
            #     'current_date': datetime.now().strftime("%Y-%m-%d"),
            #     'search_queries': os.path.join('./src/Research_crew/research/step_one_search_queries.json')
            # })

            ReportCrew().crew().kickoff(inputs={
                'search_results': os.path.join('./src/Research_crew/research/all_search_results.json'),
                'user_query': topic
            })
        elif search_way == 2:
            pass
        return True, ResponseSignal.RESEARCH_COMPLETED.value
