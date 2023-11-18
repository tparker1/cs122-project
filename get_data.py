# import the requests and BeautifulSoup modules
import requests
from bs4 import BeautifulSoup
import os
import pandas as pd
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

def get_top_movies_for_year_pie_chart(year='2023'):
    '''Saves a pie chart showing the top 8 movies for a given year, based on the number of weeks at #1
    param: year (str) - the year to get the top movies for. default is 2023
    return: None
    saves a png file to static/top_8_movies_pie.png'''

    df = get_weekly_data_for_year(year)
    top_8_movies = df['Number1Release'].value_counts().head(8)

    palette = ['#003f5c', '#2f4b7c', '#665191', '#a05195', '#d45087', '#f95d6a', '#ff7c43', '#ffa600']
    palette.reverse()

    labels = top_8_movies.index
    data = top_8_movies

    plt.figure(figsize=(20,20))

    fig1, ax1 = plt.subplots()

    # Plot the pie chart
    ax1.pie(data, colors=palette, autopct=lambda p: '{:.0f}'.format(p * sum(data) / 100), pctdistance=0.7, startangle=90, 
            textprops={'fontsize': 16, 'color': 'white', 'alpha': 1, 'path_effects': [pe.withStroke(linewidth=2, foreground="black", alpha = 0.85)]}, 
            shadow=False)

    # Draw circle
    centre_circle = plt.Circle((0,0),0.4,fc='white')
    fig = plt.gcf()
    fig.gca().add_artist(centre_circle)

    # Equal aspect ratio ensures that pie is drawn as a circle
    ax1.axis('equal')  

    # Add title and subtitle
    plt.suptitle(year + ' Top Movies', fontsize=16, fontweight='bold', y=0.95)
    plt.title('Weeks at #1', fontsize=12)

    plt.tight_layout()
    plt.legend(labels, loc='upper left', bbox_to_anchor=(0.85, 1.025), shadow=True, ncol=1)
    plt.savefig(os.path.join('static','top_8_movies_pie.png'), dpi=600, bbox_inches='tight')
    plt.close()

    return 