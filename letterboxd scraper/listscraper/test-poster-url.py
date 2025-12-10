from bs4 import BeautifulSoup
import requests

# function to extract html document from given url
def getfilm(url):
    
    # request for HTML document of given url
    response = requests.get(url)
    
    # response will be provided in JSON format
    return response.text

film_url = "https://letterboxd.com/film/carol-2015/"

# create document
film_html = getfilm(film_url)

film_soup = BeautifulSoup(film_html, 'html.parser')

# Finding the film name
film_soup["Film_title"] = film_soup.find("div", {"class" : "col-17"}).find("h1").text
print(film_soup["Film_title"])


# Extract poster URL from the second element with class 'poster film-poster'
poster = film_soup.find_all('srcset')
for item in poster:
    print(item)

# try:
#     posters = film_soup.find_all('img', class_='poster film-poster')
#     if len(posters) >= 2:
#         poster_url = posters[1].get('src') or posters[1].get('data-src')
#     else:
#         poster_url = not_found
# except Exception:
#     poster_url = not_found
# film_dict["Poster_URL"] = poster_url

# print(film_soup.title)  