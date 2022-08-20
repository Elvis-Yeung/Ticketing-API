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
        + "<p>Get one ticket : /get<idnum></p>"
        + "<p>List all tickets: /getall</p>"
        + "<p>Add/edit a ticket: /save</p>"
    )


@app.route("/getall", methods=["GET"])
def get_all_tickets():
    """
    Returns a JSON containing all tickets as JSONs.
    """
    with open("database.json", "r") as f:
        db: dict = json.load(f)
    return (db, 200)


@app.route("/save", methods=["POST"])
def save_ticket():
    """
    Give me a new/edited ticket(as JSON), I will add/change it to the database.
    JSON Format: {
        "idstr": "uuid",
        "title": "title",
        "description": "description",
        "repository": "repo link",
        "difficulty": "difficulty",
        "assignee": "assignee",
        "role": "role"
    }
    When making a new ticket, leave the "uuid" field as an empty string. 

    """

    body: dict = request.get_json()
    idstr = body["idstr"]
    status = "add"

    with open("database.json", "r") as f:
        db: dict = json.load(f)

    if idstr:
        if idstr in db:
            status = "updat"
        else:
            return (
                f"Ticket id {idstr} is not found in the database. Do you want to create a new ticket?",
                200,
            )
    else:
        idstr = str(uuid4())

    db.update(
        {
            idstr: {
                "contents": {
                    "title": body["title"],
                    "description": body["description"],
                    "repository": body["repo"],
                    "difficulty": body["difficulty"],
                    "assignee": body["assignee"],
                    "role": body["role"],
                },
                "last updated": str(datetime.now()),
            }
        }
    )
    with open("database.json", "w") as f:
        json.dump(db, f, indent=4)
    return (f"Ticket id {idstr} has been {status}ed.", 200)


@app.route("/get<idstr>", methods=["GET"])
def get_one(idstr):
    """
    Give me a uuid, I will return the corresponding ticket JSON.
    """
    with open("database.json", "r") as f:
        db: dict = json.load(f)
    ticket = db.get(idstr)

    return (ticket, 200) if ticket else ("Ticket not found", 200)
