# Description

This project is about sentiment analysis on tweets. What we want to achieve, is to let a machine predict whether a tweet has a positive or negative meaning behind it. We assume that tweets containing smiling or happy emoji, are positive, whereas those who contain sad or angry emoji, are negative. The machine will then predict the polarity of those tweets, based on a dataset we are feeding onto it to train it.
We can describe the workflow as : collecting the tweets -> text-preprocessing raw tweets' text -> features-extraction from processed text -> machine-learning 



# Authors

Paul-Emile MOREAU  p1505614
Bao Anh NGUYEN     p1510926
Thierry NGUYEN     p1503221
Supervised by Hussein Al-Natsheh



# Installation

1 - You need pip on your machine (https://pip.pypa.io/en/stable/installing)
2 - To install "virtualenv", run the command: 
		[sudo] pip install virtualenv
3 - Create a virtual environment at the project: 
		virtualenv -p python3 venv 
4 - Activate the virtual environment:
		source venv/bin/activate
5 - Install the dependencies within the virtual environment:
		pip install -r requirements.txt
6 - Deactivate the venv:
		deactivate 



# Usage and explanations

For the commands, we are supposing that you are located at the project's root and that you have the virtual environment activated :

	* collect/ => This package is used to perform the task of collecting tweets from Twitter's API. 

		** To collect tweets :  
				cd collect
				python collect.py

		=>  It will create at the project's root a json file named "collecting_file.json", which stores the collected tweets.
			The file will be appended if it is already existing. You may encounter "IncompleteRead" error, which implies that Twitter's API is fetching more tweets than the application can handle: you may retry (sometimes the error doesn't happen at all, sometimes it happens fast) or you may reduce the number of subjects the stream needs to track (for instance, in our current case : reduce the number of emoji tracked, by commenting or removing the lines which call "emoji_store").

	* features_extraction.py => This file is used to store different features extraction techniques. It is used by the classifier to get a training set.

	




