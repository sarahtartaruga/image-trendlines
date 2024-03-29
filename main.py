
from datetime import datetime
import sys
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.offsetbox import OffsetImage, AnnotationBbox
import urllib.request
import os
import random
from PIL import Image
# TODO: extend tool to plot category images instead of original images; e.g. if image is labeled as porn plot a red image with text 'porn'

# y
trend_image_ranks = []
# f(x) visual representation
trend_image_urls = []
# x
trend_image_dates = []
# TO CONFIGURE: image thumbnail size
image_width = 200


def get_trend_image_per_range(csv_file, col_time_header, col_url_header, col_rank_header, date_start, date_end, threshold, top_x, separator):
    dict_temp = {}
    dates_temp = {}
    trend_urls = []
    trend_ranks = []
    trend_dates = []
    print('Get trend image url per time slot ' +
          date_start.strftime('%Y-%m-%d') + ' to ' + date_end.strftime('%Y-%m-%d'))
    # reading csv file
    df = pd.read_csv(csv_file, sep=separator)

    # TO CONFIGURE
    df[col_time_header] = df[col_time_header].apply(
        lambda t: datetime.strptime(t.split('.')[0], '%Y-%m-%dT%H:%M:%S'))

    # get all rows where date is in between start date and end date
    for index, row in df.iterrows():
        # if date in a row is in between valid range
        if (date_start <= df[col_time_header][index] <= date_end):
            # update rank value for a given media url
            url = df[col_url_header][index]
            if url != '' and isinstance(url, str):
                # print(url)
                # if url has not been stored yet, save its rank value
                if url not in dict_temp:
                    dict_temp[url] = df[col_rank_header][index]
                    dates_temp[url] = df[col_time_header][index]
                # otherwise add rank value
                else:
                    dict_temp[url] = dict_temp[url] + \
                        df[col_rank_header][index]

    if len(dict_temp) > 0:
        # todo: min. 1 top value?
        for i in range(0, top_x):
            trend_image_url = max(dict_temp, key=dict_temp.get)
            trend_image_url_rank = max(dict_temp.values())
            trend_date = dates_temp[trend_image_url]
            # append at least one url; but after that only urls with min. threshold
            if trend_image_url_rank >= threshold or len(trend_urls) == 0:
                # trend_urls.append(trend_image_url)
                # trend_ranks.append(trend_image_url_rank)
                trend_dates.append(trend_date)
                trend_dates.sort()
                index_to_insert = trend_dates.index(trend_date)
                trend_urls.insert(index_to_insert, trend_image_url)
                trend_ranks.insert(index_to_insert, trend_image_url_rank)
            del dict_temp[trend_image_url]

        return trend_urls, trend_ranks, trend_dates

        # print('Trend image found with URL : ' + str(trend_image_url))
        # print('Trend image has rank ' + str(trend_image_url_rank))

    return [''], [0], [None]


def get_trend_images(dates, csv_file, col_time_header, col_url_header, col_rank_header, date_start, threshold, top_x, separator):
    global trend_image_urls, trend_image_ranks, trend_image_dates
    # set start date to original start
    start = date_start
    for i in range(0, len(dates)):
        end = dates[i]
        urls, ranks, trend_dates = get_trend_image_per_range(
            csv_file, col_time_header, col_url_header, col_rank_header, start, end, threshold, top_x, separator)
        trend_image_urls = trend_image_urls + urls
        trend_image_ranks = trend_image_ranks + ranks
        trend_image_dates = trend_image_dates + trend_dates
        start = dates[i]
        if i == len(dates)-1:
            trend_image_dates = trend_image_dates


def get_plot_image(path):
    if path != '':
        img = Image.open(path).convert('RGB')
        wpercent = (image_width/float(img.size[0]))
        image_height = int((float(img.size[1])*float(wpercent)))
        img = img.resize((image_width, image_height), Image.LANCZOS)
        img.save(path)
        return OffsetImage(plt.imread(path))


