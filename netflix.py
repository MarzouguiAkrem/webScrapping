"""
import requests
from bs4 import BeautifulSoup
import csv
from flask import Flask, render_template
from io import StringIO

app = Flask(__name__)

target_url = "https://www.netflix.com/in/title/80057281"
resp = requests.get(target_url)

soup = BeautifulSoup(resp.text, 'html.parser')

# Initialization of lists for each characteristic
episode_titles = []
episode_descriptions = []
name = []
seasons = []
about = []
genres = []
moods = []
facebook = []
twitter = []
instagram = []
cast = []

# Extraction of data
try:
    name.append(soup.find("h1", {"class": "title-title"}).text)
except AttributeError:
    name.append("Not available")

try:
    seasons.append(soup.find("span", {"class": "duration"}).text)
except AttributeError:
    seasons.append("Not available")

try:
    about.append(soup.find("div", {"class": "hook-text"}).text)
except AttributeError:
    about.append("Not available")

episodes = soup.find("ol", {"class": "episodes-container"}).find_all("li")

for i in range(0, min(len(episodes), 10)):  # Displaying a maximum of 10 episodes
    episode_titles.append(episodes[i].find("h3", {"class": "episode-title"}).text)

    # Verification of the existence of the "p" element with the class "episode-synopsis"
    episode_description_element = episodes[i].find("p", {"class": "episode-synopsis"})
    episode_descriptions.append(episode_description_element.text if episode_description_element else "Not available")

genres_elements = soup.find_all("span", {"class": "item-genres"})
genres = [genre.text.replace(",", "") for genre in genres_elements]

moods_elements = soup.find_all("span", {"class": "item-mood-tag"})
moods = [mood.text.replace(",", "") for mood in moods_elements]

try:
    facebook.append(soup.find("a", {"data-uia": "social-link-facebook"}).get("href"))
except AttributeError:
    facebook.append("Not available")

try:
    twitter.append(soup.find("a", {"data-uia": "social-link-twitter"}).get("href"))
except AttributeError:
    twitter.append("Not available")

try:
    instagram.append(soup.find("a", {"data-uia": "social-link-instagram"}).get("href"))
except AttributeError:
    instagram.append("Not available")

# Extracting cast data
cast_elements = soup.find_all("span", {"class": "item-cast"})
cast = [actor.text for actor in cast_elements]

# Writing data to a CSV file
csv_file_path = "netflix_data.csv"
with open(csv_file_path, 'w', newline='', encoding='utf-8') as csv_file:
    csv_writer = csv.writer(csv_file)

    # Writing the header
    header = ["Name", "Seasons", "About", "Episode Title", "Episode Description", "Genres", "Moods", "Facebook", "Twitter", "Instagram", "Cast"]
    csv_writer.writerow(header)

    # Writing the data
    for i in range(min(len(episode_titles), 10)):  # Displaying a maximum of 10 episodes
        data = [name[0], seasons[0], about[0], episode_titles[i], episode_descriptions[i], genres[0], moods[0], facebook[0], twitter[0], instagram[0], cast[i]]
        csv_writer.writerow(data)

print(f"The data has been saved to the CSV file: {csv_file_path}")

@app.route('/')
def display_data():
    # Reading data from the CSV file
    data = []

    with open(csv_file_path, 'r', encoding='utf-8') as csv_file:
        csv_reader = csv.reader(csv_file)
        header = next(csv_reader)  # Skip the header
        for row in csv_reader:
            data.append(row)

    return render_template('display_data.html', header=header, data=data)

if __name__ == '__main__':
    app.run(debug=True)
"""
import requests
from bs4 import BeautifulSoup
import csv
from flask import Flask, render_template, request
from io import StringIO

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        target_url = request.form['target_url']
        return scrape_and_display_data(target_url)
    return render_template('index.html')

def scrape_and_display_data(target_url):
    resp = requests.get(target_url)
    soup = BeautifulSoup(resp.text, 'html.parser')

    # Initialization of lists for each characteristic
    episode_titles = []
    episode_descriptions = []
    name = []
    seasons = []
    about = []
    genres = []
    moods = []
    cast = []

    # Extraction of data
    try:
        name.append(soup.find("h1", {"class": "title-title"}).text)
    except AttributeError:
        name.append("Not available")

    try:
        seasons.append(soup.find("span", {"class": "duration"}).text)
    except AttributeError:
        seasons.append("Not available")

    try:
        about.append(soup.find("div", {"class": "hook-text"}).text)
    except AttributeError:
        about.append("Not available")

    episodes = soup.find("ol", {"class": "episodes-container"}).find_all("li")

    for i in range(0, min(len(episodes), 10)):  # Displaying a maximum of 10 episodes
        episode_titles.append(episodes[i].find("h3", {"class": "episode-title"}).text)

        # Verification of the existence of the "p" element with the class "episode-synopsis"
        episode_description_element = episodes[i].find("p", {"class": "episode-synopsis"})
        episode_descriptions.append(episode_description_element.text if episode_description_element else "Not available")

    genres_elements = soup.find_all("span", {"class": "item-genres"})
    genres = [genre.text.replace(",", "") for genre in genres_elements]

    moods_elements = soup.find_all("span", {"class": "item-mood-tag"})
    moods = [mood.text.replace(",", "") for mood in moods_elements]

    # Extracting cast data
    cast_elements = soup.find_all("span", {"class": "item-cast"})
    cast = [actor.text for actor in cast_elements]

    # Writing data to a CSV file
    csv_file_path = "netflix_data.csv"
    with open(csv_file_path, 'w', newline='', encoding='utf-8') as csv_file:
        csv_writer = csv.writer(csv_file)

        # Writing the header
        header = ["Name", "Seasons", "About", "Episode Title", "Episode Description", "Genres", "Moods", "Cast"]
        csv_writer.writerow(header)

        # Writing the data
        for i in range(min(len(episode_titles), 10)):  # Displaying a maximum of 10 episodes
            data = [name[0], seasons[0], about[0], episode_titles[i], episode_descriptions[i], genres[0], moods[0],cast[i]]
            csv_writer.writerow(data)

    print("The data has been saved to the CSV file: {}".format(csv_file_path))
    # Reading data from the CSV file
    data = []

    with open(csv_file_path, 'r', encoding='utf-8') as csv_file:
        csv_reader = csv.reader(csv_file)
        header = next(csv_reader)  # Skip the header
        for row in csv_reader:
            data.append(row)

    return render_template('display_data.html', header=header, data=data)

if __name__ == '__main__':
    app.run(debug=True)


from app import app

if __name__ == '__main__':
    app.run(debug=True)

