from unittest import TestCase
from pyexpect import expect
from collections import defaultdict

from flask import g
from .. import app, db, views

class DbTests(TestCase):
    """
    First go at testing with flask, tries to setup the contex so that all the db methods work 
    with as little adaptation as possible.
    """
    
    def setUp(self):
        app.config['TESTING'] = True
        self.client = app.test_client()
        self.app_context = app.app_context()
        self.app_context.push()
        db.before_request() # create db connection
        
        self.contest_id = 2 # english
        self.descriptor_ids = db.list_descriptor_ids_in_contest(self.contest_id)
        self.user_id = db.id_from_new_user()
    
    def tearDown(self):
        # just a nicety, since we generate a new user for each test
        # the cleanup isn't strictly neccessary
        db.delete_all_answers_from_user(self.user_id)
        
        app.teardown_request(None) # kill db connection
        self.app_context.pop()
        
    def test_insert_answers(self):
        expect(db.how_many_pairs_played(self.user_id, self.contest_id)) == 0
        db.save_choice_to_db(
            dict(
                first=self.descriptor_ids[0],
                second=self.descriptor_ids[1],
                chosen=self.descriptor_ids[1]),
            self.user_id)
        expect(db.how_many_pairs_played(self.user_id, self.contest_id)) == 1
        db.save_choice_to_db(
            dict(
                first=self.descriptor_ids[2],
                second=self.descriptor_ids[3],
                chosen=self.descriptor_ids[3]),
            self.user_id)
        expect(db.how_many_pairs_played(self.user_id, self.contest_id)) == 2
    
    
    def _play_rounds(self, how_often, round_number, start_index, assertion=None):
        for index in range(how_often):
            round_number, play_count, (first, second) = db.choose_two_descriptors(self.user_id, self.contest_id)
            expect(round_number) == round_number
            expect(play_count) == start_index + index
            if assertion is not None:
                assertion(locals())
            db.save_choice_to_db(
                dict(first=first['id'], second=second['id'], chosen=first['id']),
                str(self.user_id))
    
    def _results_by_play_count(self):
        by_play_count = defaultdict(list)
        for result in db.get_results_from_user(self.user_id, self.contest_id):
            by_play_count[result[1]].append(result)
        return by_play_count
    
    def test_choose_descriptors_will_choose_each_pair_of_descriptors_once_in_first_round(self):
        "10 pairs in the first round"
        self._play_rounds(10, 1, 0)
        expect(db.how_many_pairs_played(self.user_id, self.contest_id)) == 10
        expect(db.list_descriptors_played_once(self.user_id, self.contest_id)).has_length(20)
        for result in db.get_results_from_user(self.user_id, self.contest_id):
            expect(result[1]).in_(0,1)
    
    def test_choose_descriptors_will_choose_each_winner_from_first_round_once_in_second_round(self):
        "5 pairs in the second round (winners of first round)"
        self._play_rounds(10, 1, 0)
        higher_ranked_ids = [id for (id,) in g.db.execute('''
            select descriptors.id from descriptors 
            join answers on descriptors.id == answers.higher_ranked_descriptor_id 
            where contest_id = :contest_id and user_id = :user_id
            group by descriptors.id having count(1) = 1''',
            self.__dict__).fetchall()]
        expect(higher_ranked_ids).has_length(10)
        
        def assertion(locals):
            expect(locals['first']['id']).in_(higher_ranked_ids)
            expect(locals['second']['id']).in_(higher_ranked_ids)
        
        self._play_rounds(5, 2, 10, assertion)
        expect(db.how_many_pairs_played(self.user_id, self.contest_id)) == 15
        
        by_play_count = self._results_by_play_count()
        expect(by_play_count[0]).has_length(10)
        expect(by_play_count[1]).has_length(5)
        expect(by_play_count[2]).has_length(5)
    
    def test_choose_descriptors_will_choose_each_loser_from_the_first_round_once_in_third_round(self):
        "5 pairs in the third round (loswers of the first round)"
        self._play_rounds(10, 1, 0)
        lower_ranked_ids = [id for (id,) in g.db.execute('''
            select descriptors.id from descriptors 
            join answers on descriptors.id == answers.lower_ranked_descriptor_id 
            where contest_id = :contest_id and user_id = :user_id
            group by descriptors.id having count(1) = 1''',
            self.__dict__).fetchall()]
        expect(lower_ranked_ids).has_length(10)
        self._play_rounds(5, 2, 10)
        
        def assertion(locals):
            expect(locals['first']['id']).in_(lower_ranked_ids)
            expect(locals['second']['id']).in_(lower_ranked_ids)
        
        self._play_rounds(5, 3, 15, assertion)
        
        by_play_count = self._results_by_play_count()
        expect(by_play_count[0]).has_length(5)
        expect(by_play_count[1]).has_length(10)
        expect(by_play_count[2]).has_length(5)
    
    def test_sqlalchemy(self):
        # import pdb; pdb.set_trace()
        from ..models import Contest
        print Contest.query.all()
        fail()
