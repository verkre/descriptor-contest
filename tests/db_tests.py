from unittest import TestCase
from pyexpect import expect

import flask
import app, db
from db import *

class DbTests(TestCase):
    """
    First go at testing with flask, tries to setup the contex so that all the db methods work 
    with as little adaptation as possible."""
    
    def setUp(self):
        app.app.config['TESTING'] = True
        self.client = app.app.test_client()
        self.app_context = app.app.app_context()
        self.app_context.push()
        app.before_request() # create db connection
    
    def tearDown(self):
        app.teardown_request(None) # kill db connection
        self.app_context.pop()
        
    def test_smoke(self):
        user_id = db.id_from_new_user()
        self.fail(user_id)
