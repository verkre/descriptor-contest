# encoding: UTF8
from __future__ import unicode_literals 
# to allow Umlaute in strings without errors. "encoding: UTF8" still required but not sufficient.
import random
import sqlite3

from flask import Flask, render_template, request, url_for, g

# before running, create database with:
# sqlite3 descriptor_contest.db < schema.sql < test_data.sql
# on terminal
#
# TODO move to other file
# configuration
DEBUG = True
SECRET_KEY = "pe1Eefae6oodijiis0iZaahufah2hu"
DATABASE = "descriptor_contest.db"

app = Flask(__name__) # app ist eine Instanz von Flask
app.config.from_object(__name__)
def connect_db():
    return sqlite3.connect(app.config['DATABASE'])

def choose_two_descriptors():
    cursor = g.db.execute("select * from descriptors where contest_id=1")
    descriptors = [dict(id=row[0], value=row[1]) for row in cursor.fetchall()]
    return random.sample(descriptors, 2)

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
    if request.method == 'POST':
        print request.form
    first, second = choose_two_descriptors()
    return render_template('choose_descriptor.html', first=first, second=second)
    

if __name__ == "__main__": # wenn diese Datei direkt ausgeführt wird (python app.py), dann wird app.run aufgerufen
    app.run() # startet Webserver, präsentiert die Applikation, wartet auf Anfragen vom Browser
    
    # do NOT deploy with debug = True!

