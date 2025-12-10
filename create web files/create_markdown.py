"""
create_markdown.py

Converts a JSON file of film info into individual Markdown files for each film, for use on a website.

Usage:
    python create_markdown.py input.json

Arguments:
    input.json: Path to the JSON file containing a list of film dicts.

Output:
    Writes one Markdown file per film to the 'markdown files' subdirectory.
"""

import os
import json
import argparse

def parse_args():
    """
    Parse command-line arguments for the input JSON file.
    Returns:
        argparse.Namespace: Parsed arguments with 'input_json' as a string.
    """
    parser = argparse.ArgumentParser(description="Convert film JSON to Markdown files.")
    parser.add_argument('input_json', help='Path to input JSON file')
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

def make_markdown_dir(base_dir):
    """
    Ensure the output directory exists.
    Args:
        base_dir (str): Base directory where 'markdown files' will be created.
    Returns:
        str: Path to the output directory.
    """
    out_dir = os.path.join(base_dir, 'markdown files')
    os.makedirs(out_dir, exist_ok=True)
    return out_dir

def film_to_markdown(film):
    """
    Convert a film dictionary to a Markdown string in the desired format.
    Args:
        film (dict): Film info.
    Returns:
        str: Markdown content.
    """
    title = film.get('Film_title', 'Untitled')
    genres = film.get('Genres', [])
    description = film.get('Description', '')
    year = film.get('Release_year', '')
    film_url = film.get('Film_URL', '')
    tmdb_poster_path = film.get('TMDB_poster_path', '')
    director = film.get('Director')
    runtime = film.get('Runtime')
    countries = film.get('Countries') or []
    # Strip whitespace from country names
    countries = [c.strip() for c in countries]
    original_language = film.get('Original_language')
    spoken_languages = film.get('Spoken_languages') or []
    average_rating = film.get('Average_rating')
    cast = film.get('Cast') or []
    
    # Format arrays with triple quotes for string elements
    def format_string_array(arr):
        quoted_items = [f'"""{item}"""' for item in arr]
        return '[' + ', '.join(quoted_items) + ']'
    
    # Build the extra section conditionally
    extra_lines = [
        f'film_url = """{film_url}"""',
        f'tmdb_poster_path = """{tmdb_poster_path}"""'
    ]
    
    if year:
        extra_lines.append(f'year = {year}')
    if director:
        extra_lines.append(f'director = """{director}"""')
    if runtime:
        extra_lines.append(f'runtime = {runtime}')
    if countries:
        extra_lines.append(f'countries = {format_string_array(countries)}')
    if original_language:
        extra_lines.append(f'original_language = """{original_language}"""')
    if spoken_languages:
        extra_lines.append(f'spoken_languages = {format_string_array(spoken_languages)}')
    if average_rating is not None:
        extra_lines.append(f'average_rating = {average_rating}')
    if cast:
        extra_lines.append(f'cast = {format_string_array(cast)}')
    
    extra_section = '\n'.join(extra_lines)
    
    md = f"""+++
title = \"\"\"{title}\"\"\"
template = \"xmas-movie-page.html\"
description = \"\"\"{description}\"\"\"

[taxonomies]
xmas_genres = {genres}

[extra]
{extra_section}
+++
"""
    return md

def save_markdown(md_content, out_dir, title):
    """
    Save the Markdown content to a file named after the film title.
    Args:
        md_content (str): Markdown content.
        out_dir (str): Output directory.
        title (str): Film title (used for filename).
    """
    # Make a safe filename with year
    safe_title = ''.join(c for c in title if c.isalnum() or c in (' ', '-', '_')).rstrip()
    safe_title = safe_title.replace(' ', '_').lower()
    # Add year to filename for uniqueness
    year = ''
    if hasattr(save_markdown, 'year') and save_markdown.year:
        year = str(save_markdown.year)
    if year:
        filename = f"{safe_title}_{year}.md"
    else:
        filename = f"{safe_title}.md"
    out_path = os.path.join(out_dir, filename)
    with open(out_path, 'w') as f:
        f.write(md_content)

def main():
    """
    Main function to convert JSON film data to Markdown files.
    """
    args = parse_args()
    input_path = args.input_json
    base_dir = os.path.dirname(os.path.abspath(__file__))
    out_dir = make_markdown_dir(base_dir)
    films = load_films(input_path)
    for film in films:
        md = film_to_markdown(film)
        title = film.get('Film_title', 'Untitled')
        year = film.get('Release_year', '')
        # Pass year to save_markdown via attribute (since signature is unchanged)
        save_markdown.year = year

        save_markdown(md, out_dir, title)
    print(f"Wrote {len(films)} markdown files to {out_dir}")

if __name__ == "__main__":
    main()
