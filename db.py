import psycopg2
from psycopg2 import sql, extras
import uuid
import datetime


extras.register_uuid()
TICKETSDB_TABLES = ['tickets', 'roles', 'ticket_role']


def get_connection_cursor(fn):
    def wrapper(*args, **kwargs):
        with psycopg2.connect(dbname='ticketing_system', user='postgres', password='1234') as conn:
            with conn.cursor() as cur:
                fn(cur, *args, **kwargs)
    return wrapper


@get_connection_cursor
def init_db(cur):
    # tickets table
    cur.execute('''
        CREATE TABLE IF NOT EXISTS tickets (
            id UUID,
                PRIMARY KEY (id), 
            title TEXT NOT NULL,
            description TEXT NOT NULL,
            repository_link TEXT,
            skills TEXT,
            difficulty TEXT,
            assignee_id TEXT,
            last_modified TIMESTAMP NOT NULL,
            created_at TIMESTAMP NOT NULL
        );
    ''')

    # roles table
    cur.execute('''
        CREATE TABLE IF NOT EXISTS roles (
            id SERIAL,
                PRIMARY KEY (id),
            name TEXT UNIQUE NOT NULL,
            description TEXT NOT NULL
        );
    ''')

    # tickets roles intermediate
    cur.execute('''
        CREATE TABLE IF NOT EXISTS ticket_role (
            id SERIAL,
                PRIMARY KEY (id),
            ticket_id UUID,
            role_id INT,
            CONSTRAINT fk_ticket
                FOREIGN KEY (ticket_id)
                    REFERENCES tickets(id),
            CONSTRAINT fk_role
                FOREIGN KEY (role_id)
                    REFERENCES roles(id)
        );
    ''')


@get_connection_cursor
def yeet_db(cur):
    for table in TICKETSDB_TABLES:
        cur.execute(sql.SQL('DROP TABLE IF EXISTS {} CASCADE;').format(sql.Identifier(table)))


def reset_db():
    yeet_db()
    init_db()


@get_connection_cursor
def add_ticket(cur, ticket: dict):
    roles = ticket.pop('roles')
    cur.execute('INSERT INTO tickets VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s);', tuple(ticket.values()))

    for role in roles:
        cur.execute("SELECT role_id FROM roles WHERE name = (%s);", (role,))
        role_id = cur.fetchone()
        cur.execute("""
            INSERT INTO ticket_role (ticket_id, role_id) VALUES (%s);""", (ticket['id'], *role_id))


@get_connection_cursor
def add_role(cur, name: str, desc: str):
    cur.execute('INSERT INTO roles (name, description) VALUES (%s, %s);', (name, desc))


@get_connection_cursor
def test1(cur, name):
    cur.execute("""INSERT INTO roles (name, description) VALUES (%s, %s);""", (name, 'bottom test'))

@get_connection_cursor
def test2(cur):
    cur.execute("""SELECT * FROM roles;""")
    print(cur.fetchone())
    print(cur.fetchone())


if __name__ == "__main__":
    ...
    # reset_db()