# Image trendline plotter
## About
This repository provides a way to plot image trendlines visually: the result is a two-dimensional graph image that maps images over time ranked after a measure of choice (e.g. number of retweets, image frequency, author popularity, etc.). 
## Quick start
Download the source code into a directory of your choice.

Open your terminal and head to the directory:

`cd <dirname>`

From there, run the following command:

`python3 main.py <csv file path> <timestamp column header> <url column header> <rank column header> <x axis label> <y axis label> <start date> <end date> topic>`

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
'/Users/work/Datasets/deepfake/twitter/deepfake_images.csv' 
'_ - created_at' 
'_ - entities - media - _ - url' 
'_ - quote_count' 
'month'
'quotes'
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