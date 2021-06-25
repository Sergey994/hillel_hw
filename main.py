from flask import Flask, request
from faker import Faker
import requests
import csv

app = Flask(__name__)


# FLASK_ENV=development FLASK_APP=main flask run


# Index page with links
@app.route('/')
def index():
    return """<a href='/generate_users/'>Generate users</a><br>
            <a href='/space/'>How many people are in space now</a><br>
            <a href='/mean/'>Average weight and height</a><br>
            <a href='/requirements/'>Requirements.txt</a>"""


# Generate users (100 in default)
@app.route('/generate_users/')
@app.route('/generate_users/<qty>/')
def generate_users(qty=100):
    if int(qty) < 0:
        return "Wrong input<br><a href='/'>Back</a>"
    users = ''
    fake = Faker()
    for i in range(int(qty)):
        users += fake.first_name() + ' ' + fake.email() + '<br>'
    users += "<a href='/'>Back</a>"
    return users


# How many people are in space now
@app.route('/space/')
def space():
    return f"People in space: {requests.get('http://api.open-notify.org/astros.json').json()['number']}<br><a " \
           f"href='/'>Back</a> "


# Calculating average weight an height in hw.csv
@app.route('/mean/')
def mean():
    with open('hw.csv') as csv_file:
        data = csv.DictReader(csv_file)
        weight = 0
        height = 0
        cnt = 0
        # Collecting data from file
        for line in data:
            weight += float(line['Weight(Pounds)'])
            height += float(line['Height(Inches)'])
            cnt += 1
    # Calculating average and converting from inches/pounds to cm/kg
    return f"Average weight: {round((weight / cnt) / 2.2046)}kg <br> Average height: {round((height / cnt) / 0.39370)}cm" \
           f"<br><a href=' /'>Back</a>"


# Reading requirements.txt
@app.route('/requirements/')
def requirements():
    res = ''
    with open('requirements.txt') as req:
        for line in req:
            res += line + '<br>'
    res += "<br><a href='/'>Back</a>"
    return res
