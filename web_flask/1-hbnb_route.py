#!/usr/bin/python3
"""
Starts a Flask web application listening on 0.0.0.0, port 5000
Usage: python3 -m web_flask.0-hello_route
"""

from flask import Flask

app = Flask(__name__)


@app.route('/', strict_slashes=False)
def hello_hbnb():
    """ display 'Hello HBNB!' """
    return "Hello HBNB!"


@app.route('/hbnb', strict_slashes=False)
def hbnb():
    """ display 'HBNB' """
    return "HBNB"


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
