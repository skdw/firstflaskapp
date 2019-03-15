# app.py

from flask import Flask
from flask import request
import json
app = Flask(__name__)

@app.route('/pretty_print_name', methods=['POST'])
def print_pretty_name():
    content = request.get_json()
    return 'Na imię mu {0}, a nazwisko jego {1}'.format(str(content['name']), str(content['surename']))

@app.route('/show_data', methods=['POST'])
def print_json():
    if(request.is_json):
        content = request.get_json()
        return str(content)
    else:
        return 'Not JSON'

@app.route('/method', methods=['GET', 'POST', 'PUT', 'DELETE'])
def print_method():
    return request.method

@app.route('/request')
def request_info():
    return f'request method: {request.method} url: {request.url} headers: {request.headers}'

@app.route('/') # @ - dekorator (funkcja zostanie uzyta, jeśli ktoś zapyta o ściezkę '/')
def hello():
    return 'Hello, World!'

if __name__ == '__main__':
    app.run(debug=True)
