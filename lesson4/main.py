from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/test.db'
db = SQLAlchemy(app)


class Customers(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    FirstName = db.Column(db.String(80), unique=False, nullable=False)
    LastName = db.Column(db.String(80), unique=False, nullable=False)
    Email = db.Column(db.String(80), unique=False, nullable=False)


@app.route('/names/')
def names():
    query = db.session.query(Customers.FirstName.distinct().label('firstname'))
    return str(len([row.firstname for row in query.all()]))