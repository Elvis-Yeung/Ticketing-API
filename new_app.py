from flask import Flask, request
from model import Ticket
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
        + "<p>List all tickets in order: /getall/ordered</p>"
        + "<p>Get specific ticket: /get<uuid></p>"
        + "<p>Add a ticket: /add</p>"
        + "<p>Edit a ticket: /edit<uuid></p>"
    )


@app.route("/getall", methods=["GET"])
def get_all_tickets():
    """
    Returns a JSON containing all tickets as JSONs.
    """
    with open("database.json", "r") as f:
        db: dict = json.load(f)
    return (db, 200)


@app.route("/getall/ordered", methods=["GET"])
def get_all_tickets_ordered():
    """
    Returns a JSON containing all tickets as JSONs, but in order.
    """
    with open("database.json", "r") as f:
        db: dict = json.load(f)
    # Sort tickets by time of creation, oldest first
    sorted_db: list = sorted(db.items(), key=lambda kv: kv[1]["time_of_creation"])
    print(sorted_db)
    return (sorted_db, 200)


@app.route("/get<uuid>", methods=["GET"])
def get_one(idstr):
    """
    Returns the ticket JSON that corresponds to the UUID.
    """
    with open("database.json", "r") as f:
        db: dict = json.load(f)
    ticket: dict | None = db.get(idstr)

    return (ticket, 200) if ticket else ("Ticket not found", 200)


@app.route("/add", methods=["POST"])
def add_ticket():
    """
    Adds a ticket entry to the database.
    """
    body: dict = request.get_json()
    idstr = str(uuid4())
    new_ticket = Ticket(id=idstr, **body[""]).as_json()
    _update_database(new_ticket)

    return ("Ticket successfully added.", 200)


@app.route("/edit", methods=["POST"])
def edit_ticket():
    """
    Edits a ticket entry in the database.
    """
    body: dict = request.get_json()
    idstr: str = tuple(body.keys())[0]

    with open("database.json", "r") as f:
        db: dict = json.load(f)

    if db.get(idstr):
        new_ticket = Ticket(id=idstr, **body[idstr]).as_json()
        _update_database(new_ticket)

        return (f"Ticket id {idstr} successfully updated.", 200)
    else:
        return (f"Ticket id {idstr} was not found. Did you input the right UUID?", 404)


def _update_database(ticket: type[Ticket]):
    """
    (Internal) Update the database with a new ticket entry."""
    with open("database.json", "r") as f:
        db: dict = json.load(f)
    db.update(ticket)

    with open("database.json", "w") as f:
        json.dump(db, f, indent=4)
