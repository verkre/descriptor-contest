# encoding: UTF8
from __future__ import unicode_literals 
# to allow Umlaute in strings without errors. "encoding: UTF8" still required but not sufficient.

import sqlite3
import random

from flask import g


# before first run, create database with:
# sqlite3 descriptor_contest.db < schema.sql < test_data.sql
# on terminal
#


def connect_db(database_path):
    return sqlite3.connect(database_path)

def choose_two_descriptors(user_id, contest_id):
    unplayed_descriptors_query = """
        select * from descriptors 
        left outer join answers 
            on (
                descriptors.id=answers.higher_ranked_descriptor_id
                or descriptors.id=answers.lower_ranked_descriptor_id
            )
            and user_id=:user_id 
        where contest_id=:contest_id 
        group by descriptors.id
        having count(answers.id) = 0
        """
    
    # just the winners
    descriptors_with_winner_counts_query = """
        select * from descriptors 
        join answers on descriptors.id=answers.higher_ranked_descriptor_id 
        where contest_id=:contest_id and user_id=:user_id 
        group by descriptors.id 
        having count(answers.id)=:play_count
        -- directly after the first round, we don't need to filter out higher ranked ones
        """
    
    play_counts_query = """
        select descriptors.id as descriptor_id, count(answers.id) as play_count
        from descriptors 
        left outer join answers
            on descriptors.id=answers.higher_ranked_descriptor_id
            or descriptors.id=answers.lower_ranked_descriptor_id
        where contest_id=:contest_id and user_id=:user_id 
        group by descriptors.id 
        """
    
    descriptors_with_loser_counts_query = """
        select count(answers.id) as play_count, descriptors.id as descriptor_id 
        from descriptors 
        left outer join answers on descriptors.id=answers.lower_ranked_descriptor_id 
        where contest_id=:contest_id and user_id=:user_id 
        group by descriptors.id 
        """
    
    first_round_losers_query = """
        select * from descriptors 
        join ({descriptors_with_loser_counts_query}) as losers
            on descriptors.id=losers.descriptor_id 
        join ({play_counts_query}) as play_counts
            on descriptors.id = play_counts.descriptor_id
        where contest_id=:contest_id
            and play_counts.play_count = :play_count
            and losers.play_count = :play_count
        """.format(**locals())
    play_count = how_many_pairs_played(user_id, contest_id)
    
    if not is_first_round_over(user_id, contest_id):
        cursor = g.db.execute(unplayed_descriptors_query, dict(contest_id=contest_id, user_id=user_id))
        descriptors = [dict(id=row[0], value=row[1]) for row in cursor.fetchall()]
        round_number = 1
        return round_number, play_count, random.sample(descriptors, 2)
    
    # winners from first round
    elif not is_second_round_over(user_id, contest_id):
        cursor = g.db.execute(descriptors_with_winner_counts_query, 
            dict(contest_id=contest_id, user_id=user_id, play_count=1))
        descriptors = [dict(id=row[0], value=row[1]) for row in cursor.fetchall()]
        round_number = 2
        return round_number, play_count, random.sample(descriptors, 2)
    
    # losers from first round
    elif not is_third_round_over(user_id, contest_id):
        cursor = g.db.execute(first_round_losers_query,
            dict(contest_id=contest_id, user_id=user_id, play_count=1))
        descriptors = [dict(id=row[0], value=row[1]) for row in cursor.fetchall()]
        round_number = 3
        return round_number, play_count, random.sample(descriptors, 2)
        
    else:
        round_number = 4
        return round_number, play_count, (None, None)

def get_results_from_user(user_id, contest_id):
    query = """
    select value, higher_ranked_play_count from descriptors 
    left outer join (
        select count(answers.id) as higher_ranked_play_count, descriptors.id as inner_descriptor_id 
        from descriptors 
        left outer join answers on descriptors.id=answers.higher_ranked_descriptor_id 
        where contest_id=? and answers.user_id=?
        group by descriptors.id 
    ) on descriptors.id=inner_descriptor_id 
    where descriptors.contest_id=? 
    order by higher_ranked_play_count desc
    """
    # REFACT get sql to get the zeros right
    cursor = g.db.execute(query, [contest_id, user_id, contest_id])
    return [(row[0], row[1] or 0) for row in cursor.fetchall()]

def how_many_pairs_played(user_id, contest_id):
    cursor = g.db.execute("""
        select count(answers.id), * from descriptors
        join answers on descriptors.id=answers.higher_ranked_descriptor_id
        where contest_id=? and user_id=?""", [contest_id, user_id])
    return cursor.fetchone()[0]

def list_descriptor_ids_in_contest(contest_id):
    cursor = g.db.execute("select * from descriptors where contest_id=?", [contest_id])
    ids = []
    for row in cursor.fetchall():
        ids.append(row[0])
    return ids

def list_descriptors_played_once(user_id, contest_id):
    ids_played = []
    cursor_higher = g.db.execute("""
        select * from descriptors
        left outer join answers
            on descriptors.id=answers.higher_ranked_descriptor_id
            or descriptors.id=answers.lower_ranked_descriptor_id
        where contest_id=? and user_id=?
        group by descriptors.id
        having count(answers.id) = 1
        """, [contest_id, user_id])
    return [row[0] for row in cursor_higher.fetchall()]
    

def how_many_descriptors_in_contest(contest_id):
    cursor = g.db.execute("select count(id) from descriptors where contest_id=?", [contest_id])
    return cursor.fetchall()[0][0]
    # seems a little ugly with the cursor.fetchall etc - the statement itself returns just a number in the sqlite3-shell

def is_first_round_over(user_id, contest_id):
    # account for the possibility of there being an odd number of descriptors - one will not be played then
    rounded_down_to_even = how_many_descriptors_in_contest(contest_id) - (how_many_descriptors_in_contest(contest_id) % 2)
    return how_many_pairs_played(user_id, contest_id) >= rounded_down_to_even / 2

def is_second_round_over(user_id, contest_id):
    rounded_down_to_even = how_many_descriptors_in_contest(contest_id) - (how_many_descriptors_in_contest(contest_id) % 2)
    return how_many_pairs_played(user_id, contest_id) >= rounded_down_to_even / 2 * 1.5

def is_third_round_over(user_id, contest_id):
    rounded_down_to_even = how_many_descriptors_in_contest(contest_id) - (how_many_descriptors_in_contest(contest_id) % 2)
    return how_many_pairs_played(user_id, contest_id) >= rounded_down_to_even

def save_choice_to_db(form_dict, user_id):
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
        [user_id, higher_ranked, lower_ranked])
    g.db.commit()


def id_from_new_user():
    cursor = g.db.execute("insert into users default values")
    g.db.commit()
    return cursor.lastrowid

def delete_all_answers_from_user(user_id):
    g.db.execute("delete from answers where user_id=?", [user_id])
    g.db.commit()
