import csv
from datetime import datetime
import os   # To acces files and folders
import re   # To find URLS using patterns
import fitz # Reads pdf files (comes from PyMuPDF)
import requests # Check if a url works
import argparse
import sys

class Main():

    def __init__(self, args):
       self.args= args
       self.results = []

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
      try:
            # Get headers, follow redirects, wait 5s
            response = requests.head(url, allow_redirects=True, timeout=5)
            return response.status_code
      except:
            # Unreachable, broken, url malformed, site down etc.,
            return "Error"


    @staticmethod
    def is_valid_file(path):
        """Checks if a given file exists"""
        if not os.path.isfile(path):
            print(f'Error: "{path}" is not a valid file')
            sys.exit(1)
        else: 
            print(f'"{path}" is a valid file')
        return path


    def check_urls(self):
        # Use a set to filter out duplicates
        found_urls = set()

        # Change to be arguments
        ##################################################


        ################################################
        folderpath = "documents"
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
            
            found_urls.update(urls)

        print("Checking URLs...\n")
        # sorting them for clarity and debugginh
        for url in sorted(found_urls):
            status = Main.get_response(url)
            print(f"URL: {url}  ->  response:{status}\n\n")


         #sort the urls into a csv file
        for url in sorted(found_urls):
                response_data = Main.get_response(url)
                self.results.append({
                    'url': url,
                    'status_code': Main.get_response(url),
                    'checked_at': datetime.now().isoformat()
                })

        self.write_csv()


    def write_csv(self):
        filename = f"url_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
        with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
            fieldnames = ['url', 'status_code', 'checked_at']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            for row in self.results:
                writer.writerow(row)
        print(f"\nCSV report generated: {filename}")


    def validate_input(self):
        # handles parsing command line arguments
        parser = argparse.ArgumentParser( 
        description="takes in a command line argument"
        )

        parser.add_argument('-i', '--input', metavar='input', type=self.is_valid_file, help='File name of input', required=True)
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