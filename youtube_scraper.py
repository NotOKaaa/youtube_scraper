"""
YouTube Search Scraper
A tool to scrape YouTube search results and return data as pandas DataFrame
"""

from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.firefox import GeckoDriverManager
import pandas as pd
import time


def scrape_search(query, max_results=100):
    """
    Scrape YouTube search results for a given query.
    
    Parameters:
    -----------
    query : str
        The search term to look up on YouTube
    max_results : int
        Maximum number of videos to scrape (default: 100)
        If YouTube has fewer results, returns what's available
    
    Returns:
    --------
    pandas.DataFrame
        DataFrame with columns: 'title', 'url'
    """
    
    driver = webdriver.Firefox(service=Service(GeckoDriverManager().install()))
    
    try:
        # Build search URL
        search_url = f"https://www.youtube.com/results?search_query={query.replace(' ', '+')}"
        driver.get(search_url)
        
        # Wait for initial results
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "video-title"))
        )
        
        print(f"Searching for: {query}")
        print(f"Target: {max_results} videos\n")
        
        # Keep scrolling until we have enough results or no more load
        previous_count = 0
        scroll_attempts = 0
        max_scroll_attempts = 50  # Safety limit
        
        while scroll_attempts < max_scroll_attempts:
            # Get current video count
            current_titles = driver.find_elements(By.ID, "video-title")
            current_count = len(current_titles)
            
            print(f"Scroll {scroll_attempts + 1}: Found {current_count} videos", end="")
            
            # Check if we have enough results
            if current_count >= max_results:
                print(" ✓ Target reached!")
                break
            
            # Check if no new videos loaded
            if current_count == previous_count:
                print(" - No more videos available")
                break
            
            print()  # New line
            previous_count = current_count
            
            # Scroll to bottom
            driver.execute_script("window.scrollTo(0, document.documentElement.scrollHeight);")
            time.sleep(3)
            
            scroll_attempts += 1
        
        # Final scrape
        titles = driver.find_elements(By.ID, "video-title")
        
        video_data = []
        for title in titles[:max_results]:  # Limit to max_results
            video_title = title.get_attribute('title')
            video_url = title.get_attribute('href')
            if video_title and video_url:
                video_data.append({
                    'title': video_title,
                    'url': video_url
                })
        
        print(f"\n✅ Successfully scraped {len(video_data)} videos")
        
        # Convert to DataFrame
        df = pd.DataFrame(video_data)
        return df
        
    finally:
        driver.quit()


if __name__ == "__main__":
    # Example usage
    data = scrape_search("neuralink", max_results=50)
    print("\nFirst 5 results:")
    print(data.head())
    
    # Save to CSV
    data.to_csv("results.csv", index=False)
    print("\nSaved to results.csv")