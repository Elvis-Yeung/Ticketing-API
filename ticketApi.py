import csv
import uuid
from flask import Flask, request
from datetime import datetime
from uuid import uuid4
import csv

app = Flask(__name__)

@app.route('/<var>')
def make_text(var):
    with open('database.txt', 'a') as f:
        f.write(f'{var}\n')
    return ('', 204)

@app.route('/get', methods = ['GET', 'POST'])
def man_of_post():
    if request.method == 'GET':
        with open('database.txt', 'a') as f:
            f.write(f"{datetime.now()}, Got mail.\n")
        return ('Got mail', 200)
    elif request.method == 'POST':
        body = request.get_json()
        with open('database.txt', 'a') as f:
            f.write(f"{datetime.now()}, Got {body['name']}.\n")
        return (body['name'], 200)

@app.route('/get<uuid>', methods = ['GET'])
def get_data(uuid):
    if request.method != 'GET': return ('Wrong request method.', 400)
    with open('database.csv', newline='') as csvfile:
        databasereader = csv.DictReader(csvfile)
        for row in databasereader:
            if row.get('Identifier') == uuid:
                name = row.get('Name')
                return (f'Got {name}!', 200)
    return ('Name not found.', 404)

@app.route('/post<name>', methods = ['POST'])
def post_data(name):
    if request.method != 'POST': return ('Wrong request method.', 400)
    with open('database.csv', 'a', newline='') as csvfile:
        fieldnames = ['Identifier', 'Timestamp', 'Name']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writerow({'Identifier': uuid4(), 'Timestamp': f'{datetime.now()}', 'Name': f'{name}'})
    return (f'{name} successfully written!', 200)

@app.route("/")
def hello_world():
    return 'hello'