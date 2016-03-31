# encoding: UTF8
from __future__ import unicode_literals 
# to allow Umlaute in strings without errors. "encoding: UTF8" still required but not sufficient.
import random
import sqlite3

from flask import Flask, render_template, request, url_for, g, session

# before first run, create database with:
# sqlite3 descriptor_contest.db < schema.sql < test_data.sql
# on terminal
#
# TODO move to other file that is not committed to github
# configuration
DEBUG = True # do NOT deploy with debug = True!
SECRET_KEY = "pe1Eefae6oodijiis0iZaahufah2hu"
DATABASE = "descriptor_contest.db"

app = Flask(__name__)
app.config.from_object(__name__)
def connect_db():
    return sqlite3.connect(app.config['DATABASE'])

def choose_two_descriptors():
    user_id = get_user_id()
    cursor = g.db.execute("select * from descriptors where contest_id=1")
    descriptors = [dict(id=row[0], value=row[1]) for row in cursor.fetchall()]
    return random.sample(descriptors, 2)

def save_choice_to_db(form_dict):
    first = form_dict["first"]
    second = form_dict["second"]
    chosen = form_dict["chosen"]
    if first == chosen:
        higher_ranked = first
        lower_ranked = second
    else:
        higher_ranked = second
        lower_ranked = first
    g.db.execute("insert into answers (user_id, higher_ranked_descriptor_id, lower_ranked_descriptor_id) values (?, ?, ?)", 
        [get_user_id(), higher_ranked, lower_ranked])
    g.db.commit()

def get_user_id():
    if "user_id" not in session:
        session["user_id"] = id_from_new_user()
    return session["user_id"]

def id_from_new_user():
    cursor = g.db.execute("insert into users default values")
    g.db.commit()
    return cursor.lastrowid
    
@app.before_request
def before_request():
    g.db = connect_db()
    
@app.teardown_request
def teardown_request(exception):
    db = getattr(g, "db", None)
    if db is not None:
        db.close()

@app.route("/")
def index():
    return render_template('index.html')

@app.route("/choose_descriptor", methods=["GET", "POST"])
def choose_descriptor():
    get_user_id()
    if request.method == 'POST':
        save_choice_to_db(request.form)
    first, second = choose_two_descriptors()
    return render_template('choose_descriptor.html', first=first, second=second)

@app.route("/test", methods=["GET", "POST"])
def test():
    print request.method
    return "foo"


if __name__ == "__main__": # wenn diese Datei direkt ausgeführt wird (python app.py), dann wird app.run aufgerufen
    app.run() # startet Webserver, präsentiert die Applikation, wartet auf Anfragen vom Browser
    

