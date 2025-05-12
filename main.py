# todo 
# validation of document directory
# Input parameters from user
import os   # To acces files and folders
import re   # To find URLS using patterns
import fitz # Reads pdf files (comes from PyMuPDF)



def extract_urls(content):
    # r = raw string (treat backslashes as literal character not escape characters)
    # https? = match http literally with an optional s (s?) + '://' = matches https:// or http://
    # [^] - match anything other than these characters
    # \s = whitespace, '"'<>" literal chearacters that usually end a url in files eg "url" (notice quotes) or <http...> in md files or  () in mds
    # => last part matches everything else but stops at the point where the url usually ends 
    # "+" = keep matching as long as your seeing valid characters
    pattern = r'https?://[^\s)"\'<>]+'
    return re.findall(pattern, content)

def read_text_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
        return extract_urls(content)

def read_pdf_file(filepath):
    urls = []
    with fitz.open(filepath) as f:
        for page in f:
            content = page.get_text()
            urls.extend(extract_urls(content))
    return urls

found_urls = set()
folderpath="documents"
# Go through every file in the folder
for filename in os.listdir(folderpath):
    filepath = os.path.join(folderpath, filename)

    # Only working with md, html and pdf files currently
    if filename.endswith('.md') or filename.endswith('.html'):
        urls = read_text_file(filepath)
    elif filename.endswith('.pdf'):
        urls = read_pdf_file(filepath)