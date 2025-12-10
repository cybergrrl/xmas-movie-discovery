# Changes to the original scraper

## Fix script
To start with, the app was broken and did not download or store any films. To fix this, i downloaded changes to `scrape_functions.py` and `utility_functions.py` from another user: https://github.com/cjpeterson/Letterboxd-list-scraper/tree/master/listscraper

There are issues with this fix but i am ignoring them for now. Eg lists with just 1 film will be ignored. 

## include username in output files

I made a change to `checkimport_functions.py` to ensure that when there are multiple lists to scrape, the resulting files include the username for each list. This is because i will want to scrape themed lists (eg lesbian xmas movies or horror xmas movies) and it is likely that the lists have identical names. I want each output file to include the name of the user who made the list - thus making it unique.

This works only when i do not give an output file name. Otherwise that one will be used and the resulting files will have numbers appended to distinguish them from one another.

## get the TMDB ID

I made a change to scrape_functions to get the film ID for The Internet Database. It is added to the json output and enables me in a later step to make a call to the TMDB API to get the movie poster.

## Quick guide

- put list of lists into source_lists.txt
- run `python -m listscraper -f ./source_lists.txt -ofe json` to take in the list of lists and output as json
- this will create one json file per list inside ./scraper_outputs 



