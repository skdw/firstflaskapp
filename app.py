# app.py

from flask import Flask, jsonify, session, request, make_response, redirect, url_for, render_template
import json
import datetime
import os

app = Flask(__name__)
app.permanent_session_lifetime = datetime.timedelta(days=365)
app.secret_key = os.urandom(24)

counter = 1

@app.route('/trains', methods=['GET', 'POST'])
def hello3():
    if 'user' in session:
        print('type(request.query_string):', request.query_string)
        #return redirect(url_for('hello'))
    else:
        return redirect(url_for('login'), code=301)

@app.route('/hello', methods=['GET'])
def hello2():
    if 'user' in session:
        render = render_template('hello.html', user = session['user'])
        return render
    return redirect(url_for('login'), code=301)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.authorization and request.authorization.username == 'TRAIN' and request.authorization.password == 'TuN3L':
        session['user'] = 'TRAIN'
        return redirect(url_for('hello2'))
    return make_response('Could not verify!', 401, {'WWW-Authenticate': 'Basic realm="Login required"'})

@app.route('/logout', methods=['GET', 'POST'])
def logout():
    if 'user' in session:
        session.pop('user', None)
        return redirect(url_for('hello'))
    return redirect(url_for('login'), code=301)

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