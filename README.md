# Project scope
This project is a personal learning initiaive designed to explore technologies we already use. We are setting out to build a Link Validation & Dead Link Detection Bot: an intelligent system that automatically crawls a set of pages, checks for broken or outdated links, and stores a historical log of what has changed and when.

The project aims to deepen our understanding of tools like Python CLI dev, React, Next.js, and LLMS while also exploring concepts like crawling, parsing, content comparison, similarity detection and ui design. There is the added benefit of designing a project that meaningfully sharpens our technical skills, reinforces best practices, and creates something useful that we could also maintain and showcase independently.

This side-project is an opportunity to hone our skills across multiple areas of development, without the use of any confidential data. While the focus is on upskilling and mentorship, there may be potential for future commercial integration if the tool proves useful.

## details
1. Input sources: lets start with files??
2. Output: csv of broken links
3. Initially flag just 404s?
4. optional extras

## How to run
```
usage: link-detection-bot.py [-h] -i input

takes in a command line argument

options:
  -h, --help            show this help message and exit
  -i input, --input input
                        File name of input
```

## TODO:
### For next week
#### Link summariser
- ~~set up prompt template (nicole)~~
- ~~call llm using langchains cht model wrapper (nicole)~~
- extract json entries from completion
- add explanation to csv
- ask user which llm to use - default chat
- add retry logic & fallback
- pass Headers (if available): Response headers, which may indicate blocks, SSL issues, or bot detection.
- Error details (if any): Exception message or timeout info.
- build a simple ui (node.js??/ streamlit/ flask) to demo feature 
- add requrements block which installs required packages

## Done to date
- Research technologies and look through common pages to find broken links to ensure project is useful (Nicole & Oisin)
- Find more broke links (Oisin)
- Create the base python script - just one main, init, whatever - base script that accepts command line arguments (Oisin)
- Update read me with your parts (oisin)
- Create a directory of documents (Nicole)
- Reading in all the documents and checking the urls on the current page are good or not (Nicole)
- Update txt file and send to nicole (Oisin)
- Update code to accept user input of document & input validation of directories (Oisin)
- Print output to csv (Oisin)
- Document other things we should check about links (Nicole)
- Retrying once if url fails (Nicole)
- Check for different error codes and document error code meanings (Nicole)
- Clean urls (Nicole)
- Document if urls are reachable

### Future
- What other things to check in url - dif error codes etc., eg page not found, network error etc
    - timeouts/ retried (nicole) -main
    - was it redirected? -  print redirect chain (nicole) - main
    - content type (nicole)
    - ssl certificae validity (use https? ssl cert valid?) (nicole) - main body of work
    - Domain analysis (blocklsit, shortened link, phishing/ malicious link?) (oisin) - main body of work
    - content inspection? (keywords, js redirects, suspicious code) (oisin)
    - Response size and headers (nicole)
    - Rate limits or bot detection
    - Caching and expiry
- print to output directory so we can keep track of things
- add progress bar when printing to csv & checking urls - or print checking url...?
- spit broken links to csv (Oisin or nicole - not sure)
- Check not only if theyre 404s but if the link exists period
- doc tavble - last updated
- dont visit malicious links? link validation

## notes:
- It should periodically crawling page (recursively eg follow a docs links link...)
- Need to be able to easily plug in different websites/ docs or something somehow to make it a useful tool for a variety of purposes
- AI Use: Detect semantic change (e.g., if firmware has been renamed or replaced) not just broken URLs.
- We can use react/ next js to build a simple ui where you can insert a url to recursively check links
- The tool automatically checks whether urls on a page are:
    1. alive or dead
    2. Have changed signifigantly over time
    3. Flag suspicious or broken pages using intelligent comparison - slow responses
- how do we give it something to check?? maybe we do something similar like we did & download files or just give it a list of files or links (in the case of wiki, i guess it would be a url but it also could be for the file to be fair so maybe a list of urls in a csv or something). Probably easier to start with explicit in put eg a directory with files in it or wikis etc then add crawling functionality later

