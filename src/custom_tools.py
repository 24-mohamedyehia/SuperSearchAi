from crewai.tools import tool
from tavily import TavilyClient
from dotenv import load_dotenv
import json
import os
load_dotenv()

search_client = TavilyClient(api_key=os.getenv("TVLY_SEARCH_API_KEY"))
output_dir = os.path.abspath(r'src\Research_crew\research')

@tool
def ask_user_tool(questions: str) -> str:
    """
    This Tool to ask the user clarifying questions during task execution.
    Input should be a string containing one or more questions.
    Returns the user's response as a string.
    """
    print("\n🧠 The agent needs more information from you:\n")
    print(questions)
    answer = input("\n💬 Your answer: ")
    return answer

@tool
def read_json_tool(file_path: str) -> json:
    """
    Read a JSON file from the given file path and return its content as a dictionary.
    Tries to handle encoding errors gracefully.
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except UnicodeDecodeError:
        with open(file_path, 'r', encoding='latin1') as f:
            return json.load(f)

@tool
def search_multiple_queries_tool(queries: list):
    """
    Search for a list of queries and store all results in one JSON file
    Args:
        list of queries to search between []
    """
    all_results = {
        "results": []
    }

    for query in queries:
        results = search_client.search(query, max_results=2, include_images=True)
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
