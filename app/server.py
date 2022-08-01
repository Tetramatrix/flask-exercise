from flask import Flask, render_template, make_response, request, json
from flask_restful import Api, Resource
from webargs import fields
from webargs.flaskparser import use_args, abort
from flask_httpauth import HTTPBasicAuth
import validators
from database import *
from utilities import *

server = Flask(__name__)
api = Api(server)
auth = HTTPBasicAuth()

USER_DATA = {
 "admin" : "password"
}

#route to verify the password
@auth.verify_password
def verify(username, password):
  if not(username and password):
    return False
  return USER_DATA.get(username) == password

@auth.error_handler
def unauthorized():
    # return 403 instead of 401 to prevent browsers from displaying the default
    # auth dialog
    return make_response(jsonify({'message': 'Unauthorized access'}), 403)
    
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
    
    @auth.login_required  
    def post(self):
       bookmarks = []
       for data in request.get_json(force=True):
         date = normalize_date(data['date'])
         title = scrub_input(data['title'])
         url = scrub_input(data['uri'])
         try:
          valid=validators.url(url)
         except:
          print("Invalid url: data dropped!")
          url = -1 
         else:  
          if valid != True:
            print("Invalid url: data dropped!")
            url = -1
     
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
       return {'bookmarks':bookmarks}, 200

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

class BookmarksDateAPI(Resource):
     
    user_args={
      'start':fields.DateTime(required=False, missing=None),
      'end':fields.DateTime(required=False, missing=None) 
    }
    
    def __init__(self):
        self.db = Database()
        self.startquery = "SELECT title,url,date_added from data where date_added >= %s"
        self.endquery = "SELECT title,url,date_added from data where date_added <= %s"
        self.betweenquery = "SELECT title,url,date_added from data where date_added BETWEEN %s and %s"
        self.titles = ['title','uri','date']
        super(BookmarksDateAPI, self).__init__() 
    
    @use_args(user_args, location="querystring")   
    def get(self, args):
        if (args['start'] == None and args['end'] == None):
          abort(400)
   
        if (args['start'] != None and args['end'] == None):
          return jsonify({'bookmarks':[dict(zip(self.titles, entry)) for entry in self.db.fetchall(self.startquery, (args['start']))]})
        
        if (args['start'] == None and args['end'] != None):
          return jsonify({'bookmarks':[dict(zip(self.titles, entry)) for entry in self.db.fetchall(self.endquery, (args['end']))]})
        
        if (args['start'] != None and args['end'] != None):
          return jsonify({'bookmarks':[dict(zip(self.titles, entry)) for entry in self.db.fetchall(self.betweenquery, (args['start'], args['end']))]})
        
  
api.add_resource(BookmarkListAPI, '/avaaz/api/v1.0/bookmarks', endpoint = 'bookmarks')
api.add_resource(BookmarksAPI, '/avaaz/api/v1.0/bookmarks/<int:id>', endpoint = 'bookmark')
api.add_resource(BookmarksTitleAPI, '/avaaz/api/v1.0/bookmarks/title/<string:title>', endpoint = 'title')
api.add_resource(BookmarksUrlAPI, '/avaaz/api/v1.0/bookmarks/url/<string:url>', endpoint = 'url')
api.add_resource(BookmarksDateAPI, '/avaaz/api/v1.0/bookmarks/date', endpoint = 'date')
  
@server.route("/")
def index():
    return render_template('index.html')
     
@server.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)

     
      
if __name__ == "__main__":
    server.run(host='0.0.0.0')
