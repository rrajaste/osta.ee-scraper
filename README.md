# Osta.ee web scraper

### What is this?
This is a simple web scraper for collecting product information from osta.ee auction site.
The scraper scrapes a specified category on Osta.ee and writes found product information in a .json output file.

### Setting things up

Make sure you have:

* Python3 with version that is >=3.8.2 installed on your machine
* BeautifulSoup4 (https://pypi.org/project/beautifulsoup4/) installed and accessible
### Using the scraper

To run the scraper, specify the category that you wish to scrape, e.g:
```
python scraper.py arvutid
```
Subcategories are also supported, e.g:
```
python scraper.py arvutid/monitorid
```
Specifying a second argument overrides the default output filename, eg:
```
python scraper.py arvutid/monitorid test.json
```
### Things to keep in mind
* Not all categories are have been tested, it is probable that some will not work.

* Since the script runs syncronously, it may take several seconds or even minutes to complete on bigger categories. 

* User input validation is minimal, entering faulty arguments can break the script or cause unexpected behaviour.
### Dependencies
* Python >=3.8.2
* BeautifulSoup4
### Authors
* Ranno Rajaste
