import feedparser
from datetime import datetime, timedelta
import re
from keys import keywords

# Compile the keywords regex pattern for efficiency


# Function to get articles from this year and the last year from the Hindenburg Research RSS feed
def get_hindenburg_articles():
    rss_url = 'https://hindenburgresearch.com/rss'
    feed = feedparser.parse(rss_url)
    articles = []
    year2025 = datetime.now().year
    year2024 = year2025 - 1
    year2023 = year2024 - 1
    
    for entry in feed.entries:
        pub_date = datetime(*entry.published_parsed[:3])
        if pub_date.year in [year2025, year2024, year2023]:
            articles.append(entry)
    
    return articles

# Function to check if the title, description, or content matches any audit-related words
def check_for_audit_keywords(entry):
    title = entry.title.lower()
    description = entry.description.lower() if 'description' in entry else ''
    content_encoded = entry.content[0].value.lower() if 'content' in entry else ''

    # Use regex search to match keywords and identify which keyword matched
    match = keywords.search(f"{title} {description} {content_encoded}")
    return match.group(0) if match else None

# Main function to find articles from this year and the last year with audit-related words
def hinden_find_and_display_articles():
    articles = get_hindenburg_articles()
    results = []
    
    for article in articles:
        print(f"Checking article: {article.link}")
        matched_keyword = check_for_audit_keywords(article)
        if matched_keyword:
            print(f"Keyword: {matched_keyword} found")
            # Extract the company name and format the date
            pub_date = datetime(*article.published_parsed[:3]).strftime('%Y.%m.%d')
            company = article.title.split('-')[0].strip()
            company = " ".join(company.split()[:5])
            results.append(["Hindenburg Research", pub_date, company, matched_keyword, article.link])
    
    return results

# Example usage
if __name__ == "__main__":
    articles_with_keywords = hinden_find_and_display_articles()
    if articles_with_keywords:
        for result in articles_with_keywords:
            print(result)
    else:
        print("No articles found with audit-related keywords.")
