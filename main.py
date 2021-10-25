
from datetime import datetime, timedelta
import sys
import csv
import pandas as pd

# this function calculates from a csv file what is the most trendy image in a given time range for a given measure
# make a dictionary for each media url with its count
# get max count and related media url

# f(x) visual representation
trend_image_urls = []
# f(x) value
trend_image_ranks = []


def get_trend_image_per_range(csv_path, col_time_header, col_url_header, col_rank_header, date_start, date_end):
    dict_temp = {}
    print('Get trend image per time slots')
    # reading csv file
    df = pd.read_csv(csv_path)

    # only keep day in date format
    # CAUTION: needs to be modified for other data format
    df[col_time_header] = df[col_time_header].apply(
        lambda t: datetime.strptime(t.split('T')[0], '%Y-%m-%d'))

    # TODO:access row correctly; row[index] instead row[key]

    # get all rows where date is in between start date and end date
    for index, row in df.iterrows():
        # if date in a row is in between valid range
        if (date_start <= df[col_time_header][index] <= date_end):
            # update rank value for a given media url
            url = df[col_url_header][index]
            # if url has not been stored yet, save its rank value
            if url not in dict_temp:
                dict_temp[url] = df[col_rank_header][index]
            # otherwise add rank value
            else:
                dict_temp[url] = dict_temp[url] + df[col_rank_header][index]

    # can optionally also be returned as top-of-lists
    trend_image_url = max(dict_temp, key=dict_temp.get)
    trend_image_url_rank = max(dict_temp.values())
    print(trend_image_url)
    print(trend_image_url_rank)
    return trend_image_url, trend_image_url_rank


def get_trend_images(dates, csv_path, col_time_header, col_url_header, col_rank_header, date_start, date_end):
    # set start date to original start
    start = date_start
    for i in range(0, len(dates)):
        end = dates[i]
        url, rank = get_trend_image_per_range(
            csv_path, col_time_header, col_url_header, col_rank_header, start, end)
        trend_image_urls.append(url)
        trend_image_ranks.append(rank)
        start = dates[i]
    # set final end date to original end
    end = date_end
    # if there are no dates in between, get trend image and rank for one range
    url, rank = get_trend_image_per_range(
        csv_path, col_time_header, col_url_header, col_rank_header, start, end)
    trend_image_urls.append(url)
    trend_image_ranks.append(rank)


def plot(csv_path, col_time_header, col_url_header, col_rank_header, axis_x_label, axis_y_label, date_start, date_end, result_dir):
    print('The plotting is going to start! \nYou are going to plot your images by {a}, ranked after {b}, ranging from {c} until {d}.'.format(
        a=axis_x_label, b=axis_y_label, c=date_start.strftime('%Y-%m-%d'), d=date_end.strftime('%Y-%m-%d')))
    print('By default the results are going to be stored in the directory {i}.'.format(
        i=result_dir))

    if axis_x_label == 'year':
        dates = pd.date_range(date_start, date_end, freq='y')
        get_trend_images(dates, csv_path, col_time_header,
                         col_url_header, col_rank_header, date_start, date_end)

    elif axis_x_label == 'month':
        dates = pd.date_range(date_start, date_end, freq='m')
        get_trend_images(dates, csv_path, col_time_header,
                         col_url_header, col_rank_header, date_start, date_end)

    elif axis_x_label == 'week':
        dates = pd.date_range(date_start, date_end, freq='w')
        get_trend_images(dates, csv_path, col_time_header,
                         col_url_header, col_rank_header, date_start, date_end)

    elif axis_x_label == 'day':
        dates = pd.date_range(date_start, date_end, freq='d')
        get_trend_images(dates, csv_path, col_time_header,
                         col_url_header, col_rank_header, date_start, date_end)

    else:
        print('No valid x label input: needs to be day, week, month or year')
        return


def main():
    args = sys.argv[1:]
    result_dir = 'results/'

    if len(args) == 0:
        print('Welcome to the image trendlines tool!')
        while True:
            csv_path = input(
                'Please enter the absolute path of the csv file you want to analyse and plot. \n')
            if csv_path.endswith('.csv'):
                print('Thanks! The csv path you entered is: {i}.'.format(
                    i=csv_path))
                break
            else:
                print(
                    'Something is wrong with your path. The format seems to be invalid for csv files.')
        col_time_header = input(
            'Please copy and paste the column header for the column which holds timestamp information. \n')
        print('Thanks! The timestamp header you entered is: {i}.'.format(
            i=col_time_header))
        col_url_header = input(
            'Please copy and paste the column header for the column which holds image url information. \n')
        print('Thanks! The url header you entered is: {i}.'.format(
            i=col_url_header))
        col_rank_header = input(
            'Please copy and paste the column header for the column which you want to rank your images after, e.g. retweets. \n')
        print('Thanks! The rank header you entered is: {i}.'.format(
            i=col_rank_header))
        axis_y_label = input(
            'Please enter a term describing what you rank your images after. \n')
        print('Thanks! You want to rank your images after {i}.'.format(
            i=axis_y_label))
        date_start = datetime.strptime(input(
            'From which date on do you wish to plot your trendline? Please indicate the date in following format: DD-MM-YYYY \n'), '%Y-%m-%d')
        print('Thanks! Your image trendline will be plotted from the following date: {i}.'.format(
            i=date_start.strftime('%Y-%m-%d')))
        date_end = datetime.strptime(input(
            'Until which date do you wish to plot your trendline? Please indicate the date in following format: DD-MM-YYYY \n'), '%Y-%m-%d')
        print('Thanks! Your image trendline will be plotted until the following date: {i}.'.format(
            i=date_end.strftime('%Y-%m-%d')))
        axis_x_label = input(
            'Finally, choose which time measure to apply for your trendline by typing one of the following options: \n year - month - week - day \n')
        plot(csv_path, col_time_header, col_url_header, col_rank_header,
             axis_x_label, axis_y_label, date_start, date_end, result_dir)

    elif len(args) == 8:
        plot(args[0], args[1], args[2], args[3],
             args[4], args[5], datetime.strptime(args[6], '%Y-%m-%d'), datetime.strptime(args[7], '%Y-%m-%d'), result_dir)


if __name__ == "__main__":
    main()
