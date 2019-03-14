# app.py

from flask import Flask
from flask import request
import json
app = Flask(__name__)

@app.route('/show_data', methods=['GET','POST'])
def print_json():
    return request.get_json(force=True)

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
