from crewai.tools import tool
from tavily import TavilyClient
from dotenv import load_dotenv
from typing import List
import json
import os
load_dotenv()

search_client = TavilyClient(api_key=os.getenv("TVLY_SEARCH_API_KEY"))
output_dir = os.path.abspath(r'src\Quick_Research_crew\research')

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

@tool
def search_multiple_queries_tool(queries: List):
    """
    This method takes a list of queries and store all results in one JSON file
    Args:
        list of queries to search between []
    """
    all_results = {
        "results": []
    }

    for query in queries:
        results = search_client.search(query, max_results=3, include_images=True)
        for result in results['results']:
            single_result = {
                'search_query': results['query'],
                'title': result['title'],
                'url': result['url'],
                'content': result['content'],
                'score': result['score'],
                'image': results['images'][0]    
            }
            all_results['results'].append(single_result)

    file_path = os.path.join(output_dir, 'all_search_results.json')
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(all_results, f, ensure_ascii=False, indent=2)

    return f"Saved {len(all_results['results'])} results to 'all_search_results.json'"
