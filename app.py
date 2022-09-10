from flask import Flask, request
from datetime import datetime
from db_manip import *
from dataclasses import dataclass
import json


app = Flask(__name__)


init_db()


@app.route("/")
def show_endpoints_list():
    """
    Displays the list of endpoints(as static html).
    """

    return (
        "<p>Endpooints</p>"
        + "<p>List all tickets: /getall</p>"
        + "<p>List all tickets in order: /getall/ordered</p>"
        + "<p>Get specific ticket: /get<uuid></p>"
        + "<p>Add a ticket: /add</p>"
        + "<p>Edit a ticket: /edit<uuid></p>"
    )


@app.get("/getall")
def get_all_tickets():
    """
    Returns a list of all ticket entries.
    """

    # all_entries = []
    # for row in get_all_entries():
    #     entry = stringify_query(row)
    #     ticket = Ticket(*entry).as_json()
    #     all_entries.append(ticket)
    all_entries = [Ticket(*stringify_query(row)).as_json() for row in get_all_entries()]

    return all_entries



@app.get("/getall/ordered")
def get_all_tickets_ordered():
    """
    Returns a list of all ticket entries in order of time of creation.
    """

    entries = get_all_tickets()
    sorted_entries = sorted(
        entries, key=lambda entry: datetime.fromisoformat(entry["created_at"])
    )

    return sorted_entries


@app.get("/get<idstr>")
def get_one(idstr):
    """
    Returns the ticket entry with the provided UUID.
    """

    entry = get_entry(idstr)
    if not entry:
        return (f"Ticket ID {idstr} could not be found.", 404)

    ticket = stringify_query(entry)

    return Ticket(*ticket).as_json()


@app.post("/add")
def add_ticket():
    """
    Adds a ticket entry to the database.
    """

    body: dict = request.get_json()
    ticket = objectify_query(body)
    insert_entry(ticket)

    return "Ticket has been added."


@app.post("/edit<idstr>")
def edit_ticket(idstr: str):
    """
    Edits a ticket entry in the database.
    """

    body: dict = request.get_json()
    ticket = objectify_query(body)
    edit_entry(ticket, idstr)

    return f"Ticket ID {idstr} has been updated."


def objectify_query(ticket: dict) -> dict:
    """Serialize objects in the ticket to strings."""

    ticket = ticket.copy()
    ticket["tags"] = json.dumps(ticket["tags"])
    ticket["contents"] = json.dumps(ticket["contents"])

    return ticket


def stringify_query(query_row: tuple) -> tuple:
    """Deserialize strings in the query to objects."""

    query_row = list(query_row)
    query_row[1] = json.loads(query_row[1])
    query_row[2] = json.loads(query_row[2])

    return tuple(query_row)


@dataclass
class Ticket:
    id: str
    tags: list[str]
    contents: dict[str, str]
    last_modified: str
    created_at: str

    def as_json(self):
        return {
            "uuid": self.id,
            "tags": self.tags,
            "contents": self.contents,
            "last_modified": self.last_modified,
            "created_at": self.created_at,
        }