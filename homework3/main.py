from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func
import csv
from datetime import datetime

# FLASK_ENV=development FLASK_APP=main flask run

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/test.db'
db = SQLAlchemy(app)


class Sales(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    Transaction_date = db.Column(db.DateTime, unique=False, nullable=False)
    Product = db.Column(db.String(80), unique=False, nullable=False)
    Price = db.Column(db.Float, unique=False, nullable=False)
    Payment_Type = db.Column(db.String(80), unique=False, nullable=False)


@app.route('/create_db/')
def create_db():
    db.create_all()
    with open('homework3sales.csv') as csv_file:
        data = csv.DictReader(csv_file, delimiter=';')
        for line in data:
            sales_line = Sales(Transaction_date=datetime.strptime(line['Transaction_date'], "%m/%d/%Y %H:%M"),
                               Product=line['Product'], Price=float(line['Price']), Payment_Type=line['Payment_Type'])
            db.session.add(sales_line)
        db.session.commit()
    return 'DB created'


@app.route('/summary/')
def summary():
    query = db.session.query(func.strftime("%d.%m.%Y", Sales.Transaction_date),
                             func.sum(Sales.Price)).group_by(func.strftime("%d.%m.%Y", Sales.Transaction_date))
    result = '<table border=1><tr><td>Date</td><td>Sum</td></tr>'
    for i in query.all():
        result += f'<tr><td>{i[0]}</td><td>{i[1]}</td></tr>'
    result += '</table>'
    return result


@app.route('/sales/')
def sales():
    args = {}
    params = {
        'product': 'Product',
        'payment_type': 'Payment_Type'
    }
    for i in request.args.keys():
        if i in params.keys():
            args[params[i]] = request.args[i]
    query = Sales.query.filter_by(**args)
    result = '<table border=1><tr><td>Transaction date</td><td>Product</td><td>Price</td><td>Payment type</td></tr>'
    for i in query.all():
        result += f'<tr><td>{str(i.Transaction_date)}</td><td>{i.Product}</td><td>{str(i.Price)}</td><td>{i.Payment_Type}</td></tr>'
    result += '</table>'
    return result
