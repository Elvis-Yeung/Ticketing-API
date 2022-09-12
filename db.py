import psycopg2
from psycopg2 import sql, extras
import uuid
import datetime


extras.register_uuid()
TICKETSDB_TABLES = ['tickets', 'roles', 'ticket_role']


def get_conn_cursor(fn):
    def wrapper(*args, **kwargs):
        with psycopg2.connect(dbname='ticketing_system', user='postgres', password='1234') as conn:
            with conn.cursor() as cur:
                return fn(cur, *args, **kwargs)
    return wrapper


@get_conn_cursor
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
            name TEXT,
                PRIMARY KEY (name),
            description TEXT NOT NULL
        );
    ''')

    # tickets roles intermediate
    cur.execute('''
        CREATE TABLE IF NOT EXISTS ticket_role (
            ticket_id UUID,
            role_name TEXT,
            CONSTRAINT fk_ticket
                FOREIGN KEY (ticket_id)
                    REFERENCES tickets(id),
            CONSTRAINT fk_role
                FOREIGN KEY (role_name)
                    REFERENCES roles(name)
        );
    ''')


@get_conn_cursor
def yeet_db(cur):
    for table in TICKETSDB_TABLES:
        cur.execute(sql.SQL('DROP TABLE IF EXISTS {} CASCADE;').format(sql.Identifier(table)))


def reset_db():
    yeet_db()
    init_db()


@get_conn_cursor
def add_ticket(cur, ticket: dict):
    roles = ticket.pop('roles')
    cur.execute('INSERT INTO tickets VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s);', tuple(ticket.values()))

    for role in roles:
        cur.execute("INSERT INTO ticket_role VALUES (%s, %s);", (ticket['id'], role))


@get_conn_cursor
def get_ticket(cur, id: uuid.UUID) -> dict:
    cur.execute('SELECT * FROM tickets WHERE id = %s;', (id,))
    values = cur.fetchone()
    # explanation for desc[0] https://www.psycopg.org/docs/cursor.html?highlight=cursor#cursor
    columns = [desc[0] for desc in cur.description]
    ticket = dict(zip(columns, values))

    cur.execute('''
        SELECT name 
        FROM roles
            INNER JOIN ticket_role 
            ON ticket_role.role_name = roles.name
        WHERE ticket_role.ticket_id = %s;''', (id,))
    roles: list[tuple] = cur.fetchall()
    ticket['roles'] = [role[0] for role in roles]

    # let roles: Vec<String> = roles.iter().map(|role| role[0]).collect()
    return ticket


@get_conn_cursor
def yeet_ticket(cur, id: uuid.UUID):
    cur.execute('DELETE * FROM ticket_role WHERE ticket_id = %s;', (id,))
    cur.execute('DELETE * FROM tickets WHERE id = %s;', (id,))


@get_conn_cursor
def add_role(cur, name: str, desc: str):
    cur.execute('INSERT INTO roles VALUES (%s, %s);', (name, desc))


@get_conn_cursor
def yeet_role(cur, name: str):
    cur.execute('DELETE * FROM ticket_role WHERE role_name = %s;', (name))
    cur.execute('DELETE * FROM role WHERE name = %s;', (name))


def add_cur_roles():
    add_role('frontend', '')
    add_role('backend', '')



if __name__ == "__main__":
    ...
    # reset_db()