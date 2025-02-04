import feedparser
from datetime import datetime
import re
from keys import keywords  # Importing keywords from keys.py file

# List of Law360 RSS feeds for business and securities fraud
RSS_FEEDS = [
    "https://www.law360.com/securities/rss",
    "https://www.law360.com/whitecollar/rss",
    "https://www.law360.com/corporate/rss",
    "https://www.law360.com/compliance/rss"
]

def scrape_law360_articles():
    """
    Scrape articles from multiple Law360 RSS feeds and return a list of lists with articles containing keywords.

    Returns:
    - list: A list of lists where each sublist contains ["Law360", Date, Title, Keyword, Link].
    """
    results = []

    for rss_url in RSS_FEEDS:
        print(f"Parsing RSS feed: {rss_url}")
        feed = feedparser.parse(rss_url)

        for entry in feed.entries:
            title = entry.get('title', 'No title available')
            pub_date = entry.get('published', 'No date available')
            try:
                formatted_date = datetime.strptime(pub_date, '%a, %d %b %Y %H:%M:%S %z').strftime('%Y.%m.%d')
            except ValueError:
                formatted_date = 'Invalid date format'

            title_words = title.split()[:5]
            truncated_title = ' '.join(title_words)

            description = entry.get('description', '')
            link = entry.get('link', 'No link available')

            content_to_search = f"{title} {description}"
            matches = keywords.findall(content_to_search)
            if matches:
                for match in matches:
                    print(f"Keyword: '{match}' found in {title}")
                    results.append(["Law360", formatted_date, truncated_title, match, link])

    return results

# Example usage:
if __name__ == "__main__":
    articles = scrape_law360_articles()
    for article in articles:
        print(article)
