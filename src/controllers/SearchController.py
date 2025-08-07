from Quick_Research_crew import ResearchCrew
from Deep_Research_crew import DeepResearchCrew
from models import ResponseSignal
from datetime import datetime
from typing import List, Optional
from .BaseController import BaseController
from src.models.search_request import AnswerItem
from helpers import get_markdown_content, get_all_resources_urls, get_all_image_urls
import os
import json
import shutil
import logging

logging.basicConfig(level=logging.INFO, filename='search_controller.log',)
logger = logging.getLogger(__name__)

class SearchController(BaseController):
    QUICK_OUTPUT_DIR = os.path.join(
            os.path.dirname(__file__),
            "../Quick_Research_crew/research/"
        )
    DEEP_OUTPUT_DIR = os.path.join(
            os.path.dirname(__file__),
            "../Deep_Research_crew/research_results/"
        )

    def __init__(self, session_id: str, search_mode: str, query: str, answers: List[AnswerItem], llm_setting=None):
        super().__init__()
        self.llm_setting = llm_setting
        self.session_id = session_id
        self.search_mode = search_mode
        self.query = query
        self.answers = answers
        self.user_details = self._format_user_answers()
        self.session_file = None
        self.report_content = None
        self.all_result_dir = None

    def search(self):
        if os.path.exists(self.QUICK_OUTPUT_DIR):
            shutil.rmtree(self.QUICK_OUTPUT_DIR)
        if os.path.exists(self.DEEP_OUTPUT_DIR):
            shutil.rmtree(self.DEEP_OUTPUT_DIR)
        self._save_session_data("in_progress")  # Save initial session data

        if self.search_mode.lower() == "quick":
            return True, ResponseSignal.STARTED_SEARCH.value
        elif self.search_mode.lower() == "deep":
            return True, ResponseSignal.STARTED_SEARCH.value
        else:
            return False, ResponseSignal.INVALID_SEARCH_MODE.value

    def run_background_tasks(self):
        try:
            if self.search_mode.lower() == "quick":
                self.report_content = os.path.join(self.QUICK_OUTPUT_DIR, 'Research_Report.md')
                self.all_result_dir = os.path.join(self.QUICK_OUTPUT_DIR, 'all_search_results.json')
                ResearchCrew(self.llm_setting).crew().kickoff(inputs={
                    'user_query': self.query,
                    'user_details': self.user_details,
                    'current_date': datetime.now().strftime("%Y-%m-%d"),
                    'no_keywords': 3,
                    'search_results': os.path.join(self.QUICK_OUTPUT_DIR, 'all_search_results.json')
                })
            elif self.search_mode.lower() == "deep":
                self.report_content = os.path.join(self.DEEP_OUTPUT_DIR, 'Research_Report.md')
                self.all_result_dir = os.path.join(self.DEEP_OUTPUT_DIR, 'all_search_results.json')
                DeepResearchCrew(self.llm_setting).crew().kickoff(inputs={
                    'user_query': self.query,
                    'user_details': self.user_details,
                    'current_date': datetime.now().strftime("%Y-%m-%d"),
                    'research_plan': os.path.join(self.DEEP_OUTPUT_DIR, 'Research_Planning.md'),
                })

            self._save_session_data("completed",
                                    report_content=get_markdown_content(self.report_content),
                                    images=get_all_image_urls(self.all_result_dir),
                                    resources=get_all_resources_urls(self.all_result_dir))

        except Exception as e:
            logger.error(f"Error during background tasks: {e}")
            self._save_session_data("failed")
            raise

    def _save_session_data(self, status: str,
                            report_content: Optional[str] = None,
                            images: Optional[List[str]] = None,
                            resources: Optional[List[str]] = None):
        """Save session data to JSON file."""
        session_data = {
            "session_id": self.session_id,
            "status": status,
            "search_mode": self.search_mode,
            "query": self.query,
            "user_details": self.user_details,
            "report": report_content,
            "images": images,
            "resources": resources,
            "created_at": datetime.now().isoformat(),
            "completed_at": datetime.now().isoformat() if status in ["completed", "failed"] else None,
        }

        try:
            if self.search_mode.lower() == "quick":
                self.session_file = os.path.join(self.QUICK_OUTPUT_DIR, f"session_{self.session_id}.json")
            elif self.search_mode.lower() == "deep":
                self.session_file = os.path.join(self.DEEP_OUTPUT_DIR, f"session_{self.session_id}.json")
            os.makedirs(os.path.dirname(self.session_file), exist_ok=True)
            with open(self.session_file, 'w', encoding='utf-8') as f:
                json.dump(session_data, f, indent=2, ensure_ascii=False)
        except Exception as e:
            logger.error(f"Failed to save session data: {e}")
            raise

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
