import re, datetime
from flask import jsonify, abort

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
  
def getquery(title, data):
   if len(data) == 0:
    abort(400)
   return jsonify({title: data}), 201
	