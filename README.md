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
- Research technologies and look through common pages to find broken links to ensure project is useful
- Create README with project outline
- Create the base python script
- Create a directory of documents
- Reading in all the documents and checking the urls on the current page are good or not
- Update code to accept user input of document & input validation of directories 
- Add ability to check different file types
- Print output to csv
- Document other things we should check about links 
- Retrying once if url fails
- Reasearch the other things we should be checking in the url to validate its usability:
    - status code: code returned by browser to indicate if the page is ok
    - cookies: Sometimes sites block bots or require cookies.
    - response reason: reason as to why the response is apparently ok or not
    - content/text: For error pages, a snippet of the response body might help the LLM explain custom errors.
    - ok: Boolean indicating if the response was successful (status code 200–399).
    - request method: The HTTP method used (GET, HEAD, etc.).
    - Response url: final url it lands on. Might contain useful info
    - Redirect chain: list of urls it goes through to get to the final url. May contain useful info like keywords. Also a lot of redirects ight be considered suspicous.
- Clean url
- Document if urls are reachable
- Integrate Langchain into project
- For each url, extract the useful info to a response object
- Check the text response for suspicious key words
- Use a Langchain prompt template to create a prompt for the llm
- Prompt asks the llm if a link is usable given the response info
- Use Langchain format instructions to ensure the llm produces the desired format and we can parse it
- Format instructions asks LLM to output True or False to whether or not the link is usable, then explain why, and provide resolutions steps if neccesary


### Future
- add progress bar when printing to csv & checking urls - or print checking url...?
- spit broken links to csv (Oisin or nicole - not sure)
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
- could consider crawling with dept limit
- ui to upload files/ urls?
- spit into a db instead of csv???
- build a simple ui (node.js??/ streamlit/ flask) to demo feature 
- add requrements block which installs required packages

### AI
#### todo:
- fix for null responses
- get ai to do the link extractioln then calling then explanation as a chain - could also ask it for red flag words
- could use chunking for redflag keyword thing to ensure overlap
- optimise chunk size for red flag
- add new redirect logic
- could lowk use ai to extract links too (chain1) ???? then chain it to call the url (chain2) then output the response then do the response summariser (chain3)!!!!!!!!!
- integrate diff llms & fallback llm
- retry logic & fallback llm
- FAISS / Chroma for document embedding + retrieval.
- Document it! Show architecture diagrams and example queries in README.


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
15. https://google.com redirects to https://www.google.com
16. redirect history will be empty if theres no redirects
17. Including style is recommended because:
    - It lets you control the tone, complexity, and format of the explanation (e.g., plain English, professional, technical, friendly).
    - It makes your prompt more flexible for different audiences or use cases.
    - You can easily change or experiment with how the LLM responds without rewriting your template.
16. Using langchain llm wrappers, prompt template, format instructions, parsing, memory, chains
