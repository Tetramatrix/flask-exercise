from flask import Flask, render_template, jsonify, make_response, request, abort
from database import *
from date_and_data import *

server = Flask(__name__)
      
@server.route("/")
def index():
    return render_template('index.html')

@server.route('/avaaz/api/v1.0/bookmarks', methods=['GET'])
def get_bookmarks():
    db = Database()
    bookmarks = db.fetchall("SELECT * from data", "")
    if len(bookmarks) == 0:
        abort(400)         
    return jsonify({'bookmarks': bookmarks}), 201

@server.route('/avaaz/api/v1.0/bookmarks/<int:bookmark_id>', methods=['GET'])
def get_id(bookmark_id):
    db = Database()
    bookmark = db.fetchone("SELECT * from data WHERE id = %s", bookmark_id)
    if len(bookmark) == 0:
        abort(400)
    return jsonify({'bookmark': bookmark}), 201

@server.route('/avaaz/api/v1.0/bookmarks/title/<string:bookmark_title>', methods=['GET'])
def get_title(bookmark_title):
    db = Database()
    bookmarks=db.fetchall("SELECT * from data where title Like %s", ("%"+bookmark_title+"%"))
    if len(bookmarks) == 0:
        abort(400)
    return jsonify({'bookmarks': bookmarks}), 201
      
@server.route('/avaaz/api/v1.0/bookmarks/url/<string:bookmark_url>', methods=['GET'])
def get_url(bookmark_url):
    db = Database()
    bookmarks=db.fetchall("SELECT * from data where REPLACE(REPLACE(url,'http://',''),'https://','') Like %s", ("%"+bookmark_url+"%"))
    if len(bookmarks) == 0:
        abort(400)   
    return jsonify({'bookmarks': bookmarks}), 201
      
@server.route('/avaaz/api/v1.0/bookmarks', methods=['POST'])
def create_bookmark():
    if not request.json :
        abort(400)
        
    db = Database()
    bookmarks = []
    
    for element in request.json:      
      date = normalize_date(element['date'])
      title = scrub_input(element['title'])
      url = scrub_input(element['uri'])
      
      if (date != -1 and title != -1 and url != -1):
        result = db.insert("INSERT INTO data (url, title, date_added) VALUES (%s, %s, %s)", (url, title, date))
        if (result != 1):
        	print(result)
        
        bookmark = {
            'title': title,
            'uri': url,
            'date': date  
        }
        bookmarks.append(bookmark)
    
    return jsonify({'bookmarks': bookmarks}), 201
      
@server.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)


if __name__ == "__main__":
    server.run(host='0.0.0.0')
