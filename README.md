# news_app
news_finder is an app that displays top news headlines.

## Features
  - Register and login.
  - Display recently top headlines for specific country and category.
  - Display recently news with specific keyword.
  - Bookmark news if user logged in.
  - Paginate results.
  
## Project complexity requirements
  - Query external NewsAPI (https://newsapi.org) in server side.
  - Bookmark news asynchronously with JavaScript.
  - Two models defined one for users and one for bookmarks.
  - Mobile responsiveness with Bootstrap library.
  - Seted up environment variables for api key.
            
## Install
  - Install ***Django Environ*** for Django enviroment variables with `pip install django-environ`
  - Install the ***Requests*** module for query external api in the server side with `pip install requests`
  
  - In your terminal, `cd` into the project directory.
  ```
  python manage.py makemigrations
  python manage.py migrate
  
  python manage.py runserver
  ```
