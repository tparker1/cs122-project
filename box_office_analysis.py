# import the Flask class from the flask module
from flask import Flask

# import the render_template function
from flask import render_template

# import the request function
from flask import request

# import csv module
import csv

# import pandas
import pandas as pd

# create a Flask object called app
app = Flask(__name__)

# Read data from CSV file and store it in a list of dictionaries
# with open('weekly.csv') as file:
#     csv_reader = csv.DictReader(file)
#     weekly = list(csv_reader)

# define a route to the home page
# create a home function
@app.route("/")
@app.route("/home")
def home():
    return render_template('box_office_home.html')

# define a route to the year page
# add 'GET' to the methods
# create a year function
@app.route("/year", methods=['GET'])
def year():
    pass

# define a route to the pie page
# add 'GET' to the methods
# create a pie function
@app.route("/pie", methods=['GET'])
def year():
    pass

# add a main method to run the app
# as a typical Python script
if __name__ == '__main__':
    app.run()