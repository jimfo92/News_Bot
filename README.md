# news_app

news_app is an app that displays top headlines news.

## Features
  - Register and login.
  - Display recently top headlines news for specific country and category.
  - Display recently news with specific keyword.
  - Bookmark news if user logged in.
  - Paginate results.
  
## Project complexity requirements
  - Query external NewsAPI (https://newsapi.org) in server side.
  - Bookmark news asynchronously with JavaScript.
  - Two models defined one for users and one for bookmarks.
  - Mobile responsiveness with Bootstrap library.
  - Seted up environment variables for api key.
  
## Files & Directories that have been created
  - ***news*** the app that contains all the fuctionality
       - ***static/news*** Holds static files
            - ***index.js*** JavaScript functionality
            - ***styles.css***
       - ***templates/news*** Html files
            - ***index.html*** The html file for display news
            - ***layout.html*** Contain html stracture that all the other html files extends. Also contains navigation bar
            - ***login.html***
            - ***register.html***
            
## To run the application
  - Install ***Django Environ*** for Django enviroment variables with ***pip3 install django-environ***
  - Install the ***Requests*** Module for query external api in the server side with ***pip3 install requests***
  - ***python3 manage.py runserver*** to run the app