def plot(csv_file, col_time_header, col_url_header, col_rank_header, axis_x_label, axis_y_label, date_start, date_end, result_dir, image_dir, plot_dir, topic, threshold, top_x, separator):
    print('The plotting is going to start! \nYou are going to plot your images by {a}, ranked after {b}, ranging from {c} until {d}.'.format(
        a=axis_x_label, b=axis_y_label, c=date_start.strftime('%Y-%m-%d'), d=date_end.strftime('%Y-%m-%d')))
    print('By default the results are going to be stored in the directory {i}.'.format(
        i=result_dir))

    # name to store files by
    fname = topic + '_from_' + date_start.strftime(
        '%Y-%m-%d') + '_to_' + date_end.strftime('%Y-%m-%d') + '_every_' + axis_x_label + '_top_' + str(top_x) + '_min_' + str(threshold) + '_' + str(axis_y_label)

    if axis_x_label == 'year':
        dates = pd.date_range(date_start, date_end, freq='y')
        get_trend_images(dates, csv_file, col_time_header,
                         col_url_header, col_rank_header, date_start, threshold, top_x, separator)

    elif axis_x_label == 'quarter year':
        dates = pd.date_range(date_start, date_end, freq='q')
        get_trend_images(dates, csv_file, col_time_header,
                         col_url_header, col_rank_header, date_start, threshold, top_x, separator)

    elif axis_x_label == 'month':
        dates = pd.date_range(date_start, date_end, freq='m')
        get_trend_images(dates, csv_file, col_time_header,
                         col_url_header, col_rank_header, date_start,  threshold, top_x, separator)

    elif axis_x_label == 'week':
        dates = pd.date_range(date_start, date_end, freq='w')
        get_trend_images(dates, csv_file, col_time_header,
                         col_url_header, col_rank_header, date_start, threshold, top_x, separator)

    elif axis_x_label == 'day':
        dates = pd.date_range(date_start, date_end, freq='d')
        get_trend_images(dates, csv_file, col_time_header,
                         col_url_header, col_rank_header, date_start, date_end, threshold, top_x, separator)

    else:
        print('No valid x label input: needs to be day, week, month or year')
        return

    # fetch images

     # holds paths of locally stored images
    trend_image_local_paths = []
    for url in trend_image_urls:
        try:
            trend_image_local_paths.append(urllib.request.urlretrieve(
                url, image_dir + fname + '_timeblock_' + str(trend_image_urls.index(url)) + '.jpg')[0])
        except Exception as e:
            print('Something went wrong with fetching images from urls : ' + str(e))
            if type(e).__name__ == 'HTTPError':
                trend_image_local_paths.append(
                    'placeholders/url_forbidden.jpg')
            else:
                trend_image_local_paths.append('placeholders/no_url_found.jpg')

    # section below cares about visual output
    # ----------------------------------------

    # refine label styling for date values on x-axis
    x_labels = []
    for date in trend_image_dates:
        if date is not None:
            date_str = date.strftime('%b %Y\n\n %d/%m/%y \n%H:%M:%S')
            # check if date is already present as label
            # add randomised appendix to differentiate labels
            if date_str in x_labels:
                appendix = ''
                rand_no = random.randint(1, 20)
                for i in range(0, rand_no):
                    appendix = appendix + ' '
                x_labels.append(date_str + '\n' + appendix)
            else:
                x_labels.append(date_str)
        else:
            x_labels.append('No date')

    max_rank = max(trend_image_ranks)

    # TO CONFIGURE
    # room to play with tuning parameters for changing output size
    # height_tuning 0.05 for very wide images with width 300;
    height_tuning = 0.05
    # be cautious with tuning width due to thumbnails overlapping; value between 2-4 is a good approximation
    width_tuning = 2 * (image_width / 100)
    # size should be minimum 60 x 60
    fig_height = max(60, height_tuning * max_rank)
    fig_width = max(60, width_tuning * len(x_labels))
    fig, ax = plt.subplots(figsize=(fig_width, fig_height))

    # TO CONFIGURE: change plot type here
    # ax.stem(x_labels, trend_image_ranks)
    ax.plot(x_labels, trend_image_ranks)

    for x0, y0, path in zip(x_labels, trend_image_ranks, trend_image_local_paths):
        # print('x value: ' + str(x0))
        # print('y value: ' + str(y0))
        # print('path: ' + path)
        # print('________________')

        plot_image = get_plot_image(path)
        if plot_image is not None:
            ab = AnnotationBbox(plot_image, (x0, y0), frameon=True)
            ax.add_artist(ab)

    # TO CONFIGURE: change font for axis ticks and labels
    font1 = {'family': 'serif', 'color': 'black', 'size': 60}
    font2 = {'family': 'serif', 'color': 'darkred', 'size': 40}

    # plt.xticks(rotation=45)
    ax.tick_params(axis='both', which='major', pad=15)
    plt.xticks(fontsize=20)
    plt.yticks(fontsize=20)

    plt.xlabel('date and ' + axis_x_label,
               fontdict=font2, loc='right', labelpad=30)
    plt.ylabel(axis_y_label, fontdict=font2, loc='top', rotation=0)
    plt.title('Top {top_x} trend image urls with at least {min} {rank} related to {topic} per {time} from {start} to {end}'.format(top_x=top_x, min=threshold, rank=axis_y_label, topic=topic, time=axis_x_label, start=date_start.strftime('%d.%m.%Y'), end=date_end.strftime('%d.%m.%Y')),
              loc='right', fontdict=font1, pad=100)

    # TO CONFIGURE: bbox inches remove all whitespace around figure
    fig.savefig(plot_dir + fname + '.png', bbox_inches='tight', transparent=True)
    plt.close(fig)

    # print('length image urls')
    # print(len(trend_image_urls))
    print(trend_image_urls)
    print('----------------------')

    # print('length ranks')
    # print(len(trend_image_ranks))
    # print(trend_image_ranks)
    # print('----------------------')

    # print('length local paths')
    # print(len(trend_image_local_paths))
    # print(trend_image_local_paths)
    # print('----------------------')

    # print('length dates')
    # print(len(trend_image_dates))
    # print(trend_image_dates)
    # print('----------------------')


