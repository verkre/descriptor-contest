from flask import render_template, request, url_for, g, session, redirect

from . import app
import db

# REFACT get contest id from db and URL. then move this function to db module.
def get_contest_id():
    # TODO set contest_id in cookie somewhere (let user choose german/english default set at the beginning)
    # hard-coded to use german descriptors for now.
    if "contest_id" not in session:
        session["contest_id"] = 1
    return session["contest_id"]

def get_user_id():
    if "user_id" not in session:
        session["user_id"] = db.id_from_new_user()
    return session["user_id"]


@app.route("/")
def index():
    return render_template('index.html')

@app.route("/delete_all_answers_from_user", methods=["POST"])
def delete_all():
    db.delete_all_answers_from_user(get_user_id())
    return redirect('/')

@app.route("/choose_descriptor", methods=["GET", "POST"])
def choose_descriptor():
    # ensure user is created
    get_user_id()
    if request.method == 'POST':
        db.save_choice_to_db(request.form, get_user_id())
    if db.is_third_round_over(get_user_id(), get_contest_id()):
        return redirect('show_results')
    round_number, play_count, (first, second) = db.choose_two_descriptors(get_user_id(), get_contest_id())
    return render_template('choose_descriptor.html', **locals())

@app.route("/show_results", methods=["GET", "POST"])
def show_results():
    results_list = db.get_results_from_user(get_user_id(), get_contest_id())
    return render_template('show_results.html', results_list=results_list)

@app.route("/show_results_csv", methods=["GET", "POST"])
def show_results_csv():
    results = db.get_results_from_user(get_user_id(), get_contest_id())
    return '\n'.join([", ".join(map(unicode, each)) for each in results])
