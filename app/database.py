import pymysql.cursors, os

class Database:
  my_db = my_cursor = None
  
  def __init__(self):
    global my_db, my_cursor
    try:
      my_db = pymysql.connect(host=os.environ.get('MYSQL_HOST'),
                                   user=os.environ.get('MYSQL_USER'),
                                   password=os.environ.get('MYSQL_PWD'),
                                   database=os.environ.get('MYSQL_DB'))
    except Exception as e: 
     return e
    else:
      my_cursor = my_db.cursor()
  
  def __del__(self):
        my_db.close()
          
  def fetchall(self, query, params):    
     cursor = my_db.cursor()
     if (params != ""):
       try:
        cursor.execute(query, (params))
        rows=cursor.fetchall()
        cursor.close()
       except Exception as e:
        return e
     else:
      try:
        cursor.execute(query)
        rows=cursor.fetchall()
        cursor.close()
      except Exception as e:
       return e 
     return rows
     
  def fetchone(self, query, params):
    cursor = my_db.cursor()
    try: 
      cursor.execute(query, (params))
      row=cursor.fetchone()
      cursor.close()
    except Exception as e:
      return e
    return row
    
  def insert(self, query, params):
    cursor = my_db.cursor()
    try:
      result=cursor.execute(query, (params))
      my_db.commit()
      cursor.close()
    except Exception as e:
      return e
    return result