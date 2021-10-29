# Image url trend plotter 
## About
This repository provides a way to plot the circulation of trending image urls visually: the result is an image showing a two-dimensional graph that maps the top x trending images from urls over time (per week, month, or year) ranked after a measure of choice (e.g. number of retweets, image frequency, author popularity, etc.). 

*Example use case:*

You wish to see the images of the most retweeted image urls that occur within tweets that mention a hashtag (e.g. #deepfake) on Twitter. Like this:

![Example use case](https://github.com/sarahtartaruga/image-trendlines/tree/image-trendgrids-horizontal/example.png?raw=true)

After having downloaded the dataset with tweets containing your desired hashtag, you make sure that the time stamp, media url, and the retweet count data are available. 

You choose to inspect the top 3 trending images per month, whereas you set a minimum retweet count of 10 as a restriction. This means, it might happen that some months won't show an image or some less than 3. By setting the amount of trending images and a threshold, one can retrieve a granular overview over the chronological evolution of user engagement around a topic by looking at its visual content. 

## Adaptions
Sometimes adaptions might be necessary as this repository was designed for a particular Twitter API dataset. 
In the code, look at '# TO CONFIGURE' to find the relevant points for an easy adaption. 
## Quick start
Download the source code into a directory of your choice.

Open your terminal and head to the directory:

`cd <dirname>`

From there, run the following command:

`python3 main.py <csv file path> <timestamp column header> <url column header> <rank column header> <x axis label> <y axis label> <start date> <end date>`

with

* `<csv file path>` being the absolute path to your csv data file
* `<timestamp column header>` being a copy of the column header where the time stamp attached to an image url is held
* `<url column header>` being a copy of the column header where the image urls are held
* `<rank column header>` being a copy of the column header where the  measure after which images are ranked by are held, e.g. the number of retweets
* `<x axis label>` being one of the following options: **year**, **month**, **week**, **day**
*  `<y axis label>` being a term describing the measure after which images are ranked, e.g. retweets
* `<start date>` being the date your plot starts from; please use following format: **YYYY-mm-dd**
* `<end date>` being the date your plot ends with; please use following format: **YYYY-mm-dd**


Example call

`python3 main.py 
'/Users/work/Datasets/deepfake/twitter/deepfake_images.csv' 
'_ - created_at' 
'_ - entities - media - _ - url' 
'_ - quote_count' 
'month'
'quotes'
'2017-01-01'
'2017-12-01'`


## Menu-guided start
Download the source code into a directory of your choice.

Open your terminal and head to the directory:

`cd <dirname>`

From there, run the following command:

`python3 main.py`

From there, a menu is going to guide you through the choice of arguments.