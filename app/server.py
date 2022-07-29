from flask import Flask, render_template, make_response, request, json
from flask_restful import Api, Resource, reqparse
from flask_httpauth import HTTPBasicAuth
from database import *
from utilities import *

server = Flask(__name__)
api = Api(server)
auth = HTTPBasicAuth()

class BookmarkListAPI(Resource):
    def __init__(self):
        self.db = Database()
        self.getquery = "SELECT title,url,date_added from data"
        self.params = ""
        self.postquery = "INSERT INTO data (url, title, date_added) VALUES (%s, %s, %s)"
        self.titles = ['title','uri','date']
        super(BookmarkListAPI, self).__init__()

    def get(self):
        return jsonify({'bookmarks':[dict(zip(self.titles, entry)) for entry in self.db.fetchall(self.getquery, self.params)]})
        
    def post(self):
       bookmarks = []
       for data in request.get_json(force=True):
         date = normalize_date(data['date'])
         title = scrub_input(data['title'])
         url = scrub_input(data['uri'])
          
         if (date != -1 and title != -1 and url != -1):
          result = self.db.insert(self.postquery, (url, title, date))
          if (result != 1):
           print(result)
          bookmark = {
              'title': title,
              'uri': url,
              'date': date  
          }
          bookmarks.append(bookmark)        
       return {'bookmarks':bookmarks}, 201

class BookmarksAPI(Resource):
    def __init__(self):
        self.db = Database()
        self.query = "SELECT id,title,url,date_added from data WHERE id = %s"
        self.titles = ['id','title','uri','date']
        super(BookmarksAPI, self).__init__()
       
    def get(self, id):
        return jsonify({'bookmark':[dict(zip(self.titles, self.db.fetchone(self.query, id)))]})

class BookmarksTitleAPI(Resource):
    def __init__(self):
        self.db = Database()
        self.query = "SELECT title,url,date_added from data where title Like %s"
        self.titles = ['title','uri','date']
        super(BookmarksTitleAPI, self).__init__()
    
    def get(self, title):
        return jsonify({'bookmarks':[dict(zip(self.titles, entry)) for entry in self.db.fetchall(self.query, ("%"+title+"%"))]})

class BookmarksUrlAPI(Resource):
    def __init__(self):
        self.db = Database()
        self.query = "SELECT title,url,date_added from data where REPLACE(REPLACE(url,'http://',''),'https://','') Like %s"
        self.titles = ['title','uri','date']
        super(BookmarksUrlAPI, self).__init__() 
  
    def get(self, url):
       return jsonify({'bookmarks':[dict(zip(self.titles, entry)) for entry in self.db.fetchall(self.query, ("%"+url+"%"))]})

api.add_resource(BookmarkListAPI, '/avaaz/api/v1.0/bookmarks', endpoint = 'bookmarks')
api.add_resource(BookmarksAPI, '/avaaz/api/v1.0/bookmark/<int:id>', endpoint = 'bookmark')
api.add_resource(BookmarksTitleAPI, '/avaaz/api/v1.0/bookmarks/title/<string:title>', endpoint = 'title')
api.add_resource(BookmarksUrlAPI, '/avaaz/api/v1.0/bookmarks/url/<string:url>', endpoint = 'url')

  
@server.route("/")
def index():
    return render_template('index.html')


      
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
