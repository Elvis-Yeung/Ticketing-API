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

if False:
    add_ticket({
    "id": uuid.uuid4(),
    "title": "Easiest task ever",
    "description": "Do stuff",
    "repository": "N/A",
    "skills": "N/A",
    "difficulty": "Dark Souls No Hit",
    "assignee": "idy",
    "roles": ["frontend", "backend"],
    "last_modified": datetime.datetime.fromisoformat("2022-08-23 10:04:09.104992"),
    "created_at": datetime.datetime.fromisoformat("2022-08-20 10:04:09.104992")
}
)

@get_conn_cursor
def get_ticket(cur, id: uuid.UUID) -> dict:
    cur.execute('SELECT * FROM tickets WHERE id = %s;', (id,))
    columns = [desc[0] for desc in cur.description]
    values = cur.fetchone()
    ticket = dict(zip(columns, values))

    cur.execute('''
        SELECT name 
        FROM roles
            INNER JOIN ticket_role 
            ON ticket_role.role_name = roles.name
        WHERE ticket_role.ticket_id = %s;''', (id,))
    roles = cur.fetchall()
    ticket['roles'] = [role[0] for role in roles]

    return ticket

@get_conn_cursor
def yeet_ticket(cur, id: uuid.UUID):
    cur.execute('DELETE FROM ticket_role WHERE ticket_id = %s;', (id,))
    cur.execute('DELETE FROM tickets WHERE id = %s;', (id,))


@get_conn_cursor
def add_role(cur, name: str, desc: str):
    cur.execute('INSERT INTO roles VALUES (%s, %s);', (name, desc))


def add_cur_roles():
    add_role('frontend', '')
    add_role('backend', '')


@get_conn_cursor
def test1(cur, name):
    cur.execute("INSERT INTO roles VALUES (%s, %s);", (name, 'it is a role'))

@get_conn_cursor
def test2(cur):
    cur.execute("""SELECT * FROM roles;""")
    print(cur.fetchall())


if __name__ == "__main__":
    ...
    # reset_db()