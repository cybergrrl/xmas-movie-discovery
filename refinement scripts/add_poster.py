"""
This script adds or updates the TMDB poster path for each movie in a JSON file.
It fetches poster paths from The Movie Database (TMDB) API using the movie's TMDB ID.
The script expects a TMDB API key to be set in the environment variable 'TMDB_API_KEY'.
Usage: python add_poster.py <input_json_file>
"""
import os
from dotenv import load_dotenv
import json
import requests
import sys

load_dotenv()
api_key = os.getenv('TMDB_API_KEY')

def get_poster_path(movie_id, api_key, tmdb_type='movie'):
    """
    Fetch the poster path for a movie/TV show from TMDB using its ID.
    Args:
        movie_id (str or int): The TMDB movie/TV ID.
        api_key (str): The TMDB API key (Bearer token).
        tmdb_type (str): Either 'movie' or 'tv' (default: 'movie').
    Returns:
        str or None: The poster path if found, otherwise None.
    """
    # Try the specified type first
    url = f"https://api.themoviedb.org/3/{tmdb_type}/{movie_id}"
    headers = {"Authorization": f"Bearer {api_key}"}
    response = requests.get(url, headers=headers)
    
    # If it fails with 404, try the opposite type
    if response.status_code == 404:
        alternate_type = 'tv' if tmdb_type == 'movie' else 'movie'
        print(f"  INFO: /{tmdb_type}/ endpoint failed, trying /{alternate_type}/")
        url = f"https://api.themoviedb.org/3/{alternate_type}/{movie_id}"
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            tmdb_type = alternate_type
    
    # Log failed API calls
    if response.status_code != 200:
        print(f"  ERROR: API call failed for ID {movie_id} (tried both /movie/ and /tv/)")
        print(f"  Status code: {response.status_code}")
        print(f"  Response: {response.text}")
        return None
    
    data = response.json()
    poster_path = data.get("poster_path")
    
    # Log when poster_path is None despite successful API call
    if poster_path is None:
        print(f"  WARNING: No poster_path found for {tmdb_type} ID {movie_id}")
        print(f"  Title in response: {data.get('title') or data.get('name', 'N/A')}")
        print(f"  Status: {data.get('status', 'N/A')}")
        if 'success' in data and not data['success']:
            print(f"  Error message: {data.get('status_message', 'N/A')}")
    else:
        if tmdb_type != 'movie':
            print(f"  SUCCESS: Found poster using /{tmdb_type}/ endpoint")
    
    return poster_path

def main(input_filename):
    """
    Read a JSON file of movies, fetch poster paths from TMDB, and update the file.
    Args:
        input_filename (str): Path to the input JSON file containing movie data.
    The function updates each movie dict with a 'TMDB_poster_path' key.
    """
    with open(input_filename, "r", encoding="utf-8") as f:
        movies = json.load(f)

    for movie in movies:
        tmdb_id = movie.get("TMDB_ID")  
        existing_poster = movie.get("TMDB_poster_path")
        tmdb_type = movie.get("TMDB_type", "movie")  # Default to 'movie' if not specified
        
        # Only fetch poster if it's not already set or is None
        if existing_poster is None or existing_poster == "":
            print(f"Processing {tmdb_type} ID: {tmdb_id} - missing poster")
            if tmdb_id:
                poster_path = get_poster_path(tmdb_id, api_key, tmdb_type)
                print(f"Poster path for {tmdb_type} ID {tmdb_id}: {poster_path}")
                movie["TMDB_poster_path"] = poster_path
                print(f"Updated movie: {movie.get('Film_title', 'Unknown Title')} with poster path: {poster_path}")
        # else:
        #     print(f"Skipping movie ID: {tmdb_id} - poster already exists: {existing_poster}")

    # Create new output filename with 'posterpath' in the name
    if input_filename.lower().endswith('.json'):
        output_filename = input_filename[:-5] + '_posterpath.json'
    else:
        output_filename = input_filename + '_posterpath.json'

    with open(output_filename, "w", encoding="utf-8") as f:
        json.dump(movies, f, indent=2, ensure_ascii=False)
    print(f"Poster paths updated successfully. Results written to: {output_filename}")

if __name__ == "__main__":
    """
    Entry point for the script. Expects the input JSON filename as a command-line argument.
    """
    main(sys.argv[1])