import requests
from requests.models import Response


def create_file(file_path: str) -> None:
    with open(file_path, "w", encoding="utf-8"):
        pass

def add_title_to_file(file_path: str, content: str) -> None:
    with open(file_path, "a", encoding="utf-8") as f:
        f.write(f"{content}\n\n")

def add_content_to_file(file_path: str, content: str) -> None:
    with open(file_path, "a", encoding="utf-8") as f:
        f.write(f"{content}\n\n\n")

def get_html_content(url: str) -> str:
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }
    response: Response = requests.get(url, headers=headers)
    response.encoding = "utf-8"
    return response.text