import os
import sqlite3
from sqlalchemy import *
from sqlalchemy.pool import NullPool
from flask import Flask, request, session, g, redirect, url_for, abort, \
     render_template, flash

tmpl_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'templates')

app = Flask(__name__, template_folder=tmpl_dir)


DATABASEURI = "postgresql://postgres:@localhost/mydb"

engine = create_engine(DATABASEURI)


@app.before_request
def before_request():
  try:
    g.conn = engine.connect()
  except:
    print ("haha its not connected loser")
    import traceback; traceback.print_exc()
    g.conn = None

@app.teardown_request
def teardown_request(exception):
  try:
    g.conn.close()
  except Exception as e:
    pass

@app.route('/')
def index():
  print(request.args)
  cursor = g.conn.execute("SELECT name FROM cities")
  names = []
  for result in cursor:
    names.append(result['name'])
  cursor.close()

  context = dict(data = names)

  return render_template("index.html", **context)

if __name__ == "__main__":
  import click

  @click.command()
  @click.option('--debug', is_flag=True)
  @click.option('--threaded', is_flag=True)
  @click.argument('HOST', default='0.0.0.0')
  @click.argument('PORT', default=8111, type=int)
  def run(debug, threaded, host, port):
    """
    This function handles command line parameters.
    Run the server using
        python server.py
    Show the help text using
        python server.py --help
    """

    HOST, PORT = host, port
    print ("running on %s:%d" % (HOST, PORT))
    app.run(host=HOST, port=PORT, debug=debug, threaded=threaded)


  run()



