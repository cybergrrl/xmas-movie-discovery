
# Python Environment Setup

You should already be set up with a virtual environment as stated in the [project README](../README.md).

Install requirments for the refinements scripts from inside the "refinement scripts" directory:

```
pip install -r requirements.txt
```

## API Key Setup

The poster adding script requires a TMDB API key. 

1. Get your API key from [The Movie Database](https://www.themoviedb.org/settings/api)
2. Copy `.env.example` to `.env`:
   ```
   cp .env.example .env
   ```
3. Add your TMDB API key to the `.env` file:
   ```
   TMDB_API_KEY=your_actual_api_key_here
   ```

**Note:** The `.env` file is gitignored to keep your API key secure.

## How to

The different scripts are meant to be run in a certain order to interact with the letterboxd script. See the [project README](../README.md) for more information.


### 1. JSON consolidation script

##### Input:

Identify and input path to run this script. It will then take every json file inside that path and consolidate them into one json file.

Duplicates are ignored while genres are honoured: When the script finds a duplicate movie (based on the letterboxd url), it checks what genres are assigned to that movie and ensures that the final entry into the new json contains every genre that any of the duplicates had assigned to it.

##### Output: 

One new json file inside `./outputs` named `combined.json`

### 2. Genre adding script

The genre list of letterboxd is limited. I will want to add a number of genres to my app.

##### Input: 

This script will go through every json file iside `../letterboxd scraper/scraper_outputs` and add a genre to the genre list of each movie inside. 
It is therefore important to ensure that all the json files inside the target directory are meant to receive the genre I am adding in each run of the script.

It is possible to add multiple genres to this, eg: `python add_genre.py Lesbian Queer` will add two genres: lesbian and queer to all the films. If a genre contains multiple words, it has to be in quotation marks, eg `python add_genre.py "Royal Christmas"`.

##### Output:

A new JSON file which uses the added genre in its name.

### 3. Poster adding script

The letterboxd script is not able to scrape the movie poster for each film because it is being added to their pages dynamically. So I will have to grab any movie poster urls directly from The Movie Database using their API.

##### Input:

This script will grab every movie iside `./outputs/combined.json` and perform a call to TMDB API to grab the movie poster path. Then it will add that url to the movie's entry inside the json file.

##### Output:

The original input file will be replaced with the new version containing the poster paths.

#### Note for later: 
The path can be used to construct the poster url with added size parameters:

`https://image.tmdb.org/t/p/<SIZE>/<POSTER_PATH>`

According to gpt, for posters, TMDb supports: 
- *w92, w154, w185* (aka tiny, small, or medium thumbnail), 
- *w342, w500* (aka medium and large), 
- *w780* (even larger), and
- *original*

These mean maximum width in pixels.

Example image URL:
https://image.tmdb.org/t/p/w500/cJeled7EyPdur6TnCA5GYg0UVna.jpg
