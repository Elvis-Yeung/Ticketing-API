from flask import Flask, request
from datetime import datetime
from uuid import uuid4
from csv import DictReader, DictWriter
import json

app = Flask(__name__)

@app.route('/')
def show_command_list():
    """
    Displays the list of commands as static html.
    """
    return ( '<p>Commands</p>' 
    + '<p>List all tickets: /getall</p>' 
    + '<p>Add a ticket: /edit</p>')

# something to get UUID from user, and return corresponding ticket
# 1. redirect to site which GETs a UUID (somehow)
# 2. get the ticket
# 2. go back to original site and use the ticket(?) 

@app.route('/getall', methods=['POST'])
def get_all_tickets():
    """
    Returns a JSON containing all tickets as JSONs.
    """
    try:   
        with open('database.json', 'r') as f:
            db: dict = json.load(f)
        return (db, 200)
    except Exception:
        return ('An error occurred😢.', 400)

@app.route('/edit', methods=['GET'])
def add_or_edit_ticket():
    """
    Give me a new/edited ticket(as JSON), I will add/change it to the database.
    """
    try:
        new_ticket = request.get_json()

        with open('database.json', 'r') as f:
            db: dict = json.load(f)
            db.update(new_ticket)

        with open('database.json', 'w') as f:
            json.dump(db, f, indent=4)

        return ('Database has been updated👍.', 200)
    except Exception:
        return ('An error occurred😢.', 400)






# @app.route('/<var>')
# def make_text(var):
#     with open('database.txt', 'a') as f:
#         f.write(f'{var}\n')
#     return ('', 204)

# @app.route('/get', methods = ['GET', 'POST'])
# def man_of_post():
#     if request.method == 'GET':
#         with open('database.txt', 'a') as f:
#             f.write(f"{datetime.now()}, Got mail.\n")
#         return ('Got mail', 200)
#     elif request.method == 'POST':
#         body = request.get_json()
#         with open('database.txt', 'a') as f:
#             f.write(f"{datetime.now()}, Got {body['name']}.\n")
#         return (body['name'], 200)

# @app.route('/get<uuid>', methods = ['GET'])
# def get_data(uuid):
#     if request.method != 'GET': return ('Wrong request method.', 400)
#     with open('database.csv', newline='') as csvfile:
#         databasereader = DictReader(csvfile)
#         for row in databasereader:
#             if row.get('Identifier') == uuid:
#                 name = row.get('Name')
#                 return (f'Got {name}!', 200)
#     return ('Name not found.', 404)

# @app.route('/post<name>', methods = ['POST'])
# def post_data(name):
#     if request.method != 'POST': return ('Wrong request method.', 400)
#     with open('database.csv', 'a', newline='') as csvfile:
#         fieldnames = ['Identifier', 'Timestamp', 'Name']
#         writer = DictWriter(csvfile, fieldnames=fieldnames)
#         writer.writerow({'Identifier': uuid4(), 'Timestamp': f'{datetime.now()}', 'Name': f'{name}'})
#     return (f'{name} successfully written!', 200)
