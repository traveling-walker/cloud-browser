import click
import sqlite3
from flask import current_app, g
from flask.cli import with_appcontext

def close_database(e = None):
    database = g.pop('database', None)

    if database is not None:
        database.close()

def get_database():
    if 'database' not in g:
        g.database = sqlite3.connect(
            current_app.config['DATABASE'],
            detect_types = sqlite3.PARSE_DECLTYPES
        )
        g.database.row_factory = sqlite3.Row

    return g.database

def init_app(app):
    app.teardown_appcontext(close_database)
    app.cli.add_command(init_database_command)

def init_database():
    database = get_database()

    with current_app.open_resource('database/schema.sql') as f:
        database.executescript(f.read().decode('utf8'))


@click.command('init-database')
@with_appcontext
def init_database_command():
    """Clear the existing data and create new tables."""
    init_database()
    click.echo('Initialized the database.')
