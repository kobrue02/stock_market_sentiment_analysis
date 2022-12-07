from dataframes.scores_for_source import ScoreChart
from datetime import date, timedelta

from visualizer.main import Visualizer
from dataframes.data_collecting.auxilliary import calc_day_after, string_to_date

import pandas as pd
import time
import os

from os.path import exists


class DataFrame:
    def __init__(self, query, start_date, end_date, sources):
        self.query = query
        self.start = start_date
        self.end = end_date
        self.sources = sources
        self.dates = self.list_of_dates()   # list of all dates within timeframe (start-end), in D-M-Y format
        self.vis = Visualizer(start_date, end_date, query)
        self.dataframe = self.convert_to_pandas_df()

    def list_of_dates(self):
        """ generates a list of dates between two dates """

        sdate = string_to_date(self.start)
        edate = string_to_date(self.end)

        timestamps = pd.date_range(sdate, edate-timedelta(days=1), freq='d').to_list()   # creates list of timestamps
        date_list = [str(stamp.date().strftime("%d-%m-%Y")) for stamp in timestamps]   # extract date in D-M-Y format

        return date_list

    def get_reddit_score(self, score):
        return score.rsent

    def get_stocktwits_score(self, score):
        return score.stsent

    def get_twitter_score(self, score):
        return score.twsent

    def get_label(self, score):
        return score.label

    def get_volume(self, score):
        return score.get_volume()

    def get_price(self, score):
        return score.get_close_price()

    def run_through_datelist(self):
        """ iterates through the date list to get the SP score for each day """
        date_score_dict = {}
        for start_date in self.dates:
            end_date = calc_day_after(start_date)   # to get the comments of day X, do X-M-Y to (X+1)-M-Y
            score = ScoreChart(self.query, start_date, end_date, self.sources)
            date_score_dict[start_date] = [
                                           self.get_reddit_score(score),
                                           self.get_stocktwits_score(score),
                                           self.get_twitter_score(score),
                                           self.get_volume(score),
                                           self.get_label(score),
                                           self.get_price(score)
                                                                ]
            time.sleep(1.5)   # this makes sure the pushshift.io API is ready for the next request
        return date_score_dict

    def convert_to_pandas_df(self):
        """ simple method to turn the dictionary generated by the run_through_datelist() function into a dataframe """
        self.vis.get_data()
        data = self.run_through_datelist()   # returns dict
        frame = self._convert_to_pandas_df(data)
        return pd.DataFrame.from_dict(frame)

    def _convert_to_pandas_df(self, data):
        date_col = data.keys()  # get dates
        r_col = [list_of_values[0] for list_of_values in data.values()]  # get reddit SP scores
        t_col = [list_of_values[1] for list_of_values in data.values()]  # get stocktwits SP scores
        tw_col = [list_of_values[2] for list_of_values in data.values()]  # get twitter SP scores
        vol_col = [list_of_values[3] for list_of_values in data.values()]  # get volume
        lab_col = [list_of_values[4] for list_of_values in data.values()]  # get label
        price_col = [list_of_values[5] for list_of_values in data.values()]  # get price
        frame = {"Date": date_col,
                 "Reddit Sentiment Score": r_col,
                 "StockTwits Sentiment Score": t_col,
                 "Twitter Sentiment Score": tw_col,
                 "Volume": vol_col,
                 "General Sentiment": lab_col,
                 "Price": price_col}
        return frame

    def _save_to_csv(self, file):
        file_name = f'output/{self.query}.csv'
        if not exists(file_name):
            file.to_csv(file_name, index=False, sep=";", decimal=",")  # default decimal separator is .
        else:
            old_data = pd.read_csv(file_name, sep=";", decimal=",")  # get the data from the existing csv
            new_data = self.dataframe
            merged_data = pd.concat([old_data, new_data], ignore_index=True)   # and merge it with the new data
            os.remove(file_name)   # sometimes there are permission errors when trying to append to a CSV
            merged_data.to_csv(file_name, index=False, sep=";", decimal=",")

    def save_to_csv(self):
        file = self.dataframe
        os.makedirs("output", exist_ok=True)
        self._save_to_csv(file)

