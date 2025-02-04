import requests
from bs4 import BeautifulSoup
from datetime import datetime
import re
from keys import keywords

# Compile the keywords regex pattern for efficiency


# Function to fetch article content from a given URL
def fetch_article_content(url):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')
            content = soup.find('div', class_='available-content')
            date_tag = soup.find('div', class_='pencraft pc-reset _color-pub-secondary-text_h3mln_193 _line-height-20_h3mln_80 _font-meta_h3mln_115 _size-11_h3mln_31 _weight-medium_h3mln_145 _transform-uppercase_h3mln_237 _reset_h3mln_1 _meta_h3mln_437')
            date = date_tag.get_text().strip() if date_tag else 'Unknown date'
            if date != 'Unknown date':
                try:
                    date = datetime.strptime(date, '%b %d, %Y').strftime('%Y.%m.%d')
                except ValueError:
                    date = 'Unknown date'
            return content.get_text() if content else '', date
        elif response.status_code == 404:
            return '404', None
        else:
            print(f"Failed to fetch {url}. Status code: {response.status_code}")
            return None, None
    except Exception as e:
        print(f"Error fetching {url}: {e}")
        return None, None

# Main function to find articles with regex keyword matching and return results
def bear_find_and_display_articles(start_num=230):
    results = []
    article_num = start_num
    
    while True:
        found_article = False
        url = f'https://thebearcave.substack.com/p/the-bear-cave-{article_num}'
        print(f"Checking article: {url}")
        content, date = fetch_article_content(url)

        if content and content != '404':
            found_article = True
            company_name = f"The Bear Cave #{article_num}"

            # Use regex search for keyword matching and capture which keyword matched
            match = keywords.search(content)
            if match:
                matched_keyword = match.group(0)
                print(f"Found match: {matched_keyword} in article: {url}")
                results.append(["BearCave", date, company_name, matched_keyword, url])

        if not found_article and article_num > 240:
            print(f"No more articles found after {article_num}. Stopping.")
            break

        article_num += 1
    
    return results

# Example usage
if __name__ == "__main__":
    results = bear_find_and_display_articles(start_num=225)
    for entry in results:
        print(entry)
