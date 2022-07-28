import pymysql.cursors, re, datetime, os
from flask import Flask, render_template, jsonify, make_response, request, abort
server = Flask(__name__)
bookmarks = []

def normalize_date(date):
  try: 
    datetime_object = datetime.datetime.strptime(date, '%B %d %Y')           
  except:
    try:
      datetime_object = datetime.datetime.strptime(date, '%d %b %Y')
    except: 
       match = re.search("\d{4}-\d{2}-\d{2}", date)
       if match is None:
        print ("Not a valid date: data dropped!")
        date = -1
       if match is not None:
        print("Date confirmed: "+date)
    else: 
      date = datetime_object.strftime("%Y-%m-%d")
      print("Date confirmed: "+date)
  else:
   date = datetime_object.strftime("%Y-%m-%d")
   print("Date confirmed: "+date)              
  return date

def scrub_input(data):
  if (data == "null" or data == ""):
    print("Not a valid data: data dropped!")
    data = -1
  return data
    
def get_db_connection():
  try:
    connection = pymysql.connect(host=os.environ.get('MYSQL_HOST'),
                                 user=os.environ.get('MYSQL_USER'),
                                 password=os.environ.get('MYSQL_PWD'),
                                 database=os.environ.get('MYSQL_DB'))
  except: 
    print("MySQL connection error!")
  else:
    return connection
      
@server.route("/")
def index():
    return render_template('index.html')

@server.route('/avaaz/api/v1.0/bookmarks', methods=['GET'])
def get_bookmarks():
    connection = get_db_connection()
    query = "SELECT * from data"
    cursor = connection.cursor()
    cursor.execute(query)
    bookmarks=cursor.fetchall()
    cursor.close()
    if len(bookmarks) == 0:
        abort(400)
    connection.close()            
    return jsonify({'bookmarks': bookmarks}), 201

@server.route('/avaaz/api/v1.0/bookmarks/<int:bookmark_id>', methods=['GET'])
def get_id(bookmark_id):
    connection = get_db_connection()
    query = "SELECT * from data WHERE id = %s"
    params = (bookmark_id)
    cursor = connection.cursor()
    cursor.execute(query, params)
    bookmark=cursor.fetchone()
    if len(bookmark) == 0:
        abort(400)
    connection.close()
    return jsonify({'bookmark': bookmark}), 201

@server.route('/avaaz/api/v1.0/bookmarks/title/<string:bookmark_title>', methods=['GET'])
def get_title(bookmark_title):
    connection = get_db_connection()
    query = "SELECT * from data where title Like %s"
    params = "%"+bookmark_title+"%"
    cursor = connection.cursor()
    cursor.execute(query, (params))
    bookmarks=cursor.fetchall()
    if len(bookmarks) == 0:
        abort(400)
    connection.close()
    return jsonify({'bookmarks': bookmarks}), 201
      
@server.route('/avaaz/api/v1.0/bookmarks/url/<string:bookmark_url>', methods=['GET'])
def get_url(bookmark_url):
    connection = get_db_connection()
    query = "SELECT * from data where REPLACE(REPLACE(url,'http://',''),'https://','') Like %s"
    params = "%"+bookmark_url+"%"
    cursor = connection.cursor()
    cursor.execute(query, (params))
    bookmarks=cursor.fetchall()
    if len(bookmarks) == 0:
        abort(400)
    connection.close()    
    return jsonify({'bookmarks': bookmarks}), 201
      
@server.route('/avaaz/api/v1.0/bookmarks', methods=['POST'])
def create_bookmark():
    if not request.json :
        abort(400)
        
    connection = get_db_connection()
    
    for element in request.json:      
      date = normalize_date(element['date'])
      title = scrub_input(element['title'])
      url = scrub_input(element['uri'])
      
      if (date != -1 and title != -1 and url != -1):
        query = "INSERT INTO data (url, title, date_added) VALUES (%s, %s, %s)"
        params = (url, title, date)
        cursor = connection.cursor()
        result = cursor.execute(query,params)
        connection.commit()
        cursor.close()
        
        bookmark = {
            'title': title,
            'uri': url,
            'date': date  
        }
        bookmarks.append(bookmark)
    
    connection.close()
    
    return jsonify({'bookmarks': bookmarks}), 201
      
@server.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)


if __name__ == "__main__":
    server.run(host='0.0.0.0')
