# app.py

from flask import Flask, jsonify, session, request, make_response, redirect, url_for, render_template, g
import sqlite3
import json
import datetime
import os

app = Flask(__name__)
app.permanent_session_lifetime = datetime.timedelta(days=365)
app.secret_key = os.urandom(24)

counter = 1

DATABASE = 'chinook.db'

@app.route('/tracks', methods=['GET', 'POST'])
def tracks_list():
    # POST request
    if(request.method == 'POST' and request.is_json):
        content = request.get_json()

        keys = ['album_id', 'media_type_id', 'genre_id', 'name', 'composer', 'milliseconds', 'bytes', 'price']
        tablekeys = ['AlbumId', 'MediaTypeId', 'GenreId', 'name', 'Composer', 'Milliseconds', 'Bytes', 'UnitPrice']

        for key in keys:
            if not key in content:
                return redirect(('/'), code=400)

        keys_str = ""
        values_str = ""
        for i in range(len(keys)):
            if(keys_str != ""):
                keys_str += ", "
                values_str += ", "
            keys_str += tablekeys[i]
            if(type(content[keys[i]]) == str):
                values_str += "'" + str(content[keys[i]]) + "'"
            else: 
                values_str += str(content[keys[i]])

        query1 = "INSERT INTO tracks (" + keys_str + ") VALUES (" + values_str + ")"
        query2 = "SELECT * FROM tracks WHERE TrackId = last_insert_rowid()"
        query3 = "SELECT name FROM PRAGMA_TABLE_INFO('tracks')"

        db = get_db()
        cursor = db.cursor()
        cursor.execute(query1).fetchall()
        data = cursor.execute(query2).fetchall()
        columns = cursor.execute(query3).fetchall()
        cursor.close()
        val = [dat for dat in data[0]]
        keys = [dat[0] for dat in columns]
        d = dict(zip(keys,val))
        return jsonify(d)

    # GET request
    if(request.method == 'GET'):
        querystr = 'SELECT tracks.Name FROM tracks'
        artist = request.args.get('artist')
        if(artist):
            querystr += ' JOIN albums on albums.AlbumId = tracks.AlbumId JOIN artists on artists.ArtistId = albums.ArtistID'
            querystr += ' WHERE artists.Name ='
            querystr += " '" + str(artist) + "'"
        querystr += ' ORDER by tracks.Name COLLATE NOCASE'
        
        limit = request.args.get('per_page')
        if(limit):
            querystr += ' LIMIT ' + str(limit)

        page = request.args.get('page')
        if(page and limit):
            offset = (int(page) - 1) * int(limit)
            querystr += ' OFFSET ' + str(offset)

        #print(querystr)
        db = get_db()
        cursor = db.cursor()
        data = cursor.execute(querystr).fetchall()
        d = [item[0] for item in data]
        cursor.close()
        return jsonify(d)
    return redirect(('/'), code=400)

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    return db

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

@app.route('/trains', methods=['GET', 'POST'])
def hello3():
    if 'user' in session:
        myformat = 'XML'
        if request.args.get('format') == 'json':
            myformat = 'JSON'
        print('format: ' + myformat)
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