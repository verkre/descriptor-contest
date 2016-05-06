# encoding: UTF8
from __future__ import unicode_literals 
# to allow Umlaute in strings without errors. "encoding: UTF8" still required but not sufficient.

from flask import Flask


# TODO move to other file that is not committed to github
# configuration
DEBUG = True # do NOT deploy with debug = True!
SECRET_KEY = "pe1Eefae6oodijiis0iZaahufah2hu"
DATABASE = "descriptor_contest.db"
SQLALCHEMY_DATABASE_URI = 'sqlite:///../descriptor_contest.db'
SQLALCHEMY_TRACK_MODIFICATIONS = False

app = Flask(__name__)
app.config.from_object(__name__)
app.config.from_envvar('DESCRIPTOR_CONTEST_CONFIG', silent=True)

# yes it's a circular import, but it's fine because we're not accessing anything in it
# but just ensure that it is parsed by python
import views
