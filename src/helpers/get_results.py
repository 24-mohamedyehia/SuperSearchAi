import os
import json

def get_all_resources_urls(all_search_result_dir: str):
    """ 
    Retrieves all resource URLs from the specified JSON file.
    Returns:
        set: A set of resource URLs.
    """
    with open(all_search_result_dir, "r", encoding="utf-8") as f:
        data = json.load(f)

    resource_list = []
    for item in data["results"]:
        title = item.get("title")
        url = item.get("url")
        if title and url:
            resource_list.append({"title": title, "url": url})
    return resource_list

def get_all_image_urls(all_search_result_dir: str):
    """
    Retrieves all image URLs from the specified JSON file.
    Returns:
        set: A set of image URLs.
    """
    with open(all_search_result_dir, "r", encoding="utf-8") as f:
        data = json.load(f)
    return [item["image"] for item in data["results"] if "image" in item]

def get_html_content(content_dir: str):
    """
    Reads the HTML content from the specified file.
    """
    with open(content_dir, "r", encoding="utf-8") as f:
        return f.read()
