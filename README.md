# Project scope
This project is a personal learning initiaive designed to explore technologies we already use. Its a link detection tool that scans documents or wikis for broken or out-dated linked with potential for real world value in documentation help and developer experience.

The project aims to deepen out understanding of tools like Python CLI dev, React, Next.js, and LLMS while also exploring concepts like crawling, parsing, content comparison, similarity detection and ui design.

It's developed entirely as a personal project, without the use of any confidential data. While the focus is on upskilling and mentorshop, there may be potential for future commercial integration if the tool proves useful.

## details
1. Input sources: lets start with files??
2. Output: csv of broken links
3. Initially flag just 404s?
4. optional extras

## TODO:
### For next week
- find more broke links (Oisin)
- Create the base python script - just one main, init, whatever - base script with like fuck all in it that accepts command line arguments (Oisin)
- Update read me with your parts (oisin)
- ~~Create a directory of documents~~ (Nicole)
- Reading in all the documents and checking the urls on the current page are good or not and print to csvs (Nicole)

### Future
- spit broken links to csv (Oisin or nicole - not sure)
- Check not only if theyre 404s but if the link exists period

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
- Just realised we cant do the whoel recursive search yet if were using documents (unless we download a document fromn the url and repeat the process). This is more so viable if were using urls to search through pages.

## Oisins learning
- cron jobs:
- gitignore
- Writing mds and read mes

## Nicoles learnings
1. to force a 404 return - go to an existing website then to a path that doesnt exist eg google.com/404
2. How to do strike through on md file
3. Specify utf-8 encoding to ensures python reads the file using the correct translation for the bytes inside the file. This ensures we get the actual characters we expect.
4. regular expressions - mentioned in comment
5. extend metod add elements from another list or iterable to an array (like i did iterating through a file)

