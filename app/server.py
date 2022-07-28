from flask import Flask, render_template, make_response, request, json
from flask_restful import Api, Resource, reqparse
from flask_httpauth import HTTPBasicAuth
from database import *
from utilities import *

server = Flask(__name__)
api = Api(server)
auth = HTTPBasicAuth()
db = Database()
        
def createbookmark(data):
  bookmarks = []
  date = normalize_date(data['date'])
  title = scrub_input(data['title'])
  url = scrub_input(data['uri'])
  
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
  return bookmarks
  
@server.route("/")
def index():
    return render_template('index.html')

class BookmarkListAPI(Resource):
    def get(self):
        result = db.fetchall("SELECT title,url,date_added from data", "")
        return jsonify({'bookmarks':result})
        
    def post(self):
        pass

class BookmarksAPI(Resource):
    def get(self, id):
        return jsonify({'bookmark':db.fetchone("SELECT id,title,url,date_added from data WHERE id = %s", id)})

class BookmarksTitleAPI(Resource):
    def get(self, title):
        return jsonify({'bookmarks':db.fetchall("SELECT title,url,date_added from data where title Like %s", ("%"+title+"%"))})

class BookmarksUrlAPI(Resource):
    def get(self, url):
       return jsonify({'bookmarks':db.fetchall("SELECT title,url,date_added from data where REPLACE(REPLACE(url,'http://',''),'https://','') Like %s", ("%"+url+"%"))})

api.add_resource(BookmarkListAPI, '/avaaz/api/v1.0/bookmarks', endpoint = 'bookmarks')
api.add_resource(BookmarksAPI, '/avaaz/api/v1.0/bookmark/<int:id>', endpoint = 'bookmark')
api.add_resource(BookmarksTitleAPI, '/avaaz/api/v1.0/bookmarks/title/<string:title>', endpoint = 'title')
api.add_resource(BookmarksUrlAPI, '/avaaz/api/v1.0/bookmarks/url/<string:url>', endpoint = 'url')
      
@server.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)

@auth.verify_password
def authenticate(username, password):
    if username and password:
      if username == 'admin' and password == 'admin':
        return True
    else:
      return False
    return False

if __name__ == "__main__":
    server.run(host='0.0.0.0')
