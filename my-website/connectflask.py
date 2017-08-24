import os
import sqlite3
from sqlalchemy import *
from sqlalchemy.pool import NullPool
from flask import Flask, request, session, g, redirect, url_for, abort, \
     render_template, flash

tmpl_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'templates')

app = Flask(__name__, template_folder=tmpl_dir)
app.config.from_object(__name__)

DATABASEURI = "postgresql://postgres:@localhost/mydb"

engine = create_engine(DATABASEURI)



try:
	conn = engine.connect()
	print("successful connect!")
except:
	print("uh oh, problem connecting to databse")
	import traceback; traceback.print_exc()
	conn = None

cursor = conn.execute("SELECT name FROM cities")
names = []
for result in cursor:
	names.append(result['name'])
print (names[0])
cursor.close() 

@app.teardown_request
def teardown_request(exception):
  """
  At the end of the web request, this makes sure to close the database connection.
  If you don't, the database could run out of memory!
  """
  try:
    g.conn.close()
  except Exception as e:
    pass


