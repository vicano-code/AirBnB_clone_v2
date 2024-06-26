#!/usr/bin/python3
"""
Starts a Flask web application listening on 0.0.0.0, port 5000
Usage: python3 -m web_flask.0-hello_route
"""

from flask import Flask, render_template

app = Flask(__name__)
app.url_map.strict_slashes = False


@app.route('/')
def hello_hbnb():
    """ display 'Hello HBNB!' """
    return "Hello HBNB!"


@app.route('/hbnb')
def hbnb():
    """ display 'HBNB' """
    return "HBNB"


@app.route('/c/<text>')
def c_text(text):
    """ display 'C' followed by the value of the text variable """
    return 'C {}'.format(text.replace('_', ' '))


@app.route('/python/')
@app.route('/python/<text>')
def python_text(text="is cool"):
    """display 'Python', followed by the value of the text variable"""
    return 'Python {}'.format(text.replace('_', ' '))


@app.route('/number/<int:n>')
def display_number(n):
    """display 'n is a number' only if n is an integer"""
    return '{} is a number'.format(n)


@app.route('/number_template/<int:n>')
def number_template(n):
    """display a HTML page only if n is an integer"""
    return render_template('5-number.html', n=n)


@app.route('/number_odd_or_even/<int:n>')
def number_odd_or_even(n):
    """
    display a HTML page only if n is an integer
    H1 tag: “Number: n is even|odd” inside the tag BODY
    """
    if isinstance(n, int):
        odd_or_even = 'even' if n % 2 == 0 else 'odd'
        return render_template('6-number_odd_or_even.html',
                               n=n, result=odd_or_even)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
