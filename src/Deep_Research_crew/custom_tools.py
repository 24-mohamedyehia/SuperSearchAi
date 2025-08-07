import http.client
import requests
from bs4 import BeautifulSoup
from pydantic import BaseModel
from typing import List, Dict, Union
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
output_dir_scraped = os.path.abspath(r'src\Deep_Research_crew\research_results\knowledge')


@tool
def file_json_read_tool(file_path: str):
    """
    Tries to read a JSON file using utf-8 and latin-1 encodings.
    Returns the content as a dictionary, or None if all attempts fail.
    """
    if not os.path.exists(file_path):
        print(f"❌ File not found: {file_path}")
        return None

    for encoding in ['utf-8', 'latin-1']:
        try:
            with open(file_path, 'r', encoding=encoding) as f:
                data = json.load(f)
                print(f"✅ Successfully loaded JSON using encoding: {encoding}")
                return data
        except UnicodeDecodeError:
            print(f"⚠️ UnicodeDecodeError with encoding: {encoding}")
        except json.JSONDecodeError:
            print(f"⚠️ JSONDecodeError with encoding: {encoding}")
        except Exception as e:
            print(f"⚠️ Other error with encoding {encoding}: {e}")

    print("❌ Failed to read the JSON file with utf-8 and latin-1 encodings.")
    return None


@tool
def get_knowledge_json_paths():
    """
    this function returns a list of all JSON file paths in the specified directory.
    Returns:
        list: A list of JSON file paths.
    """
    file_paths = []
    for root, dirs, files in os.walk(output_dir_scraped):
        for file in files:
            file_paths.append(os.path.join(root, file))
    return file_paths

def read_search_results_tool() -> list:
    """
    Reads a JSON file from the given file path and returns a list of links.
    Converts relative paths to absolute paths and handles encoding errors gracefully.
    
    Returns:
        list: List of links extracted from the JSON file.
    """
    file_path = os.path.join(output_dir, "all_search_results.json")
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except UnicodeDecodeError:
        with open(file_path, 'r', encoding='latin1') as f:
            data = json.load(f)

    links = data.get("results", [])

    return links

def read_json_files(list_paths: list):
    """
    Reads multiple JSON files and returns their contents as a list of dictionaries.
    Args:
        list_paths (list): List of file paths to JSON files.
    Returns:
        list: List of dictionaries containing the data from the JSON files.
    """
    data = []
    for path in list_paths:
        with open(path, 'r', encoding='utf-8') as f:
            data.append(json.load(f))
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
def extract_links_and_save():
    """
    Extracts all 'link' values from nested JSON structure and saves them in a new JSON file.
    
    returns:
        str: A message indicating the number of links saved.
    """
    json_data = get_all_search_results()
    all_links = {
        "results": []
    }

    try:
        for block in json_data:
            if 'organic' in block:
                for result in block['organic']:
                    if 'link' in result:
                        all_links["results"].append(result['link'])

        file_name = os.path.join(output_dir, "all_search_results.json")
        with open(file_name, 'w', encoding='utf-8') as f:
            json.dump(all_links, f, ensure_ascii=False, indent=4)
    except Exception as e:
        return f"❌ Error extracting links: {e}"

    return f"{len(all_links['results'])} links saved to {file_name}"


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
def scrape_tool() -> str:
    """    Scrapes web pages from a list of URLs and saves the content to JSON files.
    Returns:
        str: A message indicating the completion of the scraping process.
    """
    url_list = read_search_results_tool()

    for i in range(0, len(url_list), 2):  
        try:
            url = url_list[i]
            page_content = generic_scraper.scrape(url)

            data = {
                "url": page_content.url,
                "clean_text": page_content.clean_text
            }

            filename = f"page_{i+1}.json"
            file_path = os.path.join(output_dir_scraped, filename)
            os.makedirs(output_dir_scraped, exist_ok=True)
            with open(file_path, "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=2)

        except Exception as e:
            print(f"❌ Error scraping {url}: {e}")
    return f"✅ Scraping completed. {len(range(0, len(url_list), 2))} pages processed."
