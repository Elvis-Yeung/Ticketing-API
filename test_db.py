from db import *

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
def test1(cur, name):
    cur.execute("INSERT INTO roles VALUES (%s, %s);", (name, 'it is a role'))

@get_conn_cursor
def test2(cur):
    cur.execute("""SELECT * FROM roles;""")
    print(cur.fetchall())
