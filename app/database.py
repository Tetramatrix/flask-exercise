import pymysql.cursors, os, sys

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
      try:
        logging.error("Exception occurred", exc_info=True)
        sys.exit("Fatal database error! Program aborted:"+str(e))
      except Exception as e:
        logging.error("Exception occurred", exc_info=True)
        sys.exit("Fatal database error! Program aborted:"+str(e))       
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
        logging.error("Exception occurred", exc_info=True)
        return e
     else:
      try:
        cursor.execute(query)
        rows=cursor.fetchall()
        cursor.close()
      except Exception as e:
       logging.error("Exception occurred", exc_info=True)
       return e 
     
     if (rows == None):
      rows = ()
     return rows
     
  def fetchone(self, query, params):
    cursor = my_db.cursor()
    try: 
      cursor.execute(query, (params))
      row=cursor.fetchone()
      cursor.close()
    except Exception as e:
      logging.error("Exception occurred", exc_info=True)
      return e
      
    if (row == None):
      row = ()
    print (row)     
    return row
    
  def insert(self, query, params):
    cursor = my_db.cursor()
    try:
      result=cursor.execute(query, (params))
      my_db.commit()
      cursor.close()
    except Exception as e:
      logging.error("Exception occurred", exc_info=True)
      return e
    return result