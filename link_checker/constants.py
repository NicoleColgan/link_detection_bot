VALIDITY_PROMPT = """
        You are checking whether a link on a website is acceptable for end users, not just technically reachable.

        Use the following link check results:
        - original_url: {original_url}
        - response_url: {response_url}
        - status_code: {status_code}
        - ok: {ok}
        - is_redirect: {is_redirect}
        - redirect_chain: {redirect_chain}
        - reason: {reason}
        - cookies: {cookies}
        - elapsed: {elapsed}
        - request_method: {request_method}
        - content_snippet: {content_snippet}
        - signals: {signals}

        Rules for reasoning:
        1. Do not rely on status_code=200 or ok=True alone. Many pages return 200 but may be user-unfriendly (custom 404s, empty, or placeholder pages).
        2. Redirects and response_url should be checked — if the final page is broken, empty, placeholder, or clearly an error page, flag it. 
        3. content_snippet is a strong signal: empty content, "404", "not found", "coming soon", or other obvious placeholder text should mark it as bad.
        4. signals are extracted from the response text and may include known issues or heuristics — treat them as hints.
        5. Other fields (elapsed, cookies, request_method) provide context but are not decisive.
        6. A page is acceptable if it delivers content that functions correctly. 
        7. Pages requiring login or authentication are considered acceptable and should **not** be flagged as bad.
    
        {format_instructions}
    """