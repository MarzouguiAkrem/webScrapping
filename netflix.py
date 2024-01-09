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
"""
import os
from werkzeug.utils import secure_filename
from flask import Flask, render_template, request, redirect, flash
import requests
from bs4 import BeautifulSoup
import csv

app = Flask(__name__)

# Définissez la configuration avant de l'utiliser dans le reste du code
app.config['UPLOAD_FOLDER'] = '/home/akrem/Téléchargements/scra-web-main/netflixurl.txt'
app.secret_key = 'votre_clé_secrète'

def scrape_and_display_data(target_url):
    resp = requests.get(target_url)
    soup = BeautifulSoup(resp.text, 'html.parser')

    # Exemple d'extraction de données (remplacez par votre logique de scraping réelle)
    name = soup.find("h1", {"class": "title-title"}).text if soup.find("h1", {"class": "title-title"}) else "Not available"
    seasons = soup.find("span", {"class": "duration"}).text if soup.find("span", {"class": "duration"}) else "Not available"
    about = soup.find("div", {"class": "hook-text"}).text if soup.find("div", {"class": "hook-text"}) else "Not available"

    episodes = soup.find("ol", {"class": "episodes-container"}).find_all("li")
    episode_titles = [episode.find("h3", {"class": "episode-title"}).text for episode in episodes]
    episode_descriptions = [episode.find("p", {"class": "episode-synopsis"}).text if episode.find("p", {"class": "episode-synopsis"}) else "Not available" for episode in episodes]

    genres_elements = soup.find_all("span", {"class": "item-genres"})
    genres = [genre.text.replace(",", "") for genre in genres_elements]

    moods_elements = soup.find_all("span", {"class": "item-mood-tag"})
    moods = [mood.text.replace(",", "") for mood in moods_elements]

    cast_elements = soup.find_all("span", {"class": "item-cast"})
    cast = [actor.text for actor in cast_elements]

    # Écriture des données dans un fichier CSV
    csv_file_path = "netflix_data.csv"
    with open(csv_file_path, 'a', newline='', encoding='utf-8') as csv_file:
        csv_writer = csv.writer(csv_file)

        # Écriture des données
        for i in range(len(episode_titles)):
            data = [name, seasons, about, episode_titles[i], episode_descriptions[i], ", ".join(genres), ", ".join(moods), cast[i] if i < len(cast) else "Not available"]
            csv_writer.writerow(data)

    print(f"Les données ont été ajoutées au fichier CSV : {csv_file_path}")

    return csv_file_path

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # Vérifie si le champ 'urls_file' est dans la requête
        if 'urls_file' not in request.files:
            flash('Aucun fichier sélectionné')
            return redirect(request.url)

        urls_file = request.files['urls_file']

        # Vérifie si l'utilisateur a soumis un fichier
        if urls_file.filename == '':
            flash('Aucun fichier sélectionné')
            return redirect(request.url)

        # Vérifie si le fichier est un fichier texte (.txt)
        if urls_file and urls_file.filename.endswith('.txt'):
            # Utilisez secure_filename pour éviter des problèmes de sécurité
            filename = secure_filename(urls_file.filename)
            # Enregistrez le fichier dans un dossier temporaire (ou un dossier de votre choix)
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            urls_file.save(file_path)

            return scrape_and_display_data(file_path)

    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
