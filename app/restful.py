from flask_restful import Api, Resource, reqparse
from database import *

api = Api(server)
db = Database()

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