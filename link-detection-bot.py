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

class Main():
    STATUS_MEANINGS = {
        200: "OK",
        301: "Permanantely Moved",
        302: "Found (Redirect)",
        403: "Forbidden",
        404: "Not Found",
        500: "Internal Server Error",
        502: "Bad Gateway",
        503: "Service Unavailable",
        "Error": "Unreachable or Timed Out"
    }

    def __init__(self, args):
       self.args= args
       self.results = []

    def explain_status(self, code):
        return self.STATUS_MEANINGS.get(code)
    
    @staticmethod
    def is_link_ok(code):
        return code in [200, 301, 302]

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
    def check_redirects(url, response):
        final_url = response.url
        redirect_chain = [r.url for r in response.history]
        was_redirected = url != final_url
        return was_redirected, final_url, redirect_chain

    @staticmethod
    def get_response(url):
        url = Main.normalise_url(url)
        for attempt in range(2):
            try:
                # Get headers, follow redirects, wait 5s
                response = requests.head(url, allow_redirects=True, timeout=5)
                was_redirected, final_url, redirect_chain = Main.check_redirects(url, response)
                return response.status_code, was_redirected, final_url, redirect_chain
            except Exception:
                # Try once more but wait one second
                if attempt == 0:
                    print(f"{url} → 🔁 Retrying once...")
                    time.sleep(1)
                else:
                    # Unreachable, broken, url malformed, site down etc.,
                    return "Error", "Error", "Error", "Error"

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
            status, was_redirected, final_url, redirect_chain = Main.get_response(url)
            self.results.append({
                "url": url,
                "status_code": status,
                "status_code_meaning": self.explain_status(status),
                "reachable": "yes" if Main.is_link_ok(status) else "No",
                "redirected": was_redirected,
                "final_url": final_url,
                "redirect_chain": redirect_chain,
                'checked_at': datetime.now().isoformat()
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