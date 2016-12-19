
Optional:
    $ > virtualenv -ppython3 env

    $ > source ./env/bin/activate

To install the python requirements:

$ > pip install -r requirements.txt

To create database:

$ > python -c'import database; database.init_db()'


To begin fetching tweets:

$ > python twitter.py

To begin updating tweet counts:

$ > python tweet_count_update.py


To check number of tweets stored:

$ > psql -d tweetsql
$ >     select count(*) from tweet;

