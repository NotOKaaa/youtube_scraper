YouTube Search Scraper
A Python tool to scrape YouTube search results and return clean data as pandas DataFrames.
Features

Search YouTube for any query
Automatically scrolls to load more results
Returns data as pandas DataFrame for easy analysis
Exports to CSV
Handles cases where YouTube has fewer results than requested

Installation

Clone this repository:

bashgit clone https://github.com/NotOKaaa/youtube-scraper.git
cd youtube-scraper

Install dependencies:

bashpip install -r requirements.txt
Usage
As a Python module:
pythonfrom youtube_scraper import scrape_search

# Scrape 100 videos about "neuralink"
data = scrape_search("neuralink", max_results=100)

# View the data
print(data.head())

# Save to CSV
data.to_csv("results.csv", index=False)

# Analyze with pandas
print(f"Total videos: {len(data)}")
print(data['title'].str.contains('Elon').sum(), "videos mention Elon")
Run the example:
bashpython youtube_scraper.py
This will scrape 50 videos about "neuralink" and save them to results.csv.
Requirements

Python 3.7+
Firefox browser installed
Dependencies listed in requirements.txt

Parameters

query (str): The search term to look up on YouTube
max_results (int): Maximum number of videos to scrape (default: 100)

Output
Returns a pandas DataFrame with columns:

title: Video title
url: Full YouTube video URL

Notes

The scraper uses Firefox via Selenium
Geckodriver is automatically managed by webdriver-manager
Respects YouTube's loading behavior - won't force-load unavailable content
If YouTube has fewer results than requested, returns all available results

License
MIT

