# app.py

from flask import Flask, session, request, make_response, redirect, url_for
#from requests import Request, Session
#from requests.auth import HTTPBasicAuth
from functools import wraps
import json
from flask import jsonify
import datetime
import os

app = Flask(__name__)
app.permanent_session_lifetime = datetime.timedelta(days=365)
app.secret_key = os.urandom(24)

counter = 1

@app.route('/trains', methods=['GET', 'POST'])
def hello3():
    if getsession() == 999:
        return redirect(url_for('hello'))
    return 'Hello, world!'

@app.route('/hello', methods=['GET', 'POST'])
def hello2():
    if getsession() == 999:
        return redirect(url_for('hello'))
    return 'Hello, world!'

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.authorization and request.authorization.username == 'TRAIN' and request.authorization.password == 'TuN3L':
        session['user'] = 'TRAIN'
        return redirect(url_for('hello2'))
    return make_response('Could not verify!', 401, {'WWW-Authenticate': 'Basic realm="Login required"'})

@app.route('/logout', methods=['GET', 'POST'])
def logout():
    if getsession() == 999:
        return redirect(url_for('login'), code=200)
    return redirect(url_for('dropsession'))

@app.route('/getsession', methods=['GET', 'POST'])
def getsession():
    if 'user' in session:
        return session['user']
    return 999

@app.route('/dropsession', methods=['GET', 'POST'])
def dropsession():
    session.pop('user', None)
    return redirect(url_for('hello'), code=200)

@app.route('/counter')
def countviews():
    global counter
    counter += 1
    return str(counter)

@app.route('/pretty_print_name', methods=['POST'])
def print_pretty_name():
    content = request.get_json()
    return 'Na imię mu {0}, a nazwisko jego {1}'.format(str(content['name']), str(content['surename']))

@app.route('/show_data', methods=['POST'])
def print_json():
    if(request.is_json):
        content = request.get_json()
        return jsonify(content)
    else:
        return 'Not JSON'

@app.route('/method', methods=['GET', 'POST', 'PUT', 'DELETE'])
def print_method():
    return request.method

@app.route('/request')
def request_info():
    return f"request method: {request.method} url: {request.url} headers: {request.headers}"

@app.route('/') # @ - dekorator (funkcja zostanie uzyta, jeśli ktoś zapyta o ściezkę '/')
def hello():
    return 'Hello, World!'

if __name__ == '__main__':
    app.run(debug=True)