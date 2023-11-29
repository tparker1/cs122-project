import pandas as pd
import os

import get_data as gd

def save_weekly_data_to_csv():
    # Identify the years with box office data
    end_year = 1982

    # Scrape all weekly data from 1982 until most recent year
    while True:
        if not os.path.exists('weekly_csv'):
        # Create the directory if it doesn't exist
            os.makedirs('weekly_csv')

        try:
            print('Getting data from year', end_year)
            df = gd.get_weekly_data_for_year(str(end_year))
        # break loop when data is not available for this year
        except ValueError:
            break

        csv_filename = str(end_year) + '_weekly.csv'
        df.to_csv(os.path.join('weekly_csv', csv_filename), index=True)
        # data_list.append(df)

        end_year += 1

    end_year -= 1



