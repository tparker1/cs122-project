# import matplotlib
# matplotlib.use('Agg')

# import the requests and BeautifulSoup modules
import requests
from bs4 import BeautifulSoup
import os
import pandas as pd
import numpy as np
from datetime import datetime
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import matplotlib.patheffects as pe



def get_weekly_data_for_year(year="2023"):
    url = "https://www.boxofficemojo.com/weekly/by-year/"+ year + "/"
    req=requests.get(url)
    content=req.text
    soup=BeautifulSoup(content, 'lxml')
    rows=soup.findAll('tr')

    appended_data = []
    for row in rows:
        data_row = {}
        data = row.findAll('td')
        if len(data) == 0:
            continue
        if len(data[0].findAll('span')) > 0:
            #special weekend
            data_row['Occasion'] = data[0].findAll('span')[0].text
            data_row['Date'] = data[0].findAll('a')[0].text
        else:
            #normal weekend
            data_row['Occasion'] = ""
            data_row['Date'] = data[0].text
        data_row['Top10Gross'] = data[1].text
        data_row['PercentChangeTop10'] = data[2].text
        data_row['OverallGross'] = data[3].text
        data_row['PercentChangeOverall'] = data[4].text
        data_row['Releases'] = data[5].text
        data_row['Number1Release'] = data[6].text
        data_row['Week'] = data[10].text
        appended_data.append(data_row)

    df = clean_pd_weekly_data(appended_data, year)

    # Raise value error if there is no data for the specified year
    if df.shape[0] == 0:
        raise ValueError("No available data for year entered (" + year + ")")
    
    return df





def get_daily_data_for_year(year="2023"):
    # Path to the daily box office data, per year
    url = "https://www.boxofficemojo.com/daily/"+ year+ "/?view=year"

    # get the soup with beautiful soup
    req=requests.get(url)
    content=req.text
    soup=BeautifulSoup(content)
    rows=soup.findAll('tr')
    

    appended_data = []
    for row in rows:
        data_row = {}
        data = row.findAll('td')
        if len(data) == 0:
            continue
        if len(data[0].findAll('span')) > 0:
            #special weekend
            data_row['Occasion'] = data[0].findAll('span')[0].text
            data_row['Date'] = data[0].findAll('a')[0].text
        else:
            #normal weekend
            data_row['Occasion'] = ""
            data_row['Date'] = data[0].text
        if len(data) == 0:
            continue

        data_row['Day'] = data[1].text
        data_row['Day#'] = data[2].text
        data_row['Top10Gross'] = data[3].text
        data_row['PercentChangeYD'] = data[4].text
        data_row['PercentChangeLW'] = data[5].text
        data_row['Releases'] = data[6].text
        data_row['Number1Release'] = data[7].text
        data_row['Gross'] = data[8].text

        appended_data.append(data_row)

        df = clean_pd_daily_data(appended_data, year)

    return df


def convert_to_datetime(date_str, year_str):
    # Combine the date string and the year string
    combined_str = f'{date_str} {year_str}'

    # Convert the combined string into a datetime object
    datetime_obj = datetime.strptime(combined_str, '%b %d %Y')

    return datetime_obj




def clean_pd_weekly_data(appended_data, year):
    df = pd.DataFrame(appended_data, columns = ['Date','Occasion', 'Top10Gross', 'PercentChangeTop10', 'OverallGross', 'PercentChangeOverall', 'Releases', 'Number1Release', 'Week']) 

    df['Date'] = df['Date'].astype(str)
    df['Occasion'] = df['Occasion'].astype(str)
    df['Releases'] = df['Releases'].astype(int)
    df['Number1Release'] = df['Number1Release'].astype(str)
    df['Week'] = df['Week'].astype(int)


    df['OverallGross'] = df['OverallGross'].str.replace('$', '')
    df['OverallGross'] = df['OverallGross'].str.replace(',', '')
    df['OverallGross'] = df['OverallGross'].astype(int)

    df['Top10Gross'] = df['Top10Gross'].str.replace('$', '')
    df['Top10Gross'] = df['Top10Gross'].str.replace(',', '')
    df['Top10Gross'] = df['Top10Gross'].astype(int)

    df['PercentChangeTop10'] = df['PercentChangeTop10'].astype(str)
    df['PercentChangeOverall'] = df['PercentChangeOverall'].astype(str)

    # Datetime is first day of the week
    df['Datetime'] = df['Date'].apply(lambda x: convert_to_datetime(x.split("-")[0], year))
    return df



