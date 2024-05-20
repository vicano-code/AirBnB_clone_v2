#!/usr/bin/python3
"""
HBNB Flask web application
"""
from flask import Flask, render_template
from models import storage
from models import *

app = Flask(__name__)


@app.teardown_appcontext
def teardown_db(self):
    """remove current SQLAlchemy sessionaftet each request"""
    storage.close()

@app.route('/states_list', strict_slashes=False)
def hbnb_states():
    """display all states in mysql database"""
    stateObjList = [s for s in storage.all("State").values()]
    return render_template('7-states_list.html', data=stateObjList)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
