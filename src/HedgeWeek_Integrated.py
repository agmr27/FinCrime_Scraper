import feedparser
from datetime import datetime, timedelta
import re
from keys import keywords




# Function to get articles from the past week
def get_hedgeweek_articles():
    rss_url = 'https://www.hedgeweek.com/rss'  # Hedgeweek RSS feed URL
    feed = feedparser.parse(rss_url)
    articles = []
    today = datetime.now()
    one_week_ago = today - timedelta(weeks=1)

    for entry in feed.entries:
        pub_date = datetime(*entry.published_parsed[:3])
        if one_week_ago <= pub_date <= today:
            articles.append(entry)
    
    return articles

# Function to check if any keyword matches using regex search
def check_for_keywords(entry):
    # Combine all relevant fields for searching
    title = entry.title.lower()
    description = entry.description.lower() if 'description' in entry else ''
    content_encoded = entry.content[0].value.lower() if 'content' in entry else ''

    combined_text = f"{title} {description} {content_encoded}"
    match = keywords.search(combined_text)
    return match.group(0) if match else None

# Main function to find articles from the last week with keyword matches
def hedge_find_and_display_articles():
    articles = get_hedgeweek_articles()
    results = []
    
    for article in articles:
        print(f"Checking article: {article.link}")
        matched_keyword = check_for_keywords(article)
        if matched_keyword:
            print(f"Keyword: {matched_keyword} found")
            pub_date = datetime(*article.published_parsed[:3]).strftime('%Y.%m.%d')
            company = " ".join(article.title.split()[:5])
            results.append(["Hedge Week", pub_date, company, matched_keyword, article.link])
    
    return results

# Example usage
if __name__ == "__main__":
    articles_with_keywords = hedge_find_and_display_articles()
    if articles_with_keywords:
        for result in articles_with_keywords:
            print(result)
    else:
        print("No articles found with specified keywords.")
