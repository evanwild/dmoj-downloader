# DMOJ Downloader

### What is this for?

DMOJ.ca allows you to download the code for all your solutions, but the file names are just numbers. This script renames your solution files to the names of the problems, and groups them into folders by category.

## Want to use this project?

1. Download your submissions from DMOJ
	- Go to https://dmoj.ca/data/prepare/
	- Check *"Download submissions?"*, and make sure to filter by AC
	- Click *"Prepare new download"*, then *"Download data"*

2. Setup this project on your computer
	- Download/Fork/Clone
	- 
		```sh
		$ cd dmoj-downloader
		$ python -m venv env
		$ env\Scripts\Activate
		(env)$ pip install -r requirements.txt
		```