def clean_pd_daily_data(appended_data, year):
    df = pd.DataFrame(appended_data, columns = ['Occasion', 'Date', 'Day', 'Day#', 'Top10Gross', 'PercentChangeYD', 'PercentChangeLW', 'Releases', 'Number1Release', 'Gross'])

    # fix data types for each column in the dataframe
    df['Day'] = df['Day'].astype(str)
    df['Day#'] = df['Day#'].astype(int)
    df['Releases'] = df['Releases'].astype(int)
    df['Number1Release'] = df['Number1Release'].astype(str)

    df['Gross'] = df['Gross'].str.replace('$', '')
    df['Gross'] = df['Gross'].str.replace(',', '')
    df['Gross'] = df['Gross'].astype(int)

    df['Top10Gross'] = df['Top10Gross'].str.replace('$', '')
    df['Top10Gross'] = df['Top10Gross'].str.replace(',', '')
    df['Top10Gross'] = df['Top10Gross'].astype(int)

    df['PercentChangeYD'] = df['PercentChangeYD'].astype(str)
    df['PercentChangeLW'] = df['PercentChangeLW'].astype(str)

    df['Datetime'] = df['Date'].apply(lambda x: convert_to_datetime(x, year))

    return df



def plot_daily_data_by_year(df, year):
    plt.figure(figsize=(20,10))
    plt.plot(df['Datetime'], df['Gross'])
    plt.title('Daily Gross for ' + str(year))
    plt.xlabel('Date')
    plt.ylabel('Gross')

    # Change the y-axis formatter to display full values
    plt.gca().get_yaxis().set_major_formatter(ticker.FuncFormatter(lambda x, p: format(int(x), ',')))

    plt.xticks(rotation=45)
    plt.savefig('daily_gross.png')


    return 

def plot_weekly_data_by_year(df, year):
    plt.figure(figsize=(20,10))
    plt.plot(df['Datetime'], df['OverallGross'])
    plt.title('Weekly Overall Gross for ' + str(year))
    plt.xlabel('Week Number')
    plt.ylabel('Gross')

    # Change the y-axis formatter to display full values
    plt.gca().get_yaxis().set_major_formatter(ticker.FuncFormatter(lambda x, p: format(int(x), ',')))

    # Use the values in df['Week'] for the xticks
    plt.xticks(df['Datetime'], df['Week'], rotation=45)

    if not os.path.exists('static'):
        # Create the directory if it doesn't exist
            os.makedirs('static')

    plt.savefig(os.path.join('static', 'weekly_gross.png'))

    return 

# given a year, open weekly_csv/YYYY_weekly.csv and return a dataframe
def get_weekly_data_for_year(year):
    filename = "weekly_csv/" + year + "_weekly.csv"
    df = pd.read_csv(filename)
    return df



def get_top_worldwide_movies_df(year = '2023'):
    
    url = 'https://www.boxofficemojo.com/year/world/'+ str(year) + '/'

    # Send a GET request to the URL
    response = requests.get(url)
    
    # Parse the HTML response
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Find the table rows
    table_rows = soup.select('#table div table tr')[1:10]
    
    # Initialize an empty list to store the data
    data = []
    
    # For each row, extract the data and append it to the list
    for row in table_rows:
        rank = row.select('td')[0].text
        release = row.select('td')[1].text
        worldwide = row.select('td')[2].text
        domestic = row.select('td')[3].text
        # percent_domestic = row.select('td')[4].text
        # foreign =  row.select('td')[5].text
        # percent_foreign = row.select('td')[6].text
        
        data.append({
            'Rank': rank,
            'Release': release,
            'worldwide': worldwide,
            'domestic': domestic,
            # 'percent_domestic': percent_domestic,
            # 'foreign': foreign,
            # 'percent_foreign': percent_foreign
        })
    
    # Convert the list of dictionaries to a DataFrame
    df = pd.DataFrame(data)
    
    # Convert the 'Gross' column to an integer
    df['int_worldwide'] = df['worldwide'].str.replace('$', '').str.replace(',', '').astype(int)
    df['readable_worldwide'] = df['int_worldwide'].apply(lambda x: '${:d}'.format(int(x / 1000000)))
    df['int_domestic'] = df['domestic'].str.replace('$', '').str.replace(',', '').astype(int)
    df['readable_domestic'] = df['int_domestic'].apply(lambda x: '${:d}'.format(int(x / 1000000)))

    return df