def main():
    args = sys.argv[1:]
    result_dir = 'results/'
    image_dir = result_dir + 'images/'
    plot_dir = result_dir + 'plots/'
    # create directories to store files
    os.makedirs(result_dir, exist_ok=True)
    os.makedirs(image_dir, exist_ok=True)
    os.makedirs(plot_dir, exist_ok=True)

    # if len(args) == 0:
    #     print('Welcome to the image trendlines tool!')
    #     while True:
    #         csv_path = input(
    #             'Please enter the absolute path of the csv file you want to analyse and plot. \n')
    #         if csv_path.endswith('.csv'):
    #             print('Thanks! The csv path you entered is: {i}.'.format(
    #                 i=csv_path))
    #             break
    #         else:
    #             print(
    #                 'Something is wrong with your path. The format seems to be invalid for csv files.')
    #     col_time_header = input(
    #         'Please copy and paste the column header for the column which holds timestamp information. \n')
    #     print('Thanks! The timestamp header you entered is: {i}.'.format(
    #         i=col_time_header))
    #     col_url_header = input(
    #         'Please copy and paste the column header for the column which holds image url information. \n')
    #     print('Thanks! The url header you entered is: {i}.'.format(
    #         i=col_url_header))
    #     col_rank_header = input(
    #         'Please copy and paste the column header for the column which you want to rank your images after, e.g. retweets. \n')
    #     print('Thanks! The rank header you entered is: {i}.'.format(
    #         i=col_rank_header))
    #     axis_y_label = input(
    #         'Please enter a term describing what you rank your images after. \n')
    #     print('Thanks! You want to rank your images after {i}.'.format(
    #         i=axis_y_label))
    #     date_start = datetime.strptime(input(
    #         'From which date on do you wish to plot your trendline? Please indicate the date in following format: DD-MM-YYYY \n'), '%Y-%m-%d')
    #     print('Thanks! Your image trendline will be plotted from the following date: {i}.'.format(
    #         i=date_start.strftime('%Y-%m-%d')))
    #     date_end = datetime.strptime(input(
    #         'Until which date do you wish to plot your trendline? Please indicate the date in following format: DD-MM-YYYY \n'), '%Y-%m-%d')
    #     print('Thanks! Your image trendline will be plotted until the following date: {i}.'.format(
    #         i=date_end.strftime('%Y-%m-%d')))
    #     topic = input(
    #         'What is the topic of your research? This information will be used for the plot header')
    #     axis_x_label = input(
    #         'Finally, choose which time measure to apply for your trendline by typing one of the following options: \n year - month - week - day \n')
    #     threshold = int(input(
    #         'Choose a minimum frequency the images must fulfill, e.g. only consider images with minimum 10 retweets:\n'))
    #     top_x = int(
    #         input('How many trend images per time block do you want to plot?'))
    #     plot(csv_file, col_time_header, col_url_header, col_rank_header,
    #          axis_x_label, axis_y_label, date_start, date_end, result_dir, image_dir, plot_dir, topic, threshold, top_x)

    # elif len(args) == 11:
    plot(args[0], args[1], args[2], args[3],
        args[4], args[5], datetime.strptime(args[6], '%Y-%m-%d'), datetime.strptime(args[7], '%Y-%m-%d'), result_dir, image_dir, plot_dir, args[8], int(args[9]), int(args[10]), args[11] if len(args) == 12 else ",")


if __name__ == "__main__":
    main()
