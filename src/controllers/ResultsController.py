from .BaseController import BaseController
from ..models import ResponseSignal
from ..helpers import get_all_resources_urls, get_all_image_urls, get_html_content

class ResultsController(BaseController):
    def __init__(self):
        super().__init__()
    
    def get_results(self):
        images = get_all_image_urls(self.all_search_result_dir)
        resources = get_all_resources_urls(self.all_search_result_dir)
        html_content = get_html_content(self.content_dir)

        if not images or not resources or not html_content:
            return False, ResponseSignal.NO_RESULTS_FOUND.value
        else:
            return True, {
                "images": images,
                "content": html_content,
                "resources": resources
            }

