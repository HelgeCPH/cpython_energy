

echo "Executing experiment for version 3.13"
cd /minitwit313
source bin/activate

echo "Cleaning database from last run..."
rm /tmp/minitwit.db

sqlite3 /tmp/minitwit.db < $HOME/minitwit/schema.sql
sqlite3 /tmp/minitwit.db < $HOME/minitwit/dump.sql

echo "Starting application"
# Set long timeout to allow for import of data on new experiment start
nohup gunicorn --workers 2 --timeout 120 --bind 0.0.0.0:5000 --chdir $HOME/minitwit/ wsgi:app >> server.log &