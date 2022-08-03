import re, datetime, logging
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
        logging.debug('%s raised an error: invalid date. Skipping data.',  date)
        date = -1
       if match is not None:
        logging.debug('Date confirmed: %s',  date)
    else: 
      date = datetime_object.strftime("%Y-%m-%d")
      logging.debug('Date confirmed: %s',  date)
  else:
   date = datetime_object.strftime("%Y-%m-%d")
   logging.debug('Date confirmed: %s',  date)              
  return date

def scrub_input(data):
  if (data == "null" or data == "" or data is None):
    logging.debug('%s raised an error: invalid data. Skipping data.',  data)
    data = -1
  return data
  
def getquery(title, data):
   if len(data) == 0:
    abort(400)
   return jsonify({title: data}), 200
	