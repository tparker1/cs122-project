# CS 122 Project 1

Box Office Dashboard

## Authors

- Ezra Hsieh
- Tara Parker

## Project Description

Box Office Dashboard is a Python-based web interface to obtain, analyze, and visualize box office data from Box Office Mojo. Box Office Mojo Dashboard will display historical weekly box office weekly data, such as overall gross and #1 releases. Futhermore, Box Office Dashboard will display pie charts of top movies for each week, weighted by their weekly gross.

## Project Outline/Plan

### Interface Plan

Display data with a web interface, created with Flask. Our interface will present a gross profit timeseries, as well as an annual bar chart that visualizes weekly gross with each week's #1 movie. There should be a widget to change the dates shown for the data and to update the data.
This bar chart will have a hyperlinked weeks where you can see a vizualization of the top movies for that week in a pie chart.  
Window 1: Home screen with timeseries and bar chart of gross profits by week.
Window 2: A pie chart of top movies, by weekly gross, for the queried week.
Widget 1: A drop-down menu (TBD) to change the year of data shown on window 1
Widget 2: A go button to reload/update the data shown on window 1
Widget 3: A button to open "detailed data" (window 2) for a chosen week
Widget 4: A button to show "detailed data" for a given movie, like overall gross (TBD)

### Data Collection and Storage Plan

Data will be scraped from [Box Office Mojo(https://www.boxofficemojo.com/date/) website and stored in weekly **tab-delimited** "csv" files.
Data will preserve the format of the scraped data-- that is, we will store the data with a header and data:

| Rank (This week) | LW  | Release Gross          | %± LW       | Theaters | Change | Average | Total Gross | Weeks       | Distributor |
| ---------------- | --- | ---------------------- | ----------- | -------- | ------ | ------- | ----------- | ----------- | ----------- | ------------------ |
| 2                | 1   | The Exorcist: Believer | $14,675,000 | -56.7%   | 3,684  | +21     | $3,983      | $48,601,950 | 2           | Universal Pictures |
|                  |     |                        |             |          |        |         |             |             |             |

### Data Analysis and Visualization Plan

We will use Python's numpy package to calculate trends in the data over time and use matplotlib and/or seaborn to visualize the data as a timeseries, bar and pie charts.
