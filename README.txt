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


# Usage

With the virtual environment activated :

	1 - To collect tweets : 
		python collect.py

