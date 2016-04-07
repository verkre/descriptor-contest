# encoding: UTF8
from __future__ import unicode_literals 
# to allow Umlaute in strings without errors. "encoding: UTF8" still required but not sufficient.

from flask import Flask, render_template, request, url_for, g, session, redirect

from db import *

# TODO move to other file that is not committed to github
# configuration
DEBUG = True # do NOT deploy with debug = True!
SECRET_KEY = "pe1Eefae6oodijiis0iZaahufah2hu"
DATABASE = "descriptor_contest.db"

app = Flask(__name__)
app.config.from_object(__name__)
app.config.from_envvar('DESCRIPTOR_CONTEST_CONFIG', silent=True)

# REFACT get contest id from db and URL. then move this function to db module.
def get_contest_id():
    # TODO set contest_id in cookie somewhere (let user choose german/english default set at the beginning)
    # hard-coded to use german descriptors for now.
    if "contest_id" not in session:
        session["contest_id"] = 1
    return session["contest_id"]
    

def get_user_id():
    if "user_id" not in session:
        session["user_id"] = id_from_new_user()
    return session["user_id"]
    
@app.before_request
def before_request():
    g.db = connect_db(app)
    
@app.teardown_request
def teardown_request(exception):
    db = getattr(g, "db", None)
    if db is not None:
        db.close()

@app.route("/")
def index():
    return render_template('index.html')

@app.route("/delete_all_answers_from_user", methods=["POST"])
def delete_all():
    delete_all_answers_from_user(get_user_id())
    return redirect('/')

@app.route("/choose_descriptor", methods=["GET", "POST"])
def choose_descriptor():
    # ensure user is created
    get_user_id()
    if request.method == 'POST':
        save_choice_to_db(request.form, get_user_id())
    if is_third_round_over(get_user_id(), get_contest_id()):
        return redirect('show_results')
    round_number, play_count, (first, second) = choose_two_descriptors(get_user_id(), get_contest_id())
    return render_template('choose_descriptor.html', **locals())

@app.route("/show_results", methods=["GET", "POST"])
def show_results():
    return "results"

@app.route("/show_results_csv", methods=["GET", "POST"])
def show_results_csv():
    results = get_results_from_user(get_user_id(), get_contest_id())
    return '\n'.join([", ".join(map(unicode, each)) for each in results])


if __name__ == "__main__": # wenn diese Datei direkt ausgeführt wird (python app.py), dann wird app.run aufgerufen
    app.run() # startet Webserver, präsentiert die Applikation, wartet auf Anfragen vom Browser
    

