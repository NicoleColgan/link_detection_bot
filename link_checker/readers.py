# link_checker/readers.py
from typing import List
import re
from urllib.parse import urlparse
import fitz  # PyMuPDF

URL_PATTERN = re.compile(r'https?://[^\s)"\'<>]+')  #compile pattern once when module is imported then use find all on already compiled pattern

def extract_urls(text: str) -> List[str]:
    return URL_PATTERN.findall(text or "")  #pattern match empty string if no text

def read_text_file(filepath: str) -> List[str]:
    with open(filepath, 'r', encoding="utf-8") as f:
        return extract_urls(f.read())

def read_pdf_file(filepath: str) -> List[str]:
    urls = []
    with fitz.open(filepath) as f:
        for page in f:
            text = page.get_text()
            urls.extend(extract_urls(text))
    return urls
