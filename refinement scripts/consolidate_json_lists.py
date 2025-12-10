"""
consolidate_json_lists.py

Combines and deduplicates film entries from multiple JSON files in a specified directory.

Usage:
    python consolidate_json_lists.py <input_dir> [output_file]

Arguments:
    input_dir: Directory containing input JSON files to consolidate.
    output_file: (Optional) Name of the output JSON file (default: combined.json). Cannot be 'combined' (without .json).

The script merges all JSON files, deduplicates by 'Film_URL', and merges genres for each film.
The result is saved as 'combined.json' (or your chosen name) in the 'outputs' subdirectory.
"""

import os
import json
import argparse
import sys


def load_json_files(input_dir):
    """
    Load and combine all JSON files from the input directory.
    Returns a list of all film entries.
    """
    all_files = []
    for filename in os.listdir(input_dir):
        if filename.endswith('.json'):
            filepath = os.path.join(input_dir, filename)
            with open(filepath) as f:
                data = json.load(f)
                if isinstance(data, list):
                    all_files.extend(data)
                else:
                    all_files.append(data)
    return all_files

# Get the directory where the script lives
def deduplicate_films(all_files):
    """
    Deduplicate film entries by 'Film_URL' and merge genres.
    Returns a dict of films keyed by URL.
    """
    films_by_url = {}
    for entry in all_files:
        film_url = entry.get('Film_URL')
        # Safely handle None for Genres
        genres = entry.get('Genres')
        if genres is None:
            genres = []
        if film_url not in films_by_url:
            entry_copy = entry.copy()
            entry_copy['Genres'] = set(genres)
            films_by_url[film_url] = entry_copy
        else:
            existing_genres = films_by_url[film_url]['Genres']
            new_genres = entry.get('Genres')
            if new_genres is None:
                new_genres = []
            existing_genres.update(new_genres)
    return films_by_url

def save_combined_films(films_by_url, script_dir, output_file, all_files):
    """
    Save the deduplicated films to the specified output file in the outputs directory.
    """
    output_dir = os.path.join(script_dir, 'outputs')
    os.makedirs(output_dir, exist_ok=True)
    output_path = os.path.join(output_dir, output_file)
    with open(output_path, 'w') as out:
        json.dump(list(films_by_url.values()), out, indent=2)
    print(f"Consolidated {len(all_files)} entries into {len(films_by_url)} unique entries. Saved to {output_path}")

if __name__ == "__main__":
    script_dir = os.path.dirname(os.path.abspath(__file__))
    parser = argparse.ArgumentParser(description="Consolidate JSON lists from a directory.")
    parser.add_argument(
        'input_dir',
        type=str,
        help='Directory containing input JSON files (required)'
    )
    parser.add_argument(
        'output_file',
        nargs='?',
        default='combined.json',
        help="Name of the output JSON file (default: combined.json). Cannot be 'combined' (without .json)."
    )
    args = parser.parse_args()
    input_dir = args.input_dir
    output_file = args.output_file

    print("Looking for input directory:", input_dir)
    if not os.path.exists(input_dir):
        print("Directory does not exist:", input_dir)
        exit(1)

    if output_file == 'combined':
        print("Error: Output file name cannot be 'combined'. Use another name or 'combined.json'.")
        exit(1)

    all_files = load_json_files(input_dir)
    films_by_url = deduplicate_films(all_files)
    for film in films_by_url.values():
        film['Genres'] = list(film['Genres'])
    save_combined_films(films_by_url, script_dir, output_file, all_files)