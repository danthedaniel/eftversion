"""EFT Version Site."""

from flask import Flask, render_template, jsonify, g
import sqlite3
import os
from datetime import datetime

from .eft_api import API


app = Flask(__name__)
app.config.update(dict(
    DATABASE=os.path.join(app.root_path, 'eft.db'),
    DELAY=5 * 60  # API delay (5 minutes)
))


# ROUTES
@app.route("/")
def index():
    """Index route."""
    try:
        update_versions()
    except Exception as e:
        print("Error occured while updating version: {}".format(e))

    return render_template(
        "index.html",
        game_version=get_version("game_versions"),
        launcher_version=get_version("launcher_versions")
    )


@app.route("/versions.json")
def versions():
    """Version JSON route."""
    try:
        update_versions()
    except Exception as e:
        print("Error occured while updating version: {}".format(e))

    return jsonify({
        "client": get_version("game_versions"),
        "launcher": get_version("launcher_versions")
    })


# DATABASE
def connect_db():
    """Connect to the database as specified in the config."""
    rv = sqlite3.connect(
        app.config['DATABASE'],
        detect_types=sqlite3.PARSE_DECLTYPES
    )
    rv.row_factory = sqlite3.Row
    return rv


def get_db():
    """Open a new database connection if there is none yet for the context."""
    if not hasattr(g, 'sqlite_db'):
        g.sqlite_db = connect_db()
    return g.sqlite_db


def init_db():
    """Initialize the database."""
    db = get_db()
    cur = db.cursor()

    with app.open_resource('schema.sql', mode='r') as f:
        cur.executescript(f.read())

    epoch = datetime.fromtimestamp(0)
    cur.execute("insert into checked_on values (?, ?)", (1, epoch))
    db.commit()


def get_version(table_name):
    """Get the most recent version number held in a given table."""
    db = get_db()
    cur = db.cursor()
    cur.execute("select * from {} order by entered_on desc".format(table_name))
    return cur.fetchone()["version"]


def versions_stale():
    """Determine if the information in the db is stale."""
    db = get_db()
    cur = db.cursor()
    cur.execute("select * from checked_on where id = 1")
    last_checked = cur.fetchone()["checked_on"]
    return (datetime.now() - last_checked).total_seconds() > app.config['DELAY']


def update_versions():
    """Update both the game and launcher version information from the API."""
    if not versions_stale():
        return

    print("Getting them versions. Synchronously!!!")

    game_resp = API["GetDistrib"]()
    launcher_resp = API["GetLauncherDistrib"]()

    if game_resp.ok() and launcher_resp.ok():
        db = get_db()
        cur = db.cursor()
        now = datetime.now()
        game, launcher = game_resp.data, launcher_resp.data
        cur.execute(
            "insert or ignore into game_versions values (?, ?, ?, ?)",
            (game["hash"], game["Version"], game["DownloadUri"], now)
        )
        cur.execute(
            "insert or ignore into launcher_versions values (?, ?, ?, ?)",
            (launcher["hash"], launcher["Version"], launcher["DownloadUri"], now)
        )
        cur.execute("update checked_on set checked_on = ? where id = 1", (now,))
    else:
        raise RuntimeError("API Error")
    db.commit()


@app.teardown_appcontext
def close_db(error):
    """Close the database at the end of the request."""
    if hasattr(g, 'sqlite_db'):
        g.sqlite_db.close()


# CLI
@app.cli.command('initdb')
def initdb_command():
    """Initialize the database."""
    try:
        init_db()
        print("Initialized the database.")
    except Exception as e:
        print("Error occured during database init: {}".format(e))


@app.cli.command('seeddb')
def seeddb_command():
    """Seed the database."""
    try:
        update_versions()
        print("Seeded the database.")
    except Exception as e:
        print("Error occured during database init: {}".format(e))


if __name__ == "__main__":
    app.run()
