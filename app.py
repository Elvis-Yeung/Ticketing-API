from flask import Flask, request
from datetime import datetime
from uuid import uuid4
import json

app = Flask(__name__)

@app.route('/')
def show_command_list():
    """
    Displays the list of commands as static html.
    """
    return ('<p>Commands</p>' 
    + '<p>List all tickets: /getall</p>' 
    + '<p>Add/edit a ticket: /update</p>')

# something to get UUID from user, and return corresponding ticket
# 1. redirect to site which GETs a UUID (somehow)
# 2. get the ticket
# 2. go back to original site and use the ticket(?) 

# @app.get('/update')
# def get_uuid():
#     'ask user for uuid?'
#     return 'something idk'

# @app.post('/update')
# def post_ticket(id):
#     return db.get(id)

@app.route('/getall', methods=['POST'])
def get_all_tickets():
    """
    Returns a JSON containing all tickets as JSONs.
    """
    if request.method != 'POST':
        return ('Wrong request method, try POST.', 400)
    try:   
        with open('database.json', 'r') as f:
            db: dict = json.load(f)
        return (db, 200)
    except Exception:
        return ('An error occurred😢.', 400)

@app.route('/update', methods=['GET'])
# async \
def add_or_edit_ticket():
    """
    Give me a new/edited ticket(as JSON), I will add/change it to the database.
    """
    if request.method != 'GET':
        return ('Wrong request method, try GET.', 400)
    try:
        # id = await get_uuid()
        # await post_ticket(id)

        new_ticket: dict = request.get_json()
        new_ticket.update({"time": str(datetime.now())})

        with open('database.json', 'r') as f:
            db: dict = json.load(f)
            db.update(new_ticket)

        with open('database.json', 'w') as f:
            json.dump(db, f, indent=4)

        return ('Database has been updated👍.', 200)
    except Exception:
        return ('An error occurred😢.', 400)