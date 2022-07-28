from flask_restful import Api, Resource

api = Api(app)

class BookmarksAPI(Resource):
    def get(self):
        pass

    def post(self):
        pass

class BookmarkAPI(Resource):
    def get(self, id):
        pass

class BookmarkTitleAPI(Resource):
    def get(self, id):
        pass

class BookmarkUrlAPI(Resource):
    def get(self, id):
        pass
        
api.add_resource(BookmarksAPI, '/avaaz/api/v1.0/bookmarks', endpoint = 'bookmarks')
api.add_resource(BookmarkAPI, '/avaaz/api/v1.0/bookmarks/<int:id>', endpoint = 'bookmarks')
api.add_resource(BookmarksTitleAPI, '/avaaz/api/v1.0/bookmarks/title/<string:bookmark_title>', endpoint = 'title')
api.add_resource(BookmarksUrlAPI, '/avaaz/api/v1.0/bookmark/url/<string:bookmark_url>', endpoint = 'url')
