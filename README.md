# Xmas movie discovery

## Background:

This is a Christmas movie discovery project. It builds a database (json actually) of Christmas movies, enriches this data, and creates markdown files for use in a zola static site.

## Set up

This project uses Python 3.12.12 in a virtualenv called `xmas-movie-discovery`.

Quick setup:
```sh
pyenv install 3.12.12
pyenv virtualenv 3.12.12 xmas-movie-discovery
pyenv local xmas-movie-discovery
```

Dependencies get installed separately in each directory through requirements.txt. Instructions are in the separate README files.

## Structure

This project consists of three parts:

1. letterboxd scraper
2. refinement scripts
3. markdown creation script

### Letterboxd scraping

Use letterboxd user lists to identify as many Christmas films as possible. The scraper is taken from another github repo but it needed some fixes and refinements. (see [letterboxd project readme](./letterboxd%20scraper/README.md))

### Refinements

Adding genres: letterboxd has a very limitied number of genres: *Action, Adventure, Animation, Comedy, Crime, Documentary, Drama, Family, Fantasy, History, Horror, Music, mystery, Romance, Science Fiction, Thriller, TV Movie, War, Western*.
The scripts allow adding other genres, like *Hallmark, Royal Christmas, LGBTQ, Christmas Carol* etc.

Adding image url: It is not possible to scrape movie poster urls from letterboxd, so there is a script to get these from TMDB.

Consolidate: a script to combine multiple json files into one

The different scripts are meant to be run in a certain order to finally produce one large json file containing every movie for the app.

### Markdown creation

This script takes in a json file created in the previous steps and creates a markdown file for each film in the json.

## Workflow

1. collect all lists (for a particular genre) with the letterboxd script.

   the output is a number of json files inside the [scraper outputs directory](./letterboxd%20scraper/scraper_outputs/). 

   `python -m listscraper -f ./source_lists.txt -ofe json` 

2. use the [consolidate_json_lists script](./refinement%20scripts/consolidate_json_lists.py) to combine all those films into one large file (removing duplicates). 

   Output is saved as **combined.json** inside the [outputs directory](./refinement%20scripts/outputs/).

   `python consolidate_json_lists.py input-directory` 

3. if desired, use the [add_genre](./refinement%20scripts/add_genre.py) script to add the appropriate genre/genres to the films in the resulting **combined.json** file. 

   The script will overwrite combined.json with a new json file based on the genre(s) that was/were added, eg hallmark.json.

   `python add_genre.py new-genre "multiple word genre"`

7. Run the add_poster script on the json file to add an image path to each film entry. This will save a file **final.json**

   `python add_poster.py <input_json_file>`

8. Recommended: Before moving on to create markdown files, it is highly recommended to scrape all the films that should be in there first. The combining script removes duplicates. If films are added later to an existing directory, you may accidentally overwrtie existing entries with their own distinct genre additions.

   Keep a copy of the last used big combined json file. Whenever you run the scraper again, ensure to combine it witht he previous json file so not lose any data previously generated.

   example: the film Carol gets downloaded in a new scraper run but it has previoulsy been added to the database with the additon of the "queer" genre. if the new scraped content gets properly combined with the old one by use of the consolidation script, then the previoulsy added genre will be preserved (along with any new ones).

9. run the [create markdown script](./create%20web%20files/create_markdown.py) to create md files for all the films in that json.

