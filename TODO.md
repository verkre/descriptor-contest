# TODO

* in second round: let winners and losers play against each other, respectively
* make show_results page
* add a "start new" button -> delete all answers from that user
* allow (force?) user to enter their name (and more info?) at some point of the game
* make results/statistics downloadable for the admin (hidden URL)
* show progress during game
* add automatic deployment to cloud hosting service
* add acceptance tests


# LATER
* create admin role
* restrict downloading of statistics to admin
* show list of contests to admin
* let admin create new contests (incl. their own sets of descriptors)


# DONE
* write user's answers to database
* create user when starting a game
* keep user during all of a game
* only present each descriptor once per round
    * one query for preferred and rejected descriptors counts
    * a method to add these
    * a method to find out in which round we are (is_first_round(), is_second_round())
    * a method to load remaining first round descriptors and remaining second round descriptors

