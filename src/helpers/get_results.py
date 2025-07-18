import json

def get_all_resources_urls(all_search_result_dir: str):
    """ 
    Retrieves all resource URLs from the specified JSON file.
    Returns:
        set: A set of resource URLs.
    """
    try:
        with open(all_search_result_dir, "r", encoding="utf-8") as f:
            data = json.load(f)

        resource_list = []
        for item in data["results"]:
            title = item.get("title")
            url = item.get("url")
            if title and url:
                resource_list.append({"title": title, "url": url})
        return resource_list
    except Exception as e:
        print(e)
        return None

def get_all_image_urls(all_search_result_dir: str):
    """
    Retrieves all image URLs from the specified JSON file.
    Returns:
        set: A set of image URLs.
    """
    try:
        with open(all_search_result_dir, "r", encoding="utf-8") as f:
            data = json.load(f)
        return [item["image"] for item in data["results"] if "image" in item]

    except Exception as e:
        print(e)
        return None

def get_markdown_content(file_path: str) -> str:
    """
    Reads the content of a Markdown (.md) file and returns it as a string.
    
    Parameters:
        file_path (str): The path to the Markdown file.
    
    Returns:
        str: The content of the Markdown file, or None if an error occurs.
    """
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()
        return content
    except Exception as e:
        print(f"Error reading Markdown file: {e}")
        return None

