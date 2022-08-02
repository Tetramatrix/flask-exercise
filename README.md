# Avaaz Engineering Exercise

Thanks for your interest in joining Avaaz! We are thrilled that you considered working with us.

Your task is to build a small application that allows a user to search data using several filters:
- Date range (after, before, and between)
- Title (text search, case-insensitive, full or partial matches)
- URL (full or partial matches)

The following things are provided in this repository:
- The destination database table (see `database/initdb.d/setup.sql`)
- A bare bones Flask app (see `app/server.py`)

**We recommend you spend a maximum of two hours on it, and don't worry if you didn’t cover all of the requirements.**

## Instructions

- Use Python and Flask for your application
- The application ingests JSON source data (see the input folder)
- The application stores valid data and normalized datetimes in the provided database
- The application allows searching the data through an API endpoint (using the filters described above)

Submit your solution by sending a zipped file via email to your Avaaz recruiting contact (you can reply to your existing email thread).


=====================================================================================================================

## Solution

## Installation

1. Unpack the .zip-Archive to your development machine or navigate to github (https://github.com/Tetramatrix/flask-exercise/tree/contribution) and clone with git. 

2. Open a console and navigate to the folder "flask-exercise".
   Run virt\Scripts\activate.ps1 in Powershell or (source virt\Scripts\activate in Linux).
   Your command prompt should change to (virt){path}\flask-exercise>. 
  
3. Then edit the file .env to match your sql-database and save it:
 		
 		MYSQL_HOST=
		MYSQL_DB=
		MYSQL_USER=
		MYSQL_PWD=

3.1 If you install from git you need to add these lines to the file .env:

		FLASK_APP=app\server
		FLASK_ENV=development

4. To start the application type "python -m flask run" and press return. Example output:

 * Serving Flask app 'app\\server' (lazy loading)
 * Environment: development
 * Debug mode: on
 * Running on http://127.0.0.1:5000 (Press CTRL+C to quit)
 * Restarting with stat
 * Debugger is active!
 * Debugger PIN: 869-370-679

5. Open a browser window and navigate to http://127.0.0.1:5000. It loads a page with the content "Welcome to Flask-Avaaz!". Congrats!

## Tutorial 

1. The application has 5 REST-API endpoints:
	
1.1 [get]   /avaaz/api/v1.0/bookmarks   							retrieve all bookmarks      
    [post]  /avaaz/api/v1.0/bookmarks  								create bookmarks from a json source
 
1.2 [get]   /avaaz/api/v1.0/bookmarks/{id}  					retrieve a bookmark by id
 
1.3 [get]   /avaaz/api/v1.0/bookmarks/title/{title} 	retrieve a bookmark by title (fulltext search)
 
1.4 [get]   /avaaz/api/v1.0/bookmarks/url/{url}  			retrieve a bookmark by url (fulltext search)	 	   

1.5 [get]   /avaaz/api/v1.0/bookmarks/date?start={datetime}&end={datetime} 	retrieve a list of bookmarks by date (after, befor, 		 																																					between)
   	
   	  
2.1 Example to retrieve all bookmarks

			Open a browser window and copy and paste into the address bar:
			http://localhost:5000/avaaz/api/v1.0/bookmarks

2.1.1 Example to import bookmarks from a json source

			This endpoint is password protected because it can add bookmarks to the database! I have included a default user "admin" and password "password" in the application. You should use it to authenticate for this endpoint. For example: 
			
			Open a browser console and copy and paste the code and press return:
			
			fetch('http://localhost:5000/avaaz/api/v1.0/bookmarks', {
			  method: 'POST',
			  headers: { 'Authorization': 'Basic ' + btoa('admin:password') },
			  body: JSON.stringify([
			    {
			      "title": "A arte de atingir seus objetivos simplesmente",
			      "uri": "http://matthews-espinoza.com/",
			      "date": "2014-03-08T15"
			    },
			    {
			      "title": "L'avantage d'innover \u00e0 l'\u00e9tat pur",
			      "uri": "http://www.hood.net/about.html",
			      "date": "March 30 1985"
			    },   
			    {
			      "title": "L'assurance de rouler \u00e0 sa source",
			      "uri": "https://thierry.com/register/",
			      "date": "05 Jan 1972"
			    }] )  
			})
			.then(res => res.json()).then(console.log);
			
			The application skips bookmarks with invalid title and url, e.g. empty title and invalid url. 
			If the request is succesful a list of the saved bookmarks and a HTTP 200 response code is returned.
			In all other cases an empty list and a HTTP 200 response code is returned (for example an empty database).
			
2.2   Example to retrieve a bookmark by id
		
			Open a browser window and copy and paste into the address bar:
		  http://localhost:5000/avaaz/api/v1.0/bookmarks/2
		  or any number after ...bookmarks/
		  If the request is succesful the bookmark and a HTTP 200 response code is returned.
		  In all other cases a HTTP 404 response code is returned.
		  		  	
2.3   Example to retrieve a bookmark by title

	   	Open a browser window and copy and paste into the address bar:
	   	http://localhost:5000/avaaz/api/v1.0/bookmarks/title/ta
	   	or any string after ...title/
	   	If the request is succesful a list of the bookmarks and a HTTP 200 response code is returned.
	   	In all other cases a HTTP 404 response code is returned.
	   	
2.4   Example to retrieve a bookmark by url

	   	Open a browser and window copy and paste into the address bar:
	   	http://localhost:5000/avaaz/api/v1.0/bookmarks/url/am	   	
			or any string after ...url/
	   	If the request is succesful a list of the bookmarks and a HTTP 200 response code is returned.
	   	In all other cases a HTTP 404 response code is returned.
	   	
2.5 Example to retrieve a bookmark by date

		There are 3 posibilities: after, before and between. The application accepts the following 2 datetime formats:
		YYYY-MM-DDThh:mm:ss.s and YYYY-MM-DDThh:mm:ss.sTZD, e.g 1920-06-01T00:00:00 or with TZ then url_encoded: 1917-08-07T12%3A09%3A23.555%2B01%3A00
	
2.5.1 Example to retrieve a list of bookmarks after a specific date:

		Open a browser window and copy and paste into the address bar:
		http://localhost:5000/avaaz/api/v1.0/bookmarks/date?start=1920-06-01T00:00:00
		If the request is succesful a list of the bookmarks and a HTTP 200 response code is returned. An empty list is returned if the result is empty. 
		In case the date format is wrong a HTTP 422 response code is returned.
		
2.5.2 Example to retrieve a list of bookmarks before a specific date:		
		
		Open a browser window and copy and paste into the address bar:
		http://localhost:5000/avaaz/api/v1.0/bookmarks/date?end=2010-12-01T00:00:00
	  If the request is succesful a list of the bookmarks and a HTTP 200 response code is returned. An empty list is returned if the result is empty. 
		In case the date format is wrong a HTTP 422 response code is returned.
		
2.5.3 Example to retrieve a list bookmarks between 2 specific dates:

		Open a browser window and copy and paste into the address bar:
		http://localhost:5000/avaaz/api/v1.0/bookmarks/date?start=1950-03-03T00:00:00&end=2020-03-03T00:00:00
 		If the request is succesful a list of the bookmarks and a HTTP 200 response code is returned. An empty list is returned if the result is empty. 
	  In case the date format is wrong a HTTP 422 response code is returned.
	  
3. Quit Flask and virtual environment

3.1 Press CTRL+C to quit Flask and type deactivate and press return to quit 