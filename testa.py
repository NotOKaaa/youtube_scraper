from youtube_scraper import scrape_search

# Scrape 100 videos about "neuralink"
data = scrape_search("neuralink", max_results=100)

# View the data
print(data.head())

# Save to CSV
data.to_csv("results.csv", index=False)

# Analyze with pandas
print(f"Total videos: {len(data)}")
print(data['title'].str.contains('Elon').sum(), "videos mention Elon")