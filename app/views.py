
from flask import render_template, request
import csv  # Add this line
from app import app
from .scraper import scrape_netflix_data

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        target_url = request.form['target_url']
        return scrape_and_display_data(target_url)
    return render_template('index.html')

def scrape_and_display_data(target_url):
    # Call your scraping function
    csv_file_path = scrape_netflix_data(target_url)

    # Reading data from the CSV file
    data = []
    with open(csv_file_path, 'r', encoding='utf-8') as csv_file:
        csv_reader = csv.reader(csv_file)
        header = next(csv_reader)  # Skip the header
        for row in csv_reader:
            data.append(row)

    return render_template('display_data.html', header=header, data=data)

