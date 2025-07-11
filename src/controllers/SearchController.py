from Quick_Research_crew import ResearchCrew
from models import ResponseSignal
from datetime import datetime
from typing import List, Optional
from .BaseController import BaseController
from src.models.search_request import AnswerItem
from helpers import get_json_content, get_all_resources_urls, get_all_image_urls
import os
import json

class SearchController(BaseController):
    def __init__(self, session_id: str, search_mode: str, query: str, answers: List[AnswerItem], llm_setting=None):
        super().__init__()
        self.llm_setting = llm_setting
        self.session_id = session_id
        self.search_mode = search_mode
        self.query = query
        self.answers = answers
        self.user_details = self._format_user_answers()
        self.session_file = f"./src/Quick_Research_crew/research/session_{self.session_id}.json"

    def search(self):
        # Save initial session data
        self._save_session_data("in_progress")

        if self.search_mode.lower() == "quick":
            return True, ResponseSignal.STARTED_SEARCH.value
        elif self.search_mode.lower() == "deep":
            return False, ResponseSignal.NOT_YET_IMPLEMENTED.value
        else:
            return False, ResponseSignal.INVALID_SEARCH_MODE.value

    def run_background_tasks(self):
        try:
            ResearchCrew(self.llm_setting).crew().kickoff(inputs={
                'user_query': self.query,
                'user_details': self.user_details,
                'current_date': datetime.now().strftime("%Y-%m-%d"),
                'no_keywords': 3,
                'search_results': os.path.join('src/Quick_Research_crew/research/all_search_results.json')
            })

            self._save_session_data("completed")    # Update session data with results

        except Exception as e:
            self._save_session_data("failed", error=str(e))

    def _save_session_data(self, status: str, error: Optional[str] = None):
        """Save session data to JSON file."""
        session_data = {
            "session_id": self.session_id,
            "status": status,
            "search_mode": self.search_mode,
            "query": self.query,
            "user_details": self.user_details,
            "report": get_json_content(self.report_content),
            "images" : get_all_image_urls(self.all_result_dir),
            "resources": get_all_resources_urls(self.all_result_dir),
            "created_at": datetime.now().isoformat(),
            "completed_at": datetime.now().isoformat() if status in ["completed", "failed"] else None,
            "error": error
        }

        try:
            os.makedirs(os.path.dirname(self.session_file), exist_ok=True)
            with open(self.session_file, 'w', encoding='utf-8') as f:
                json.dump(session_data, f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"Error saving session data: {e}")

    def _format_user_answers(self) -> str:
        """Format the answers from AnswerItem objects into a readable string."""
        if not self.answers:
            return ResponseSignal.NO_ANSWERS_PROVIDED

        formatted_answers = {}
        for answer in self.answers:
            # Access AnswerItem attributes, not dictionary keys
            formatted_answers[answer.question_id] = answer.choice

        # Convert to readable format
        answer_strings = []
        for question_id, choice in formatted_answers.items():
            answer_strings.append(f"Question {question_id} - {answer.question}: {choice}")

        return "User Answers:\n" + "\n".join(answer_strings)
