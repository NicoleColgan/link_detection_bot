import csv
from datetime import datetime
import os   # To acces files and folders
import re   # To find URLS using patterns
import fitz # Reads pdf files (comes from PyMuPDF)
import requests # Check if a url works
import argparse
import sys
import time
from urllib.parse import urlparse, urlunparse
from langchain_community.chat_models import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from dotenv import load_dotenv, find_dotenv
from langchain.output_parsers import ResponseSchema, StructuredOutputParser
from langchain.chains import SequentialChain
# Place this at the top of your script, after imports but before any class or function definitions. This way, your environment variables are loaded before any code that needs them runs.
_ = load_dotenv(find_dotenv())

class Main():
    VALIDITY_PROMPT = """
        You are checking whether a link on a website is acceptable for end users, not just technically reachable.

        Use the following link check results:
        - original_url: {original_url}
        - response_url: {response_url}
        - status_code: {status_code}
        - reason: {reason}
        - ok: {ok}
        - is_redirect: {is_redirect}
        - elapsed: {elapsed}
        - redirect_chain: {redirect_chain}
        - cookies: {cookies}
        - request_method: {request_method}
        - content_snippet: {content_snippet}
        - signals: {signals}

        Rules for reasoning:
        1. Do not rely on status_code=200 or ok=True alone. Many pages return 200 but may be user-unfriendly (custom 404s, empty, or placeholder pages).
        2. Redirects and response_url should be checked — if the final page is broken, empty, placeholder, or clearly an error page, flag it. Login pages should **not** be considered broken.
        3. content_snippet is a strong signal: empty content, "404", "not found", "coming soon", or other obvious placeholder text should mark it as bad.
        4. signals are extracted from the response text and may include known issues or heuristics — treat them as hints.
        5. Other fields (elapsed, cookies, request_method) provide context but are not decisive.
        6. A page is acceptable if it delivers content that functions correctly. Pages requiring login or authentication are considered acceptable and should **not** be flagged as bad.
        
        {format_instructions}
    """
    def install_dependencies(self):
            #!pip install pandas
            print("install_dependencies function not yet defined")

    def __init__(self, args):
       self.args= args
       self.results = []
       self.install_dependencies()
       # Add a little randomness for creativity
       self.llm=ChatOpenAI(temperature=0.9)

    @staticmethod
    def normalise_url(url):
        parsed = urlparse(url.strip())  #strip() removes whitespace and urlparse() seperates it into url parts
        stripped = parsed._replace(fragment="", query=parsed.query.strip()) #remove fragment(specific section of page pointing to) & strip whitespace from query
        return urlunparse(stripped).rstrip('/') #rebuild url after cleaning and remove trailing slash
    
    @staticmethod
    def extract_urls(content):
        # r = raw string (treat backslashes as literal character not escape characters)
        # https? = match http literally with an optional s (s?) + '://' = matches https:// or http://
        # [^] - match anything other than these characters
        # \s = whitespace, '"'<>" literal chearacters that usually end a url in files eg "url" (notice quotes) or <http...> in md files or  () in mds
        # => last part matches everything else but stops at the point where the url usually ends 
        # "+" = keep matching as long as your seeing valid characters
        pattern = r'https?://[^\s)"\'<>]+'
        return re.findall(pattern, content)

    @staticmethod
    def read_text_file(filepath):
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
            return Main.extract_urls(content)

    @staticmethod
    def read_pdf_file(filepath):
        urls = []
        with fitz.open(filepath) as f:
            for page in f:
                content = page.get_text()
                urls.extend(Main.extract_urls(content))
        return urls

    @staticmethod
    def get_response(url):
        url = Main.normalise_url(url)
        for attempt in range(2):
            try:     
                headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}
                response = requests.get(url, headers=headers, allow_redirects=True, timeout=10)
                return response
            except Exception:
                # Try once more but wait one second
                if attempt == 0:
                    print(f"{url} → 🔁 Retrying once...")
                    time.sleep(1)
                else:
                    # Unreachable, broken, url malformed, site down etc.,
                    return None

    @staticmethod
    def is_valid_directory(path):

        if not os.path.isdir(path):
            print(f'Error: "{path}" is not a valid directory')
            sys.exit(1)
        elif not any(os.path.isfile(os.path.join(path, f)) for f in os.listdir(path)):
            print(f'Error: "{path}" is a directory but contains no files')
            sys.exit(1)
        else:
            print(f'"{path}" is a valid directory with files')
            return path
       
    def write_csv(self):
        filename = f"url_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
        with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
            fieldnames = ['url', 'status_code', 'status_code_meaning', 'reachable', 'redirected', 'final_url', 'redirect_chain', 'checked_at']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            for row in self.results:
                writer.writerow(row)
        print(f"\nCSV report generated: {filename}")

    # prob should use something like this
    def format_prompt(self, response_info):
        prompt_template = ChatPromptTemplate.from_template(self.TEMPLATE_STRING)

        return prompt_template.format_messages(
            style=self.STYLE,
            url=response_info["url"],
            status_code=response_info["status_code"],
            reason=response_info["reason"],
            ok=response_info["ok"],
            is_redirect=response_info["is_redirect"],
            elapsed=response_info["elapsed"],
            redirect_chain=response_info["redirect_chain"],
            cookies=response_info["cookies"],
            request_method=response_info["request_method"],
            content_snippet=response_info["content_snippet"],
            checked_at=response_info["checked_at"]
        )

    #is this the best way to do this?
    def generate_response_schemas(self):
        # use langchain parser to extract json
        usable_schema = ResponseSchema(name="usable", description="Is this link actually usable for a user? Answer with 'True' if it is, 'False' if it is not, and 'Unknown' if you are not sure")
        reason_schema = ResponseSchema(name="reason", description="Explanation as to why you answered True or False to whether or not its usable")
        resolution_steps = ResponseSchema(name="resolution_steps", description="suggest possible next steps for the user if the link is not usable. if it is usable, just output 'N/A'")
        return [usable_schema, reason_schema, resolution_steps]
    
    def check_link_validity(self, response_info):
        prompt_template = ChatPromptTemplate.from_template(self.VALIDITY_PROMPT)
        response_schemas = self.generate_response_schemas()
        output_parser = StructuredOutputParser(response_schemas=response_schemas)
        format_instructions = output_parser.get_format_instructions()

        messages = prompt_template.format_messages(
            original_url=response_info["original_url"],
            response_url=response_info["response_url"],
            status_code=response_info["status_code"],
            reason=response_info["reason"],
            ok=response_info["ok"],
            is_redirect=response_info["is_redirect"],
            elapsed=response_info["elapsed"],
            redirect_chain=response_info["redirect_chain"],
            cookies=response_info["cookies"],
            request_method=response_info["request_method"],
            content_snippet=response_info["content_snippet"],
            signals=response_info["signals"],
            format_instructions=format_instructions
        )
        validity_response = self.llm(messages)
        output_dict = output_parser.parse(validity_response.content)
        
        return output_dict.get("usable"), output_dict.get("reason"), output_dict.get("resolution_steps")

    def detect_signals(self, response):
        #check if theres amy red flag key words in response to indicate an issue (page could hazve a custom error page which would return ok but isnt)

        signals=[]

        if not response or response.text == "":
            return signals.append("error")
        
        snippet = response.text[:500].lower()
        for word in ["coming soon", "not found", "404", "error", "forbidden"]:
            if word in snippet:
                signals.append(word)

        return signals
    
    def check_urls(self):
        # Use a set to filter out duplicates
        found_urls = set()
        folderpath = self.args.input
        # Go through every file in the folder
        for filename in os.listdir(folderpath):
            filepath = os.path.join(folderpath, filename)

            # Only working with md, html and pdf files currently
            if filename.endswith('.md') or filename.endswith('.html'):
                urls = Main.read_text_file(filepath)
            elif filename.endswith('.pdf'):
                urls = Main.read_pdf_file(filepath)
            else:
                print(f"{filename} skipped - only accepts .md, .pdf, and .html files")
            # only add urls if some were found
            if urls:
                found_urls.update(urls)

        print("Checking URLs...\n")

        # sorting them for clarity and debugging
        for url in sorted(found_urls):
            # status, was_redirected, final_url, redirect_chain = Main.get_response(url)
            response = Main.get_response(url)
            checked_at = datetime.now().isoformat()
            
            if response is None:
                response_info = {}
            else:
                signals= self.detect_signals(response)
                response_info = {
                "original_url": url,
                "response_url": response.url,
                "reason": response.reason,
                "status_code": response.status_code,
                "ok": response.ok,
                "is_redirect": response.is_redirect,
                "elapsed": response.elapsed,
                "redirect_chain": [redirect.url for redirect in response.history],
                "cookies": response.cookies,
                "request_method": response.request.method,
                "content_snippet": response.text[:500],
                "signals": signals,
                "checked_at": checked_at
                }
            
            # Use LLM to check link validity cause even some 200s arent ok
            usable, reason, resolution_steps = self.check_link_validity(response_info)
            self.results.append({
                "original_url": url,
                "usable": usable,
                "reason": reason,
                "resolution_steps": resolution_steps
            })
            #print(f"{self.results[-1]}\n")

        self.write_csv()

    def validate_input(self):
        # handles parsing command line arguments
        parser = argparse.ArgumentParser( 
            description="takes in a command line argument"
        )

        parser.add_argument('-i', '--input', metavar='input', type=self.is_valid_directory, help='File name of input', required=True)
        self.args = parser.parse_args()

        print(f"Validated input path: {self.args.input }")

    def run(self):
        self.validate_input()
        self.check_urls()

def main(args):
   app = Main(args)
   app.run()

if __name__ == "__main__":
    main(sys.argv[1:])