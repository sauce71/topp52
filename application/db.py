import sqlite3

import click
from flask import current_app
from flask import g
from flask.cli import with_appcontext
from random import choice, randint
from datetime import date, timedelta


def get_db():
    """Connect to the application's configured database. The connection
    is unique for each request and will be reused if this is called
    again.
    """
    if "db" not in g:
        g.db = sqlite3.connect(
            current_app.config["DATABASE"], detect_types=sqlite3.PARSE_DECLTYPES
        )
        g.db.row_factory = sqlite3.Row
    return g.db


def close_db(e=None):
    """If this request connected to the database, close the
    connection.
    """
    db = g.pop("db", None)

    if db is not None:
        db.close()


def init_db():
    """Clear existing data and create new tables."""
    db = get_db()

    with current_app.open_resource("schema.sql") as f:
        db.executescript(f.read().decode("utf8"))


def get_user(user_id):
    q = "select * from users where id = ?"
    db = get_db()
    return db.execute(q, (user_id,)).fetchone()

def get_user_tours(user_id, date_from, date_to):
    q = """
    select id, tour_date
    from tours
    WHERE
    user_id = 2
    AND
    tour_date >= '2021-01-01'
    AND
    tour_date <= '2021-12-31'
    order by tour_date
    """
    db = get_db()
    return db.execute(q).fetchall()
    

def get_user_tours_count(user_id, year):
    q = """
    select count(*) count_tours
    FROM
    tours
    WHERE
    user_id = ?
    AND
    tour_date >= ?
    AND
    tour_date <= ?
    """
    df = date(year, 1, 1)
    dt = date(year, 12, 31)
    db = get_db()
    return db.execute(q, (user_id, df, dt)).fetchone()
    fetchone()


def get_users_top(date_from, date_to):
    q = """
    select t.user_id, u.username, count(*) count_tours
    from tours t
    join users u on u.id = t.user_id
    WHERE
    t.tour_date >= '2021-01-01' and t.tour_date <= '2021-12-31'
    group by t.user_id
    order by count(*) DESC
    limit 50
    """
    db = get_db()
    db.execute(q)
    return db.fetchall()

def get_tours_latest():
    q = """
    select t.*, u.username 
    from tours t
    join users u on u.id = t.user_id
    WHERE
    u.visible = TRUE
    order by t.tour_date desc, t.created desc
    limit 10
    """
    db = get_db()
    db.execute(q)
    return db.fetchall()

def get_tours_count(year):
    q = """
    select count(*) count_tours
    FROM
    tours
    WHERE
    tour_date >= '2021-01-01'
    AND
    tour_date <= '2021-12-1'
    """
    db = get_db()
    db.execute(q)
    return db.fetchall()




@click.command("init-db")
@with_appcontext
def init_db_command():
    """Clear existing data and create new tables."""
    init_db()
    click.echo("Initialized the database.")

def populate_db():
    db = get_db()
    insert_users = """
    DELETE FROM users;
    INSERT INTO users (username, email, password) VALUES ('Vetle', 'vetle@vealos.no', '');
    INSERT INTO users (username, email, password) VALUES ('Mikael', 'mikael@vealos.no', '');
    INSERT INTO users (username, email, password) VALUES ('Andreas', 'andreas@vealos.no', '');
    INSERT INTO users (username, email, password) VALUES ('Noah', 'noah@vealos.no', '');
    INSERT INTO users (username, email, password) VALUES ('Tobias', 'tobias@vealos.no', '');
    INSERT INTO users (username, email, password) VALUES ('August', 'august@vealos.no', '');
    INSERT INTO users (username, email, password) VALUES ('Tom', 'tom@vealos.no', '');    
    """
    db.executescript(insert_users)
    users = db.execute('SELECT id FROM users').fetchall()
    userlist = []
    for user in users:
        userlist.append(user['id'])
    
    db.execute('DELETE FROM tours')
    for i in range(100):
        user_id = choice(userlist)
        td = timedelta(days=randint(0, 60))
        tour_date = date.today() - td
        # Se video om SQL injection
        db.execute("INSERT INTO tours (user_id, tour_date) VALUES (?, ?)", (user_id, tour_date,))

    db.commit()
    print(userlist)


@click.command("populate-db")
@with_appcontext
def populate_db_command():
    """Clear existing data and fill with new data."""
    populate_db()
    click.echo("Created dummy data.")


def init_app(app):
    """Register database functions with the Flask app. This is called by
    the application factory.
    """
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)
    app.cli.add_command(populate_db_command)
