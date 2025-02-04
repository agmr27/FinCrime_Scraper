import requests
from bs4 import BeautifulSoup
import re
from datetime import datetime
from keys import keywords


def bleeker_scrape_and_check_keywords():
    url = "https://www.bleeckerstreetresearch.com/research"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    
    articles_info = []
    
    # Find all blog items
    articles = soup.find_all('div', class_='blog-item-text')

    for article in articles:
        title_tag = article.find('h1', class_='blog-title')
        title = title_tag.get_text().replace("\n", "").strip() if title_tag else "No title found"
        link = title_tag.find('a')['href'] if title_tag else ""
        
        # Retrieve the article page for more content
        article_page = requests.get(f"https://www.bleeckerstreetresearch.com{link}")
        print (f"Checking article: www.bleeckerstreetresearch.com{link}")
        article_soup = BeautifulSoup(article_page.text, "html.parser")
        
        # Extract article content
        content = article_soup.find('div', class_='sqs-block-content')  # This is the correct selector
        content_text = content.get_text() if content else ""
        
        # Check if any keywords are in the content
        match = keywords.search(content_text)
        keyword_found = match.group(0) if match else "No keyword found"
    
        
        # Get the article's date
        date_tag = article.find('time', class_='blog-date')
        date_str = date_tag.get_text() if date_tag else "Unknown Date"
        
        # Convert date to the required format (yyyy.mm.dd)
        try:
            date = datetime.strptime(date_str, "%m/%d/%y").strftime("%Y.%m.%d")
        except ValueError:
            date = "Unknown Date"
        
        # Store information in the desired list format
        if keyword_found != "No keyword found":
            print (f"Keyword '{keyword_found}' found")
            articles_info.append(["Bleeker Street", date, title, keyword_found, f"https://www.bleeckerstreetresearch.com{link}"])
    
    return articles_info

# # Call the function and print results
if __name__ == "__main__":
    articles_with_keywords = bleeker_scrape_and_check_keywords()
    if articles_with_keywords:
        for result in articles_with_keywords:
            print(result)
    else:
        print("No articles found with specified keywords.")
