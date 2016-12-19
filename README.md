
virtualenv -ppython3 env

source ./env/bin/activate

pip install -r requirements.txt

To create database:

python -c'import database; database.init_db()'


CHANGE_LIST

Tweets without coordinates / place will still be stored


