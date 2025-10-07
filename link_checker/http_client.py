import logging
from urllib.parse import urlparse, urlunparse
from typing import Optional, Tuple, List
import requests
import time

"""


Did we stop using signalss???



"""


logger = logging.getLogger(__name__)    #create logger with name of this file

def normalise_url(url: str) -> str:
    parsed = urlparse(url.strip())  #strip() removes whitespace and urlparse() seperates it into url parts
    stripped = parsed._replace(fragment="", query=parsed.query.strip()) #remove fragment(specific section of page pointing to) & strip whitespace from query
    return urlunparse(stripped).rstrip('/') #rebuild url after cleaning and remove trailing slash

def get_response(url: str, timeout: int = 10, max_retries: int = 2, base_delay: float = 1.0) -> Optional[requests.Response]:
    """Return requests.Response of None on failure. Retries twice by default"""
    url = normalise_url(url)
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}   #mimic user visiting site
    attempts = 0

    while attempts <= max_retries:
        try:
            resp = requests.get(url, headers=headers, allow_redirects=True, timeout=timeout)
            return resp
        except requests.RequestException as exc:
            logger.debug("Reques failed for %s: %s (attempt %s)", url, exc, attempts + 1)
            if attempts < max_retries:
                delay = base_delay * (2 ** (attempts - 1)) #exponential backoff
                time.sleep(delay)
            attempts += 1
    return None

def build_response_info(url: str, resp: Optional[requests.Response]) -> dict:
    if resp is None:
        return {
            "original_url": url,
            "response_url": None,
            "status_code": None,
            "ok": False,
            "is_redirect": False,
            "redirect_chain": [],
            "reason": "no response",
            "cookies": None,
            "elapsed": None,
            "request_method": None,
            "content_snippet": "",
        }
    return {
        "original_url": url,
        "response_url": resp.url,
        "status_code": resp.status_code,
        "ok": resp.ok,
        "is_redirect": len(resp.history) > 0,
        "redirect_chain": [r.url for r in resp.history],
        "reason": resp.reason,
        "cookies": dict(resp.cookies),  #convert RequestsCookieJar to dict so  it is JSON-Serialisable which is required by llm
        "elapsed": getattr(resp, "elapsed", None),  #getattr is a safe way of saying if elapsed exists get it or else make it none (elapsed doesnt always exist unlike the other attrivutes)
        "request_method": resp.request.method if resp.request is not None else None,
        "content_snippet": (resp.text[:500] if resp.text else ""),
    }