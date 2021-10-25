
from datetime import date, datetime, timedelta
import sys
import csv
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.offsetbox import OffsetImage, AnnotationBbox
from collections import OrderedDict
import urllib.request
import os
from PIL import Image

# y
trend_image_ranks = []
# f(x) visual representation
trend_image_urls = []
# image size
image_width = 100


def get_trend_image_per_range(csv_path, col_time_header, col_url_header, col_rank_header, date_start, date_end):
    dict_temp = {}
    print('Get trend image per time slots')
    # reading csv file
    df = pd.read_csv(csv_path)

    # only keep day in date format
    # CAUTION: needs to be modified for other data format
    df[col_time_header] = df[col_time_header].apply(
        lambda t: datetime.strptime(t.split('T')[0], '%Y-%m-%d'))

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


def get_plot_image(path):
    img = Image.open(path)
    wpercent = (image_width/float(img.size[0]))
    image_height = int((float(img.size[1])*float(wpercent)))
    img = img.resize((image_width, image_height), Image.ANTIALIAS)
    img.save(path)
    return OffsetImage(plt.imread(path))


def plot(csv_path, col_time_header, col_url_header, col_rank_header, axis_x_label, axis_y_label, date_start, date_end, result_dir, image_dir):
    print('The plotting is going to start! \nYou are going to plot your images by {a}, ranked after {b}, ranging from {c} until {d}.'.format(
        a=axis_x_label, b=axis_y_label, c=date_start.strftime('%Y-%m-%d'), d=date_end.strftime('%Y-%m-%d')))
    print('By default the results are going to be stored in the directory {i}.'.format(
        i=result_dir))

    # x axis
    trend_image_time_blocks = []
    # labels for x axis
    time_block_labels = []
    # paths of locally stored images
    trend_image_local_paths = []

    if axis_x_label == 'year':
        dates = pd.date_range(date_start, date_end, freq='y')
        # get all dates with removed duplicates
        dates_list = list(map(lambda d: d.to_pydatetime(), dates))
        all_dates = list(OrderedDict.fromkeys(
            [date_start] + dates_list + [date_end]))
        time_block_labels = list(map(lambda d: d.strftime('%Y'), all_dates))
        get_trend_images(dates, csv_path, col_time_header,
                         col_url_header, col_rank_header, date_start, date_end)

    elif axis_x_label == 'month':
        dates = pd.date_range(date_start, date_end, freq='m')
        # get all dates with removed duplicates
        dates_list = list(map(lambda d: d.to_pydatetime(), dates))
        all_dates = list(OrderedDict.fromkeys(
            [date_start] + dates_list + [date_end]))
        time_block_labels = list(map(lambda d: d.strftime(
            '%B') + ' ' + d.strftime('%Y'), all_dates))
        get_trend_images(dates, csv_path, col_time_header,
                         col_url_header, col_rank_header, date_start, date_end)

    elif axis_x_label == 'week':
        dates = pd.date_range(date_start, date_end, freq='w')
        # get all dates with removed duplicates
        dates_list = list(map(lambda d: d.to_pydatetime(), dates))
        all_dates = list(OrderedDict.fromkeys(
            [date_start] + dates_list + [date_end]))
        time_block_labels = list(
            map(lambda d: 'Week ' + d.strftime('%U') + ' ' + d.strftime('%Y'), all_dates))
        get_trend_images(dates, csv_path, col_time_header,
                         col_url_header, col_rank_header, date_start, date_end)

    elif axis_x_label == 'day':
        dates = pd.date_range(date_start, date_end, freq='d')
        # get all dates with removed duplicates
        dates_list = list(map(lambda d: d.to_pydatetime(), dates))
        all_dates = list(OrderedDict.fromkeys(
            [date_start] + dates_list + [date_end]))
        time_block_labels = list(
            map(lambda d: d.strftime('%d.%m.%Y'), all_dates))
        get_trend_images(dates, csv_path, col_time_header,
                         col_url_header, col_rank_header, date_start, date_end)

    else:
        print('No valid x label input: needs to be day, week, month or year')
        return

    # get images from urls and save them
    try:
        trend_image_local_paths = [urllib.request.urlretrieve(
            url, image_dir + 'trend_image_time_block_' + str(trend_image_urls.index(url)) + '.jpg')[0] for url in trend_image_urls]
    except Exception as e:
        print('Something went wrong with fetching images from urls : ' + str(e))

    # create visual output

    # x values: create as many time blocks as ranks are available: block 0, 1, ... for rank 0, 1, ...
    trend_image_time_blocks = list(range(0, len(trend_image_ranks)))

    fig, ax = plt.subplots()
    ax.scatter(trend_image_time_blocks, trend_image_ranks)

    for x0, y0, path in zip(trend_image_time_blocks, trend_image_ranks, trend_image_local_paths):
        ab = AnnotationBbox(get_plot_image(path), (x0, y0), frameon=False)
        ax.add_artist(ab)

    fig.savefig('foo.png')
    plt.close(fig)

    print(trend_image_urls)
    print(trend_image_ranks)
    print(trend_image_local_paths)


def main():
    args = sys.argv[1:]
    result_dir = 'results/'
    image_dir = result_dir + 'images/'
    # create directories to store files
    os.makedirs(result_dir, exist_ok=True)
    os.makedirs(image_dir, exist_ok=True)

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
             axis_x_label, axis_y_label, date_start, date_end, result_dir, image_dir)

    elif len(args) == 8:
        plot(args[0], args[1], args[2], args[3],
             args[4], args[5], datetime.strptime(args[6], '%Y-%m-%d'), datetime.strptime(args[7], '%Y-%m-%d'), result_dir, image_dir)


if __name__ == "__main__":
    main()
