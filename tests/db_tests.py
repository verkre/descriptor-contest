from unittest import TestCase
from pyexpect import expect

import flask
import app, db
from db import *

class DbTests(TestCase):
    """
    First go at testing with flask, tries to setup the contex so that all the db methods work 
    with as little adaptation as possible.
    """
    
    def setUp(self):
        app.app.config['TESTING'] = True
        self.client = app.app.test_client()
        self.app_context = app.app.app_context()
        self.app_context.push()
        app.before_request() # create db connection
        
        self.contest_id = 2 # english
        self.descriptor_ids = db.list_descriptor_ids_in_contest(self.contest_id)
        self.user_id = db.id_from_new_user()
    
    def tearDown(self):
        # just a nicety, since we generate a new user for each test
        # the cleanup isn't strictly neccessary
        delete_all_answers_from_user(self.user_id)
        
        app.teardown_request(None) # kill db connection
        self.app_context.pop()
        
    def test_insert_answers(self):
        expect(how_many_pairs_played(self.user_id, self.contest_id)) == 0
        db.save_choice_to_db(
            dict(
                first=self.descriptor_ids[0],
                second=self.descriptor_ids[1],
                chosen=self.descriptor_ids[1]),
            self.user_id)
        expect(how_many_pairs_played(self.user_id, self.contest_id)) == 1
        db.save_choice_to_db(
            dict(
                first=self.descriptor_ids[2],
                second=self.descriptor_ids[3],
                chosen=self.descriptor_ids[3]),
            self.user_id)
        expect(how_many_pairs_played(self.user_id, self.contest_id)) == 2
    
    def test_choose_descriptors_will_choose_each_pair_of_descriptors_once_in_first_round(self):
        for index in range(10):
            # import sys; sys.stdout = sys.__stdout__; from pdb import set_trace; set_trace()
            round_number, play_count, (first, second) = db.choose_two_descriptors(self.user_id, self.contest_id)
            expect(round_number) == 1
            expect(play_count) == index
            db.save_choice_to_db(
                dict(first=first['id'], second=second['id'], chosen=first['id']),
                str(self.user_id))
        expect(how_many_pairs_played(self.user_id, self.contest_id)) == 10
        expect(list_descriptors_played_once(self.user_id, self.contest_id)).has_length(20)