def get_top_movies_pie_chart(df, year, scope):
    '''Saves a pie chart showing the top 8 movies for a given year, based on gross revenue
    param: df (DataFrame) - the DataFrame to get the top movies from
    param: year (str) - the year to get the top movies for
    param: scope (str) - 'domestic' or 'worldwide'
    return: None
    saves a png file to static/top_8_worldwide_pie.png or static/top_8_domestic_pie.png'''

    assert scope in ['domestic', 'worldwide'], "Scope must be 'domestic' or 'worldwide'"

    # Sort the DataFrame by the appropriate column in descending order and select the top 8 movies
    top_8_movies = df.sort_values(f'int_{scope}', ascending=False).head(8).reset_index(drop=True)


    palette = ['#003f5c', '#2f4b7c', '#665191', '#a05195', '#d45087', '#f95d6a', '#ff7c43', '#ffa600']
    palette.reverse()
    
    # Use the appropriate column for the pie chart data and labels
    data = top_8_movies[f'int_{scope}']
    labels = top_8_movies[f'readable_{scope}']

    plt.figure(figsize=(20,20))

    fig1, ax1 = plt.subplots()

    plt.text(0,0,year, ha='center', va='center', fontsize=20, fontweight='bold')
    
    # Plot the pie chart without percentages
    wedges, _ = ax1.pie(data, colors=palette, startangle=90, shadow=False)

    # Calculate the angles at which to place the labels
    bbox_props = dict(boxstyle="square,pad=0.3", fc="w", ec="k", lw=0.72)
    kw = dict(arrowprops=dict(arrowstyle="-"),
              bbox=bbox_props, zorder=0, va="center")

    for i, p in enumerate(wedges):
        ang = (p.theta2 - p.theta1)/2. + p.theta1
        y = np.sin(np.deg2rad(ang))
        x = np.cos(np.deg2rad(ang))
        horizontalalignment = {-1: "right", 1: "left"}[int(np.sign(x))]
        connectionstyle = "angle,angleA=0,angleB={}".format(ang)
        kw["arrowprops"].update({"connectionstyle": connectionstyle})
        ax1.annotate(labels[i], xy=(x, y), xytext=(1.1*np.sign(x), 1.1*y),
                    horizontalalignment=horizontalalignment, **kw)

    # Draw circle
    centre_circle = plt.Circle((0,0),0.4,fc='white')
    fig = plt.gcf()
    fig.gca().add_artist(centre_circle)


    # Equal aspect ratio ensures that pie is drawn as a circle
    ax1.axis('equal')  

    # Use the 'Release' column for the legend
    legend_labels = top_8_movies['Release']

    # Center the title over the entire image
    plt.figtext(0.5, 1.4, f'{scope.capitalize()} Top Movies by Gross Revenue', ha='center', va='center', fontsize=16, fontweight='bold')
    plt.figtext(0.5, 1.35, r'Gross Revenue $\it{in\ Millions}$', ha='center', va='center', fontsize=12)

    # Move the legend up
    plt.legend(legend_labels, loc='lower center', bbox_to_anchor=(.5, -0.6), shadow=True, ncol=1)
    plt.legend(legend_labels, loc='lower center', bbox_to_anchor=(.5, 1.05), shadow=True, ncol=1)

    # Save the image with an appropriate filename
    plt.savefig(os.path.join('static',f'top_8_{scope}_pie.png'), dpi=600, bbox_inches='tight')
    plt.close()

    return

def run_get_pie_plot(year=2023):
    year = str(year)
    scopes = ['domestic', 'worldwide']
    df = get_top_worldwide_movies_df(year)
    get_top_movies_pie_chart(df, year, scopes[0])
    get_top_movies_pie_chart(df, year, scopes[1])
    return 