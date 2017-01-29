
Optional (recommended):
    $ > virtualenv -ppython3 env

    $ > source ./env/bin/activate

To install the python requirements:

$ > pip install -r requirements.txt

To create database:

$ > python -c'import database; database.init_db()'


To upgrade database to latest schema:

$ > alembic upgrade head


To begin fetching tweets:

$ > python twitter.py

To begin updating tweet counts:

$ > python refresh_tweet_data.py

    refresh_tweet_data takes the optional local parameter. If provided, it will only  work locally to update the reply counts of tweets.

To update user follower counts:

    refresh_user_followers.py
    Provide the optional 'create' paramater, to try and create new users based on tweet entries.

To check number of tweets stored:

$ > psql -d tweetsql
$ >     select count(*) from tweet;

