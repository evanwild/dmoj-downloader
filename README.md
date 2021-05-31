# DMOJ Downloader

## What is this for?

DMOJ lets you download the code for all your solutions, however the files are just named as numbers. This tool renames your files to the problem names, and groups them into folders.

## Want to use this project?

1. Download your submissions from DMOJ
	1. Go to https://dmoj.ca/data/prepare/
	2. Check "Download submissions" and make sure to filter by AC
	3. Click "Prepare new download", then "Download data"

2. Setup this project on your computer
	1. Clone with `$ git clone https://github.com/evanwild/dmoj-downloader.git`
	2. Setup a virtual environment (Commands differ by operating system)
		```sh
		$ cd dmoj-downloader
		$ python -m venv env
		$ env\Scripts\Activate
		(env)$ pip install -r requirements.txt
		```

3. Run download.py (You must specify the path to your submissions folder)
	```sh
	(env)$ python downloader.py C:\Users\Evan\Downloads\submissions
	```