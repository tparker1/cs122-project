# CS 122 Project: Box Office Dashboard
![Piechart Screenshot](Piescreenshot.png)

## Authors

- Ezra Hsieh
- Tara Parker

## Project Description

Box Office Dashboard (BOD) allows users to visualize trends at the box office through an interactive dashboard. BOD is a Python-based web interface to obtain, analyze, and visualize box office data from Box Office Mojo by IMDB. BOD will allow users to load in the latest and historical box office data to visuazlize temporal trends. BOD will display timeseries and bar charts for weekly box office data, such as overall gross and #1 releases. Futhermore, BOD will allow users to access detailed information by displaying pie charts of top movies for each week, weighted by their weekly gross. By combining data collection, storage, and visualization techniques, BOD aims to streamline the process of accessing and understanding box office trends.

## Project Outline and Plan

### Interface Plan

Display data with a web interface, created with Flask. Our interface will present a gross revenue timeseries, as well as an annual bar chart that visualizes weekly gross with each week's #1 movie. There should be a widget to change the dates shown for the data and to update the data.<br><br>
This bar chart will have a hyperlinked weeks where you can see a vizualization of the top movies for that week in a pie chart.  <br><br>
Window 1: Home screen with timeseries and bar chart of gross revenue by week.<br><br>
Window 2: A pie chart of top movies, by weekly gross, for the queried week.<br><br>
Widget 1: A drop-down menu (TBD) to change the year of data shown on window 1<br><br>
Widget 2: A go button to reload/update the data shown on window 1<br><br>
Widget 3: A button to open "detailed data" (window 2) for a chosen week<br><br>
Widget 4: A button to show "detailed data" for a given movie, like overall gross (TBD)<br><br>

### Data Collection and Storage Plan

Data will be scraped from [Box Office Mojo](https://www.boxofficemojo.com/date/) website and stored in weekly **tab-delimited** "csv" files.
Data will preserve the format of the scraped data-- that is, we will store the data with a header and data as shown below:

| Rank (This week) | LW  | Release                | Gross       | %± LW  | Theaters | Change | Average | Total Gross | Weeks | Distributor        |
| ---------------- | --- | ---------------------- | ----------- | ------ | -------- | ------ | ------- | ----------- | ----- | ------------------ |
| 2                | 1   | The Exorcist: Believer | $14,675,000 | -56.7% | 3,684    | +21    | $3,983  | $48,601,950 | 2     | Universal Pictures |
|                  |     |                        |             |        |          |        |         |             |       |                    |

### Data Analysis and Visualization Plan

BOD will utilize matplotlib and seaborn to create standard visualizations, such as line charts for depicting the trends in box office gross over time and bar charts for comparing the performance of different movies.
Window 1 will use a line chart and a bar graph to visualize gross trends of weekly box office data. Window 2 will use a pie chart to vizualize movies from that week, weighted by their gross for that week.

<!-- Other analysis and visualization plan if we have the time:
Comparative Analysis: BOD will visualize key metrics between different movies to facilitate a straightforward understanding of their relative performance. This will involve creating side-by-side bar charts or tables that highlight the differences in metrics such as total gross or average weekly gross between selected movies. -->
