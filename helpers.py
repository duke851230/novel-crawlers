import time
import functools
import requests
from requests.models import Response
from requests.exceptions import RequestException


def retry(max_retries=3, delay=5):
    """
    A decorator for retrying a function if a RequestException occurs.
    """
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            for attempt in range(max_retries):
                try:
                    return func(*args, **kwargs)
                except RequestException as e:
                    print(f"Attempt {attempt + 1} failed: {e}")
                    if attempt + 1 < max_retries:
                        print(f"Retrying in {delay} seconds...")
                        time.sleep(delay)
                    else:
                        print("Max retries reached. Failing.")
                        raise
        return wrapper
    return decorator


def create_file(file_path: str) -> None:
    with open(file_path, "w", encoding="utf-8"):
        pass

def add_title_to_file(file_path: str, content: str) -> None:
    with open(file_path, "a", encoding="utf-8") as f:
        f.write(f"{content}\n\n")

def add_content_to_file(file_path: str, content: str) -> None:
    with open(file_path, "a", encoding="utf-8") as f:
        f.write(f"{content}\n\n\n")

@retry()
def get_html_content(url: str) -> str:
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }
    response: Response = requests.get(url, headers=headers)
    response.raise_for_status()
    response.encoding = "utf-8"
    return response.text