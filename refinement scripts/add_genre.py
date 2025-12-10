"""
add_genre.py

Adds one or more genres to every film entry in the combined.json file, saves the updated list to a new file using a filename based on the added genres, then deletes the original combined.json file.

Usage:
    python add_genre.py Hallmark "Royal Christmas"

Arguments:
    genres: One or more genres to add. Separate by space. Use quotes for multi-word genres.

"""

import os
import json
import argparse

def parse_args():
    """
    Parse command-line arguments for genres to add.
    Returns:
        argparse.Namespace: Parsed arguments with 'genres' as a list of strings.
    """
    parser = argparse.ArgumentParser(description="Add genres to each film in the JSON file.")
    parser.add_argument('genres', nargs='+', help='Genres to add (e.g. Lesbian "Holiday movie")')
    return parser.parse_args()

def load_films(input_path):
    """
    Load the list of films from the specified JSON file.
    Args:
        input_path (str): Path to the JSON file.
    Returns:
        list: List of film dictionaries.
    """
    with open(input_path) as f:
        return json.load(f)

def save_films(films, output_path):
    """
    Save the list of films to the specified JSON file.
    Args:
        films (list): List of film dictionaries.
        output_path (str): Path to the JSON file.
    """
    with open(output_path, 'w') as f:
        json.dump(films, f, indent=2)

def main():
    """
    Main function to add genres to each film entry in the combined JSON file.
    """
    script_dir = os.path.dirname(os.path.abspath(__file__))

    input_path = os.path.join(script_dir, 'outputs', 'combined.json')

    print("Looking for input file:", input_path)
    if not os.path.exists(input_path):
        print("File does not exist:", input_path)
        exit(1)

    args = parse_args()
    genre_list = args.genres
    all_films = load_films(input_path)

    for film in all_films:
        print(film["Film_title"] + ": " + str(film.get("Genres", [])))

        # Ensure 'Genres' key exists and is a list
        if "Genres" not in film or not isinstance(film["Genres"], list):
            film["Genres"] = []

        # Add new genres if not already present
        for genre in genre_list:
            if genre not in film["Genres"]:
                film["Genres"].append(genre)

        print(film["Film_title"] + ": " + str(film["Genres"]))

    # Build output filename from genres, joined by dashes, lowercased, no spaces
    safe_genres = [g.lower().replace(' ', '-') for g in genre_list]
    output_filename = f"{'-'.join(safe_genres)}.json"
    output_path = os.path.join(os.path.dirname(input_path), output_filename)
    print(f"Saving to: {output_path}")

    save_films(all_films, output_path)

    # Delete the original input file after saving the new one
    try:
        os.remove(input_path)
        print(f"Deleted original input file: {input_path}")
    except Exception as e:
        print(f"Warning: Could not delete original file: {e}")

if __name__ == "__main__":
    main()

