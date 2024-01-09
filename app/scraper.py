"""
import requests
from bs4 import BeautifulSoup
import csv

def scrape_netflix_data(target_url):
    resp = requests.get(target_url)
    soup = BeautifulSoup(resp.text, 'html.parser')

    # (Your scraping logic here)

    # Example initialization of lists

    
    episode_titles = ["Episode 1", "Episode 2"]
    episode_descriptions = ["Description 1", "Description 2"]
    name = ["Show Name"]
    seasons = ["Season 1"]
    about = ["About the show"]
    genres = ["Genre1", "Genre2"]
    moods = ["Mood1", "Mood2"]
    cast = ["Actor1", "Actor2"]

    # Example writing data to a CSV file
    csv_file_path = "netflix_data.csv"
    with open(csv_file_path, 'w', newline='', encoding='utf-8') as csv_file:
        csv_writer = csv.writer(csv_file)

        # Writing the header
        header = ["Name", "Seasons", "About", "Episode Title", "Episode Description", "Genres", "Moods", "Cast"]
        csv_writer.writerow(header)

        # Writing the data
        for i in range(min(len(episode_titles), 10)):  # Displaying a maximum of 10 episodes
            data = [name[0], seasons[0], about[0], episode_titles[i], episode_descriptions[i], genres[0], moods[0], cast[i]]
            csv_writer.writerow(data)

    print(f"The data has been saved to the CSV file: {csv_file_path}")

    return csv_file_path
"""
"""
import requests
from bs4 import BeautifulSoup
import csv

def scrape_netflix_data(target_url):
    resp = requests.get(target_url)
    soup = BeautifulSoup(resp.text, 'html.parser')

    # Example data extraction (replace with actual scraping logic)
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

    # Writing data to a CSV file
    csv_file_path = "netflix_data.csv"
    with open(csv_file_path, 'w', newline='', encoding='utf-8') as csv_file:
        csv_writer = csv.writer(csv_file)

        # Writing the header
        header = ["Name", "Seasons", "About", "Episode Title", "Episode Description", "Genres", "Moods", "Cast"]
        csv_writer.writerow(header)

        # Writing the data
        for i in range(len(episode_titles)):
            data = [name, seasons, about, episode_titles[i], episode_descriptions[i], ", ".join(genres), ", ".join(moods), cast[i] if i < len(cast) else "Not available"]
            csv_writer.writerow(data)

    print(f"The data has been saved to the CSV file: {csv_file_path}")

    return csv_file_path

"""
# app/scraper.py
import requests
from bs4 import BeautifulSoup
import csv

def scrape_netflix_data(target_url):
    resp = requests.get(target_url)
    soup = BeautifulSoup(resp.text, 'html.parser')

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

    csv_file_path = "netflix_data.csv"
    with open(csv_file_path, 'w', newline='', encoding='utf-8') as csv_file:
        csv_writer = csv.writer(csv_file)
        header = ["Name", "Seasons", "About", "Episode Title", "Episode Description", "Genres", "Moods", "Cast"]
        csv_writer.writerow(header)

        for i in range(len(episode_titles)):
            data = [name, seasons, about, episode_titles[i], episode_descriptions[i], ", ".join(genres), ", ".join(moods), cast[i] if i < len(cast) else "Not available"]
            csv_writer.writerow(data)

    print(f"The data has been saved to the CSV file: {csv_file_path}")
    return csv_file_path




