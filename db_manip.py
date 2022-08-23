import sqlite3


def init_db():
    create_table()


def create_table():
    with sqlite3.connect("TicketStorage.db") as con:
        con.cursor().execute(
            """
            CREATE TABLE IF NOT EXISTS tickets(
                UUID STRING PRIMARY KEY NOT NULL,
                TAGS STRING NOT NULL,
                CONTENTS STRING NOT NULL,
                LAST_MODIFIED STRING NOT NULL,
                CREATED_AT STRING NOT NULL
            );
        """
        )


def insert_entry(ticket: dict):
    with sqlite3.connect("TicketStorage.db") as con:
        con.cursor().execute(
            "INSERT INTO tickets VALUES (?, ?, ?, ?, ?);", tuple(ticket.values())
        )


def edit_entry(ticket: dict, uuid: str):
    with sqlite3.connect("TicketStorage.db") as con:
        for k, v in ticket.items():
            con.cursor().execute(
                f"""
                UPDATE tickets
                SET '{k}' = '{v}'
                WHERE uuid = '{uuid}';"""
            )


def get_entry(uuid: str) -> tuple:
    with sqlite3.connect("TicketStorage.db") as con:
        return (
            con.cursor()
            .execute("SELECT * FROM tickets WHERE uuid = ?;", (uuid,))
            .fetchone()
        )


def get_all_entries() -> list[tuple]:
    with sqlite3.connect("TicketStorage.db") as con:
        return con.cursor().execute("SELECT * FROM tickets").fetchall()
