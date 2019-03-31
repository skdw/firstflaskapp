# app.py

from flask import Flask, session, request, make_response, redirect, url_for
from requests import Request, Session
from requests.auth import HTTPBasicAuth
import json
from flask import jsonify
import datetime

app = Flask(__name__)
app.permanent_session_lifetime = datetime.timedelta(days=365)

counter = 1

@app.route('/hello')
def hello():
    return 'Hello!'

def auth_required(f):
    @wraps(f)
    def decorated(*args, *kwargs):
        auth = request.authorization
        if auth and auth.username == 'username' and auth.password == 'password':
            return f(*args, **kwargs)
        return make_response('Could not verify!', 401, {'WWW-Authenticate': 'Basic realm="Login required"'})

@app.route('/login', methods=['GET', 'POST'])
@auth_required
def login():
    return redirect(url_for('/hello'))

def logincopy():
    if request.authorization and request.authorization.username == 'username' and request.authorization.password == 'password':
        return redirect(url_for('/hello'))

    return make_response('Could not verify!', 401, {'WWW-Authenticate': 'Basic realm="Login required"'})
    #requests.get('https://api.github.com/user', auth=HTTPBasicAuth('user', 'pass'))

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