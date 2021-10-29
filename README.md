# Image url trend plotter 
## About
This repository provides a way to plot the circulation of trending image urls visually: the result is an image showing a two-dimensional graph that maps the top x trending images from urls over time (per week, month, or year) ranked after a measure of choice (e.g. number of retweets, image frequency, author popularity, etc.). 

*Example use case:*

You wish to see the images of the most retweeted image urls that occur within tweets that mention a hashtag (e.g. #deepfake) on Twitter. Like this:

![Example use case](https://github.com/sarahtartaruga/image-trendlines/blob/image-trendgrids-horizontal/example.png)

After having downloaded the dataset with tweets containing your desired hashtag, you make sure that the time stamp, media url, and the retweet count data are available. 

You choose to inspect the top 3 trending images per month, whereas you set a minimum retweet count of 10 as a restriction. This means, it might happen that some months won't show an image or some less than 3. By setting the amount of trending images and a threshold, one can retrieve a granular overview over the chronological evolution of user engagement around a topic by looking at its visual content. 

You download our tool to your local device, and follow the instructions below to generate the visual output.

## Quick start 

*For a menu-guided start please see below*

Download the source code into a directory of your choice.

Open your terminal and head to the directory:

`cd <dirname>`

From there, run the following command:


`python3 main.py <csv file path> <timestamp column header> <url column header> <rank column header> <x axis label> <y axis label> <start date> <end date> <topic> <threshold> <top x>`

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
* `<threshold>` being the lower limit for a trend image url in terms of measure, e.g. min. 10 retweets
* `<top x>` being the maximum number of trending images you want to inspect per time batch, e.g. max. 2 trending images per month


*Example call*

`python3 main.py 
'/Users/datasets/deepfake/twitterdata/deepfake_data.csv' 
'_ - created_at' 
'_ - entities - media - _ - url' 
'_ - retweet_count' 
'month'
'retweets'
'2017-01-01'
'2017-12-01'
'#deepfake'
10
3`

## Menu-guided start
Download the source code into a directory of your choice.

Open your terminal and head to the directory:

`cd <dirname>`

From there, run the following command:

`python3 main.py`

From there, a terminal menu is going to guide you sequentially through the choice of arguments.

## Adaptions
Sometimes adaptions might be necessary as this repository was designed for a particular Twitter API dataset. 
In the code, look at `# TO CONFIGURE` to find the relevant points for an easy adaption. 

Typical features that you have to adapt will be the time format as indicated in your csv file for pasing it correctly. Further, you might wish to change the plot type (e.g. to a stem plot) or the general styling (e.g. font, figure size, image size). 

## Further plans and extensions

* **Placeholder feature**: gives the possibility to show pre-designed placeholder images instead of the image url image after a label in the dataset, e.g. if an image url is labeled as 'porn' in the dataset ( 'is_porn' == True) one can manually design a placeholder image which will then be displayed instead of the fetched url; a new input parameter would then be the name from the csv column which must holds booleans ('is_porn')
* **Color feature**: the background is colored after time batch belonging, e.g. all top x images which belong to a certain time batch (e.g. a month) share the same background color
* **Annotation feature**: extend the information related to the image url by showing it in the x-axis label (e.g. original tweet author)