## Future work
- Add input parameters (parsers) and input validation eg valid document directory
- could consider crawling with dept limit
- Integreation with llms to summarise content, suggest fixes
- ui to upload files/ urls?
- What file formats to consider
- Just realised we cant do the whoel recursive search yet if were using documents (unless we download a document fromn the url and repeat the process). This is more so viable if were using urls to search through pages.
- spit into a db


### AI
1. Broken link explainer If you’re checking links and get errors or 404s:
    - Use AI to explain why a link might be broken.
    - Complex scenarios: Sometimes, the reason isn’t obvious from the status code alone. For example, a redirect chain might show a link bouncing between domains, or headers might reveal a blocklist, expired SSL, or bot detection.
User-friendly explanations: AI can summarize technical details (redirects, headers, errors) into plain English, tailored for non-technical users.
    - Feed it the history/redirects, headers, and have it give a user-friendly explanation.
    - “This link likely failed because the domain is misconfigured or expired.”
    - Contextual suggestions: AI can suggest next steps (e.g., “Try contacting the site owner,” “Check if the domain has expired,” “This link may be blocked by your network”).
    - This becomes more useful as the app scales because as you add more checks (SSL, phishing, content inspection), AI can combine all signals for a holistic explanation.
2. AI Summarizer for Documents
    - For .pdf, .html, .md files you're already scanning, use LangChain to:
    - Summarize the file.
    - Highlight key points or check for policy terms.
    - Use TextLoader + chunking + summarization chains.

This gives a direct showcase of embeddings, chains, and LLM integration.
🧠 Stack You Could Use
- LangChain for building pipelines or agents.
- OpenAI or Claude for reasoning and summarization.
- FAISS / Chroma for document embedding + retrieval.
- Streamlit or Flask for showing a working demo.

✅ Tips for Impressiveness
- Use prompt templates and show prompt engineering skill.
- Add retry logic, fallback models, and tool use (e.g. metadata extractor).
- Document it! Show architecture diagrams and example queries in README.

## Oisins learning
1. used a gitignore for the first time to hide stuff from the version control
2. Python - don't have much experience at all with language but learnt how to write a simple script with it
3. Md- this is my first time writing/using markdown
4. Csv - learnt how to create csv files
5. Using clean input validation when adding arguments to the parser
- cron jobs:

## Nicoles learnings
1. to force a 404 return - go to an existing website then to a path that doesnt exist eg google.com/404
2. How to do strike through on md file
3. Specify utf-8 encoding to ensures python reads the file using the correct translation for the bytes inside the file. This ensures we get the actual characters we expect.
4. regular expressions - mentioned in comment
5. extend metod add elements from another list or iterable to an array (like i did iterating through a file)
6. A set is a collection of unique items which doesnt have duplicates, is unordered, is fast to check if an item exists. I used a set for the found urls to filter out duplicates to make sure each url is only checked once
7. ```response = requests.head(url, allow_redirects=True, timeout=5)``` 
A HEAD request is like a GET but it only asks for headers not full content (all thats neccesary to check status code). allowing redirects follows redirects in case page has moved to new location. Add a timeout to wait before giving up.
8. if method doesnt use class variables make it static and call it like ClassName.methodName
9. If you create a branch from main then merge something else into main, your brch doesnt automatically get those changes but if you do  git merge main that merges mains changes into your branch then creates commit so you need to push this commit to your repo
10. Different error codes and their meanings
11. Its important to check redirects because:
    - shortened links often redirect to final destination and when validating links its imoprtant to store final url
    - seo/content content audits (link may have permanantely moved and lots of redirects is bad for seo)
    - security because it could be redirecting to suspicious pages
12. ```parsed = urlparse(url.strip())``` strip() removes whitespace and urlparse() seperates it into url parts
13. the fragment is the part after the '#' in a url which points to a specific part of th page
14. ```urlunparse(stripped).rstrip('/')``` rebuild url after cleaning
15.  including style is recommended because:
    - It lets you control the tone, complexity, and format of the explanation (e.g., plain English, professional, technical, friendly).
    - It makes your prompt more flexible for different audiences or use cases.
    - You can easily change or experiment with how the LLM responds without rewriting your template.
