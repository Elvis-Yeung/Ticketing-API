from flask import Flask, request
from datetime import datetime
from uuid import uuid4
import json

app = Flask(__name__)

@app.route("/")
def show_command_list():
    """
    Displays the list of commands as static html.
    """
    return (
        "<p>Commands</p>"
        + "<p>List all tickets: /getall</p>"
        + "<p>Add/edit a ticket: /save</p>"
        + "<p>Get one ticket : /get<idnum></p>"
    )


@app.route("/getall", methods=["GET"])
def get_all_tickets():
    """
    Returns a JSON containing all tickets as JSONs.
    """
    if request.method != "GET":
        return ("Wrong request method, try POST.", 400)
    try:
        with open("database.json", "r") as f:
            db: dict = json.load(f)
        return (db, 200)
    except Exception:
        return ("An error occurred😢.", 400)


@app.route("/save", methods=["POST"])
def save_ticket():
    """
    Give me a new/edited ticket(as JSON), I will add/change it to the database.
    """
    if request.method != "POST":
        return ("Wrong request method, try POST.", 400)

    body: dict = request.get_json()
    idstr = tuple(body.keys())[0]

    with open("database.json", "r") as f:
        db: dict = json.load(f)

    if idstr in db:
        db.update(body)
        with open("database.json", "w") as f:
            json.dump(db, f, indent=4)
        return (f'Ticket updated, ticket id {idstr}', 200)
    else:
        idstr = str(uuid4())
        db.update(
            {
                idstr: {
                    "contents": {
                        "title": body["title"],
                        "description": body["description"],
                        "repo": body["repo"],
                        "difficulty": body["difficulty"],
                        "assignee": body["assignee"],
                        "role": body["role"]
                    },
                    "time": str(datetime.now())
                }
            }
        )
        with open("database.json", "w") as f:
            json.dump(db, f, indent=4)
        return (f'New ticket added, ticket id {idstr}.', 200)
        


@app.route("/get<idnum>", methods=["GET"])
def get_one(idstr):
    with open("database.json", "r") as f:
        db: dict = json.load(f)
    ticket = db.get(idstr)
    if ticket:
        return (ticket, 200)
    else:
        return ('Ticket not found', 200)
