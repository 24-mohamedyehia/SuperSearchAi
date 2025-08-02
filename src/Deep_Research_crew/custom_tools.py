import http.client
import requests
from bs4 import BeautifulSoup
from pydantic import BaseModel
from typing import List, Dict
import json
import time
from crewai.tools import tool
from dotenv import load_dotenv
import os
import datetime
load_dotenv()

serper_api_key = os.getenv("SERPER_API_KEY")
output_dir_research = os.path.abspath(r'src\Deep_Research_crew\research_results\research')
output_dir = os.path.abspath(r'src\Deep_Research_crew\research_results')
output_dir_scraped = os.path.abspath(r'src\Deep_Research_crew\scraped_pages')

@tool
def read_search_results_tool(file_path: str) -> list:
    """
    Reads a JSON file from the given file path and returns a list of 'content' fields from each result.
    Converts relative paths to absolute paths and handles encoding errors gracefully.
    """
    abs_path = os.path.abspath(file_path)

    if not os.path.exists(abs_path):
        raise FileNotFoundError(f"File not found: {abs_path}")

    try:
        with open(abs_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except UnicodeDecodeError:
        with open(abs_path, 'r', encoding='latin1') as f:
            data = json.load(f)

    contents = [result["content"] for result in data.get("results", []) if "content" in result]

    return contents

def read_json_files(list_paths: list) -> list:
    """
    Reads multiple JSON files and returns their contents as a list of dictionaries.
    Args:
        list_paths (list): List of file paths to JSON files.
    Returns:
        list: List of dictionaries containing the data from the JSON files.
    """
    data = {}
    for path in list_paths:
        with open(path, 'r', encoding='utf-8') as f:
            data.update(json.load(f))
    return data

@tool
def serper_search_tool(query: str, num_results: int = 5, search_type: str = "search") -> str:
    """
    Performs a search using the SerperDevTool.

    Args:
        query (str): The search query.
        num_results (int): The number of results to return (default is 5).
        search_type (str): The type of search (e.g., "search", "images", "videos") (default is "search").
    Returns:
        str: A confirmation message with the path to the saved search results.
    """
    conn = http.client.HTTPSConnection("google.serper.dev")
    payload = json.dumps({
        "q": query,
        "num": num_results,
        "page": 1,
        "engine": "google"
        })
    headers = {
        'X-API-KEY': serper_api_key,
        'Content-Type': 'application/json'
    }
    conn.request("POST", f"/{search_type}", payload, headers)
    res = conn.getresponse()
    data = res.read()
    data = data.decode("utf-8")
    data = json.loads(data)
    
    timestamp = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
    filename = f"search_{query.replace(' ', '_')}_{timestamp}.json"
    file_path = os.path.join(output_dir_research, filename)
    os.makedirs(output_dir_research, exist_ok=True)
    
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    return f"✅ Search results saved to: {file_path}"

def get_all_search_results() -> list:
    """
    Returns a list of all search results in the specified directory.
    Returns:
        list: A list of search results.
    """
    file_paths = []
    for root, dirs, files in os.walk(output_dir_research):
        for file in files:
            file_paths.append(os.path.join(root, file))

    content = read_json_files(file_paths)
    return content

@tool
def extract_and_save_links_from_search_results() -> str:
    """
    Extracts all URLs from the 'organic' search results section in a JSON response,
    and saves them into a JSON file named 'all_search_results.json'.

    Returns:
        str: A success message indicating the number of links saved.
    """
    try:
        # Get the full search result JSON
        json_data = get_all_search_results()
        
        # Check if 'organic' section exists and has items
        organic_results = json_data.get("organic", [])
        if not organic_results:
            return "No organic search results found in the JSON."

        # Extract links
        links = [item["link"] for item in organic_results if "link" in item]
        if not links:
            return "No links found in the organic search results."

        # Save links to JSON file
        output_data = {"links": links}
        file_path = os.path.join(output_dir, "all_search_results.json")
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(output_data, f, indent=2)

        return f"✅ {len(links)} links have been saved to all_search_results.json."

    except Exception as e:
        return f"❌ An error occurred while extracting or saving links: {e}"


each_page_content_schema = {
    "url": "string",
    "raw_html": "string",
    "clean_text": "string"
}

# PageContent model
class PageContent(BaseModel):
    url: str
    clean_text: str

# Scraper class
class GenericScraper:
    def __init__(self, wait_time: float = 1.0):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)',
            'Accept-Language': 'en-US,en;q=0.9',
        })
        self.wait_time = wait_time

    def fetch(self, url: str) -> str:
        time.sleep(self.wait_time)
        response = self.session.get(url, timeout=15)
        response.raise_for_status()
        return response.text

    def clean_text(self, html: str) -> str:
        soup = BeautifulSoup(html, 'html.parser')
        for tag in soup(['script', 'style']):
            tag.decompose()
        text = soup.get_text(separator=' ', strip=True)
        return ' '.join(text.split())

    def scrape(self, url: str) -> PageContent:
        html = self.fetch(url)
        text = self.clean_text(html)
        return PageContent(url=url, clean_text=text)

# Scraper instance
generic_scraper = GenericScraper()

@tool
def scrape_tool(url_list: list) -> str:
    """This tool scrapes a list of URLs and saves the content to individual JSON files.
    Args:
        url_list (list): List of URLs to scrape.
    Returns:
        str: Confirmation message with the number of pages processed.
    
    Example:
        scrape_tool(["https://example.com/page1", "https://example.com/page2"])
    """
    for i, url in enumerate(url_list, start=1):
        try:
            page_content = generic_scraper.scrape(url)

            data = {
                "url": page_content.url,
                "clean_text": page_content.clean_text
            }

            filename = f"page_{i}.json"
            file_path = os.path.join(output_dir_scraped, filename)
            os.makedirs(output_dir_scraped, exist_ok=True)
            with open(file_path, "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=2)

        except Exception as e:
            print(f"❌ Error scraping {url}: {e}")
    return f"✅ Scraping completed. {len(url_list)} pages processed."
