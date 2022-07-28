from flask import Flask, render_template, make_response, request
from database import *
from utilities import *

server = Flask(__name__)
db = Database()
          
@server.route("/")
def index():
    return render_template('index.html')

@server.route('/avaaz/api/v1.0/bookmarks', methods=['GET'])
def get_bookmarks():
    return getquery('bookmarks', db.fetchall("SELECT * from data", ""))

@server.route('/avaaz/api/v1.0/bookmarks/<int:bookmark_id>', methods=['GET'])
def get_id(bookmark_id):
    return getquery('bookmark', db.fetchone("SELECT * from data WHERE id = %s", bookmark_id))

@server.route('/avaaz/api/v1.0/bookmarks/title/<string:bookmark_title>', methods=['GET'])
def get_title(bookmark_title):
    return getquery('bookmarks', db.fetchall("SELECT * from data where title Like %s", ("%"+bookmark_title+"%")))

@server.route('/avaaz/api/v1.0/bookmarks/url/<string:bookmark_url>', methods=['GET'])
def get_url(bookmark_url):
    return getquery('bookmarks', db.fetchall("SELECT * from data where REPLACE(REPLACE(url,'http://',''),'https://','') Like %s", ("%"+bookmark_url+"%")))
      
@server.route('/avaaz/api/v1.0/bookmarks', methods=['POST'])
def create_bookmark():
    if not request.json :
        abort(400)
        
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
