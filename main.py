from flask import Flask, request
from faker import Faker
import requests
import csv

app = Flask(__name__)


# FLASK_ENV=development FLASK_APP=main flask run


@app.route('/')
def index():
    return """<a href='/generate_users/'>users</a>
            <a href='/space/'>space</a>"""


@app.route('/generate_users/')
@app.route('/generate_users/<qty>/')
def generate_users(qty=100):
    if int(qty) < 0:
        return
    users = ''
    fake = Faker()
    for i in range(int(qty)):
        users += fake.first_name() + ' ' + fake.email() + '<br>'
    return users


@app.route('/space/')
def space():
    return f"People in space: {requests.get('http://api.open-notify.org/astros.json').json()['number']}"


@app.route('/mean/')
def mean():
    with open('hw.csv') as csv_file:
        data = csv.DictReader(csv_file)
        weight = 0
        height = 0
        cnt = 0
        for line in data:
            weight += float(line['Weight(Pounds)'])
            height += float(line['Height(Inches)'])
            cnt += 1
    return f'Average weight: {round((weight / cnt) / 2.2046)}kg <br> Average height: {round((height / cnt) / 0.39370)}cm'


@app.route('/requirements/')
def requirements():
    res = ''
    with open('requirements.txt') as req:
        for line in req:
            res += line + '<br>'
    return res
