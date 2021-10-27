# Image trendline plotter
## About
This repository provides a way to plot image trendlines visually: the result is a two-dimensional graph image (.jpg) that maps images over time ranked after a measure of choice (e.g. number of retweets, image frequency, author popularity, etc.). 

## Input
A csv file with the following data:

* image urls
* ranking measure per url (e.g. retweets)
* time stamp per url (e.g. time of being shared in a tweet); preferably keep the time data in the following formats: YYYY-mm-dd, or another valid example would be 2017-12-16T20:23:21.000Z. If your time format is different, this can also be changed accordingly in the code instead of your data.

Besides:
* a topic name which gets included in the title
* a measure name which gets included on the y-axis and in the title 
* a choice whether you want to plot your image trendline with a weekly, monthly, quarter monthly, annual distance
* the path to your csv file

## Output
The output is a .jpg file which displays the image trendline graph and will be stored in a directory named 'plots'. 
Further, all retrievable image urls are stored locally on your device in a directory named 'images'.

The output might be extended to include a csv output file that holds the relevant data for reproducing other visual outputs. 
  
## Prerequisites

* Have installed python3
* Install missing python packages via installer such as pip3 
  
## Quick start
Download the source code into a directory of your choice.

Open your terminal and head to the directory:

`cd <dirname>`

From there, run the following command:

`python3 main.py <csv file path> <timestamp column header> <url column header> <rank column header> <x axis label> <y axis label> <start date> <end date> <topic>`

with

* `<csv file path>` being the absolute path to your csv data file
* `<timestamp column header>` being a copy of the column header where the time stamp attached to an image url is held
* `<url column header>` being a copy of the column header where the image urls are held
* `<rank column header>` being a copy of the column header where the  measure after which images are ranked by are held, e.g. the number of retweets
* `<x axis label>` being one of the following options: **year**, **month**, **week**, **day**
*  `<y axis label>` being a term describing the measure after which images are ranked, e.g. retweets
* `<start date>` being the date your plot starts from; please use following format: **YYYY-mm-dd**
* `<end date>` being the date your plot ends with; please use following format: **YYYY-mm-dd**
* `<topic>` being the name of the topic you analyse 


Example call

`python3 main.py 
'/Users/datasets/deepfake/twitterdata/deepfake_images.csv' 
'_ - created_at' 
'_ - entities - media - _ - url' 
'_ - retweet_count' 
'month'
'retweets'
'2017-01-01'
'2017-12-01'
'#deepfake'`


## Menu-guided start
Download the source code into a directory of your choice.

Open your terminal and head to the directory:

`cd <dirname>`

From there, run the following command:

`python3 main.py`

From there, a menu is going to guide you through the choice of arguments.

## Other

Currently there is another tool under development which plots image trendgrids. 

Further, feel free to fork and use this tool for exciting research or just fun. 