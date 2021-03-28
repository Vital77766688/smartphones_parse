# smartphones_parse

This project is meant to learn scrapy frame work.

It uses scrapy framework for scrapping smartphone data from online stores and also uses flask to display results in web.

Need to download selenium driver (chromedriver for instance). 
Add folder with driver to PATH variable.

export PATH={path_to_folder_with_driver}:$PATH

If driver is other than chrome, change settings.

Before running web server need export variables
export FLASK_APP=application.py
export FLASK_ENV=development

Then execute command: flask run, this will run development server.