"""
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
"""

# app/views.py
from curses import flash
import os
from flask import redirect, render_template, request
from werkzeug.utils import secure_filename
import csv
from app import app
from .scraper import scrape_netflix_data
from app.scraper import scrape_netflix_data


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        urls_file = request.files['urls_file']

        if urls_file.filename == '':
            flash('Aucun fichier sélectionné')
            return redirect(request.url)

        if urls_file and urls_file.filename.endswith('.txt'):
            filename = secure_filename(urls_file.filename)
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            urls_file.save(file_path)

            return scrape_and_display_data_from_file(file_path)

    return render_template('index.html')

def scrape_and_display_data_from_file(urls_file_path):
    with open(urls_file_path, 'r') as file:
        urls = file.read().splitlines()

    for url in urls:
        scrape_netflix_data(url)

    data = []
    header = []

    with open("netflix_data.csv", 'r', encoding='utf-8') as csv_file:
        csv_reader = csv.reader(csv_file)
        header = next(csv_reader)
        for row in csv_reader:
            data.append(row)

    return render_template('display_data.html', header=header, data=data)
