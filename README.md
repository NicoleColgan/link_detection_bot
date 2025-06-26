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
python link-detection-bot.py "documents"
```

## TODO:
### For next week
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
- merging changes (nicole)

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

## Oisins learning
1. used a gitignore for the first time to hide stuff from the version control
2. Python - don't have much experience at all with language but learnt how to write a simple script with it
3. Md- this is my first time writing/using markdown
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
