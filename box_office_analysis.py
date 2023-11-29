# import the Flask class from the flask module
from flask import Flask

# import the render_template, redirect, and url_for function 
from flask import render_template, redirect, url_for

# import the request variable
from flask import request

import pandas as pd
import os

import get_data as gd
import save_data as sd
import matplotlib
matplotlib.use('qtagg')

# create a Flask object called app
app = Flask(__name__)

# Specify the directory path
directory_path = 'weekly_csv'

year_list = []
end_year = 0
start_year = 0

# Function to update year list
def update_year_list():
    global year_list 
    global end_year, start_year

    year_list.clear()
    # Traverse through files in the directory
    for filename in os.listdir(directory_path):
        # Check if the file is a regular file (not a directory)
        if os.path.isfile(os.path.join(directory_path, filename)):
            # Extract the year from the file name (assuming the year is at the beginning of the file name)
            try:
                year = int(filename.split('_')[0])  # Adjust the splitting logic based on your file naming convention
                year_list.append(year)
            except ValueError:
                print(f"Skipping file {filename} as it does not start with a valid year.")

    year_list.sort(reverse=True)

    if len(year_list) > 0:
        end_year = year_list[0]
        start_year = year_list[-1]
    else:
        end_year = 0
        start_year = 0

# define a route to the home page
# create a home function
@app.route("/")
@app.route("/home")
def home():
    global directory_path
    update_year_list()
    if len(year_list) > 0:
    # create plot for current year
        current_year_csv_path = os.path.join(directory_path, str(end_year) + '_weekly.csv')
        df = pd.read_csv(current_year_csv_path)
        # reverse and reset the order of the dataframe
        df = df.iloc[::-1]
        df = df.reset_index(drop=True)
        gd.plot_weekly_data_by_year(df, end_year)

    return render_template('box_office_home.html', years=year_list, selected_year=end_year)

# define a route to the year page
# add 'GET' to the methods
# create a year function
@app.route("/year", methods=['GET'])
def year():
    global start_year, end_year, directory_path

    # Get the selected year from the query parameters 
    selected_year = int(request.args.get('year', 0))

    # Check if the selected year is within your range of available years
    if selected_year > max(year_list):
        selected_year = end_year
    elif selected_year < min(year_list):
        selected_year = start_year
    
    # create plot for selected year
    current_year_csv_path = os.path.join(directory_path, str(selected_year) + '_weekly.csv')
    df = pd.read_csv(current_year_csv_path)
    # reverse and reset the order of the dataframe
    df = df.iloc[::-1]
    df = df.reset_index(drop=True)
    gd.plot_weekly_data_by_year(df, selected_year)

    return render_template('box_office_home.html', years=year_list, selected_year=selected_year)

# define a route to the pie page
# add 'GET' to the methods
# create a pie function
@app.route("/pie", methods=['GET'])
def pie():
    global start_year, end_year, directory_path

    # Get the selected year from the query parameters 
    selected_year = int(request.args.get('year', 0))

    # Check if the selected year is within your range of available years
    if selected_year > max(year_list):
        selected_year = end_year
    elif selected_year < min(year_list):
        selected_year = start_year

    # create pie chart for selected year
    # current_year_csv_path = os.path.join(directory_path, str(selected_year) + '_weekly.csv')
    # df = pd.read_csv(current_year_csv_path)
    gd.get_top_movies_pie_chart(df, selected_year, 'domestic')

    return render_template('pie_chart.html', years=year_list, selected_year=selected_year)

# define a route to update and download data from BoxOfficeMojo through a button
@app.route('/update_data', methods=['POST'])
def update_data():
    # Your Python function logic goes here
    sd.save_weekly_data_to_csv()
    update_year_list()
    
    print("Data Updated!")

    # Redirect back to homepage after finishing updating
    return redirect(url_for('home'))

# add a main method to run the app
# as a typical Python script
if __name__ == '__main__':
    app.run()