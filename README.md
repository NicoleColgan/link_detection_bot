# Project scope
This project is a personal learning initiaive designed to explore technologies we already use. We are setting out to build a Link Validation & Dead Link Detection Bot: an intelligent system that automatically crawls a set of pages, checks for broken or outdated links, and stores a historical log of what has changed and when.

The project aims to deepen our understanding of tools like Python CLI dev, React, Next.js, and LLMS while also exploring concepts like crawling, parsing, content comparison, similarity detection and ui design. There is the added benefit of designing a project that meaningfully sharpens our technical skills, reinforces best practices, and creates something useful that we could also maintain and showcase independently.

This side-project is an opportunity to hone our skills across multiple areas of development, without the use of any confidential data. While the focus is on upskilling and mentorship, there may be potential for future commercial integration if the tool proves useful.

## details
1. Input sources: lets start with files??
2. Output: csv of broken links
3. Initially flag just 404s?
4. optional extras

## TODO:
### For next week
- find more broke links (Oisin)
- ~~Create the base python script - just one main, init, whatever~~ - base script with like fuck all in it that accepts command line arguments (Oisin)
- ~~Update read me with your parts~~ (oisin)
- ~~Create a directory of documents~~ (Nicole)
- Reading in all the documents and checking the urls recursively (Nicole)

### Future
- spit broken links to csv (Oisin or nicole - not sure)

## notes:
- It should periodically crawling page (recursively eg follow a docs links link...)
- Need to be able to easily plug in different websites/ docs or something somehow to make it a useful tool for a variety of purposes
- AI Use: Detect semantic change (e.g., if firmware has been renamed or replaced) not just broken URLs.
- We can use react/ next js to build a simple ui where you can insert a url to recursively check links
- The tool automatically checks whether urls on a page are:
    1. alive or dead
    2. Have changed signifigantly over time
    3. Flag suspicious or broken pages using intelligent comparison - slow responses
- how do we give it something to check?? i think the product page itself shouldnt have any broken links so maybe we do something similar like we did in the poc and download files or just give it a list of files or links (in the case of wiki, i guess it would be a url but it also could be for the file to be fair so maybe a list of urls in a csv or something). Probably easier to start with explicit imput eg a directory with files in it or wikis etc then add crawling functionality later

## Future work
- could consider crawling with dept limit
- Integreation with llms to summarise content, suggest fixes
- ui to upload files/ urls?
- What file formats to consider

## Oisins learning
1. used a gitignore for the first time to hide stuff from the version control
2. Python - don't have much experience at all with language but learnt how to write a simple script with it
3. Md- this is my first time writing/using markdown
- cron jobs:



## Nicoles learnings
1. to force a 404 return - go to an existing website then to a path that doesnt exist eg google.com/404
2. How to do strike through on md file

