#!/usr/bin/python3
'''Module containing script that starts a Flask web application.'''
from flask import Flask, render_template


app = Flask(__name__)


@app.route('/', strict_slashes=False)
def hello():
    '''Displays 'Hello HBNB!'. '''
    return 'Hello HBNB!'


@app.route('/hbnb', strict_slashes=False)
def hbnb():
    '''Displays "HBNB".'''
    return 'HBNB'


@app.route('/c/<text>', strict_slashes=False)
def c_text(text):
    '''display “C ”, followed by the value of the text variable'''
    text = text.replace('_', ' ')
    return f'C {text}'


@app.route('/python/', defaults={'text': 'is_cool'}, strict_slashes=False)
@app.route('/python/<text>', strict_slashes=False)
def python_text(text):
    '''display “Python ”, followed by the value of the text variable'''
    text = text.replace('_', ' ')
    return f'Python {text}'


@app.route('/number/<int:n>', strict_slashes=False)
def number(n):
    '''display “n is a number” only if n is an integer'''
    return f'{n} is a number'


@app.route('/number_template/<int:n>', strict_slashes=False)
def number_template(n):
    '''
    display a HTML page only if n is an integer:
    H1 tag: “Number: n” inside the tag BODY
    '''
    return render_template('5-number.html', number=n)


@app.route('/number_odd_or_even/<int:n>', strict_slashes=False)
def even_odd(n):
    '''
    display a HTML page only if n is an integer:
    H1 tag: “Number: n is even|odd” inside the tag BODY
    '''
    value = 'even' if (n % 2 == 0) else 'odd'
    return render_template('6-number_odd_or_even.html', number=n, value=value)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
