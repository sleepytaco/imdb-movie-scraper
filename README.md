  # IMDB Parents Guide Information Scraper
A python web scraping script that takes in a movie name as input and outputs the metascore and the parents guide information (only the sex &amp; nudity description) for that movie. If not much information about the movie was found, the script offers to google the movie in your web browser.

 # Installation
```
pip install beautifulsoup4
pip install requests
```

# Screenshots
### Initial Input
![screenshot 1](script_screenshots/imdb_sc1.png?raw=true)
### General Search Result Screen
![screenshot 2](script_screenshots/imdb_sc2.png?raw=true)
### Search Result Screen in case not enough information is found
![screenshot 3](script_screenshots/imdb_sc3.png?raw=true)



 # How the script works
 This script uses the beautifulsoup4 and the requests module to scrape the IMDB website for the information. The script first gets the movie's reference code from the IMDB search page and uses that to find the movie's main page and the parents guide page. As the script only considers the first result from the search page, **it is recommended that you type in the movie name as accurately you can**.
 
 # My motive for this script
Whenever I watch a movie with my relatives/family I often end up looking at the parents guide section in order to decide whether or not to watch the movie with them. It is really tiresome to first find the movie then scrolldown to find the parents guide section. So, I ended up making this script to gather all the information I need.
