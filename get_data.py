import requests
from bs4 import BeautifulSoup

import os
import pandas as pd
import numpy as np

from datetime import datetime as dt
from datetime import datetime

import time

import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import matplotlib.patheffects as pe
import matplotlib
matplotlib.use('qtagg')

def get_weekly_data_for_year(year="2023"):
    '''Returns a dataframe of weekly data for a given year'''

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


def convert_to_datetime(date_str, year_str):
    '''Converts a date string and a year string into a datetime object'''

    combined_str = f'{date_str} {year_str}'
    datetime_obj = datetime.strptime(combined_str, '%b %d %Y')

    return datetime_obj


def clean_pd_weekly_data(appended_data, year):
    '''Cleans the weekly data and returns a dataframe'''

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


def toYearFraction(date):
    '''Converts a datetime object to a year fraction'''
    def sinceEpoch(date): # returns seconds since epoch
        return time.mktime(date.timetuple())
    s = sinceEpoch

    year = date.year
    startOfThisYear = dt(year=year, month=1, day=1)
    startOfNextYear = dt(year=year+1, month=1, day=1)

    yearElapsed = s(date) - s(startOfThisYear)
    yearDuration = s(startOfNextYear) - s(startOfThisYear)
    fraction = yearElapsed/yearDuration

    return date.year + fraction

def calculate_trendline(df):
    '''Calculates the trendline for the overall gross'''

    df['Datetime2'] = pd.to_datetime(df['Datetime'])
    df['dec_yr'] = df['Datetime2'].apply(lambda x: toYearFraction(x))

    # Fit a line to the data
    z = np.polyfit(df['dec_yr'], df['OverallGross'], 1)
    p = np.poly1d(z)

    trendline = p(df['dec_yr'])
    dates = df['dec_yr']
    slope = z[0]

    return trendline, slope


def plot_weekly_data_by_year(df, year):
    '''Plots the weekly data for a given year as a bar chart with a trendline and saves the plot as a png file'''

    palette = ['#003f5c', '#2f4b7c', '#665191', '#a05195', '#d45087', '#f95d6a', '#ff7c43', '#ffa600', '#001f2e']

    plt.figure(figsize=(20,10))
    plt.bar(df['Datetime'], df['OverallGross'], color=palette[1], edgecolor=palette[0], linewidth=2.5, alpha=0.9, width=1)

    # NEW CODE
    trendline, slope = calculate_trendline(df)
    # Plot the trendline
    sign = '+' if np.sign(slope) > 0 else '-'
    label=f'Overall Trend: {sign}${abs(slope):,.0f}'
    plt.plot(df['Datetime'], trendline, 'grey', linestyle='dashed', label=label)

    
    plt.xlabel('Week', fontsize=22, labelpad=20, color=palette[-1])
    plt.ylabel('Gross\n$_{(in\, \$MM)}$', fontsize=22, labelpad=20, color=palette[-1])

    plt.gca().get_yaxis().set_major_formatter(ticker.FuncFormatter(lambda x, p: format(int(x/1000000), ',')))

    plt.xticks(df['Datetime'], df['Week'], rotation=0, fontsize=14, color=palette[-1])

    plt.ylim(0, df['OverallGross'].max() * 1.1)
    
    for label in plt.gca().xaxis.get_ticklabels()[::2]:
        label.set_visible(False)

    yticks = plt.yticks()[0]
    plt.yticks(yticks[:], fontsize=14, color=palette[-1])

    if not os.path.exists('static'):
        os.makedirs('static')

    plt.legend(loc='upper right', fontsize=14, frameon=False)

    plt.subplots_adjust(top=0.9)  # Adjust the top margin
    plt.savefig(os.path.join('static', 'weekly_gross.png'), dpi=300, bbox_inches='tight', transparent=True)

    return



def get_top_worldwide_movies_df(year = '2023'):
    '''Returns a DataFrame of the top movies for a given year'''
    url = 'https://www.boxofficemojo.com/year/world/'+ str(year) + '/'

    # request and parse
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    table_rows = soup.select('#table div table tr')[1:]
    
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
    

    df = pd.DataFrame(data)    
    # convert the gross strings to integers
    df['worldwide'] = df['worldwide'].str.replace('-', '0')
    df['int_worldwide'] = df['worldwide'].str.replace('$', '').str.replace(',', '').astype(np.int64)
    df['readable_worldwide'] = df['int_worldwide'].apply(lambda x: '${:d}'.format(np.int64(x / 1000000)))
    df['domestic'] = df['domestic'].str.replace('-', '0')
    df['int_domestic'] = df['domestic'].str.replace('$', '').str.replace(',', '').astype(np.int64)
    df['readable_domestic'] = df['int_domestic'].apply(lambda x: '${:d}'.format(np.int64(x / 1000000)))

    return df


def get_top_movies_pie_chart(df, year, scope):
    '''Saves a pie chart showing the top 8 movies for a given year, based on gross revenue
    param: df (DataFrame) - the DataFrame to get the top movies from
    param: year (str) - the year to get the top movies for
    param: scope (str) - 'domestic' or 'worldwide'
    return: None
    saves a png file to static/top_8_worldwide_pie.png or static/top_8_domestic_pie.png'''


    assert scope in ['domestic', 'worldwide'], "Scope must be 'domestic' or 'worldwide'"

    # Sort the DataFrame by the scope column and get the top 8 
    top_8_movies = df.sort_values(f'int_{scope}', ascending=False).head(8).reset_index(drop=True)

    data = top_8_movies[f'int_{scope}']
    labels = top_8_movies[f'readable_{scope}']

    palette = ['#003f5c', '#2f4b7c', '#665191', '#a05195', '#d45087', '#f95d6a', '#ff7c43', '#ffa600']
    palette.reverse()

    plt.figure(figsize=(20,20))

    fig1, ax1 = plt.subplots()

    plt.text(0,0,year, ha='center', va='center', fontsize=20, fontweight='bold')
    
    # plot pie chart without percentages
    wedges, _ = ax1.pie(data, colors=palette, startangle=90, shadow=False)

    # calculate the angles for the labels
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

    # donut circle
    centre_circle = plt.Circle((0,0),0.4,fc='white')
    fig = plt.gcf()
    fig.gca().add_artist(centre_circle)

    # keep pie as a circle 
    ax1.axis('equal')  

    # get the movie name for the legend
    legend_labels = top_8_movies['Release']


    plt.figtext(0.5, 1.4, f'{scope.capitalize()}', ha='center', va='center', fontsize=16, fontweight='bold')
    plt.figtext(0.5, 1.35, r'Gross Revenue $\it{in\ Millions}$', ha='center', va='center', fontsize=12)

    # move the legend up
    plt.legend(legend_labels, loc='lower center', bbox_to_anchor=(.5, -0.6), shadow=True, ncol=1)
    plt.legend(legend_labels, loc='lower center', bbox_to_anchor=(.5, 1.05), shadow=True, ncol=1)

    plt.savefig(os.path.join('static',f'top_8_{scope}_pie.png'), dpi=600, bbox_inches='tight', transparent=True)
    plt.close()

    return

def run_get_pie_plot(year=2023):
    '''Runs the get_top_movies_pie_chart function for both domestic and worldwide scope'''
    year = str(year)
    scopes = ['domestic', 'worldwide']
    df = get_top_worldwide_movies_df(year)
    get_top_movies_pie_chart(df, year, scopes[0])
    get_top_movies_pie_chart(df, year, scopes[1])
    return 