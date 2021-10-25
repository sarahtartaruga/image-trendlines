
from datetime import datetime
import sys

# this function calculates from a csv file what is the most trendy image in a given time range for a given measure

def trend_image_per_time_slot(csv_path, ):
    trend_image = None

    return trend_image


def plot(csv_path, col_time_header, col_url_header, col_rank_header, axis_x_label, axis_y_label, date_start, date_end, result_dir):
    print('The plotting is going to start! \nYou are going to plot your images by {a}, ranked after {b}, ranging from {c} until {d}.'.format(
        a=axis_x_label, b=axis_y_label, c=date_start.strftime('%Y-%m-%d'), d=date_end.strftime('%Y-%m-%d')))
    print('By default the results are going to be stored in the directory {i}.'.format(
        i=result_dir))


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
            'From which date on do you wish to plot your trendline? Please indicate the date in following format: DD-MM-YYYY \n'), '%d-%m-%Y')
        print('Thanks! Your image trendline will be plotted from the following date: {i}.'.format(
            i=date_start.strftime('%d-%m-%Y')))
        date_end = datetime.strptime(input(
            'Until which date do you wish to plot your trendline? Please indicate the date in following format: DD-MM-YYYY \n'), '%d-%m-%Y')
        print('Thanks! Your image trendline will be plotted until the following date: {i}.'.format(
            i=date_end.strftime('%d-%m-%Y')))
        axis_x_label = input(
            'Finally, choose which time measure to apply for your trendline by typing one of the following options: \n year - month - week - day \n')
        plot(csv_path, col_time_header, col_url_header, col_rank_header,
             axis_x_label, axis_y_label, date_start, date_end, result_dir)

    elif len(args) == 8:
        plot(args[0], args[1], args[2], args[3],
             args[4], args[5], datetime.strptime(args[6], '%d-%m-%Y'), datetime.strptime(args[7], '%d-%m-%Y'), result_dir)


if __name__ == "__main__":
    main()
