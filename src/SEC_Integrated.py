import requests
from bs4 import BeautifulSoup
import os
import re
from keys import sec_keywords

USER_AGENT = os.getenv('USER_AGENT', "SECurityTr8Ker/1.0 (martinrosenthal.asher@gmail.com)")
HEADERS = {"User-Agent": USER_AGENT}

# Compile the keywords regex pattern for efficiency
# keywords_pattern = re.compile('|'.join(map(re.escape, keywords)), re.IGNORECASE)

def fetch_8k_filings(how_many):
    rss_url = f"https://www.sec.gov/cgi-bin/browse-edgar?action=getcurrent&type=8-K&company=&dateb=&owner=include&start=0&count={how_many}&output=atom"
    response = requests.get(rss_url, headers=HEADERS)
    soup = BeautifulSoup(response.content, "xml")
    
    entries = soup.find_all("entry")
    filing_details = []
    for entry in entries:
        filing_url = entry.find("link", {"rel": "alternate"})["href"].replace('-index.htm', '.txt')
        filing_details.append({"url": filing_url})
    
    return filing_details

def extract_info_from_filing(filing_url):
    return_url = filing_url.replace('.txt', '-index.htm')
    response = requests.get(filing_url, headers=HEADERS)
    content = response.text.splitlines()[:150]  # Only process the first 150 lines
    result_list = []

    # Initialize variables
    date = None
    company_name = None

    for idx, line in enumerate(content):
        line = line.strip()

        # Extract the date from the first line after the colon
        if idx == 0 and ':' in line:
            date_part = line.split(':')[-1].strip()
            if re.match(r"\d{8}", date_part):
                date = f"{date_part[:4]}.{date_part[4:6]}.{date_part[6:]}"

        # Extract the company name from the specified line
        if line.startswith("COMPANY CONFORMED NAME:"):
            company_name = line.split(":", 1)[1].strip()

        # Check for keyword matches using regex
        if sec_keywords.search(line):
            # Ensure date and company are captured before appending
            if not date or not company_name:
                continue
            matched_keywords = sec_keywords.findall(line)
            for matched_keyword in matched_keywords:
                result_list.append(["SEC", date, company_name, matched_keyword, return_url])

    return result_list

def SEC_run_keyword_search(how_many):
    print("Fetching new 8-K filings...")
    filings = fetch_8k_filings(how_many)
    if not filings:
        print("No filings found.")
        return

    all_results = []
    total_filings = len(filings)
    for idx, filing in enumerate(filings, start=1):
        results = extract_info_from_filing(filing['url'])
        all_results.extend(results)
        print(f"Processing: {idx}/{total_filings} filings complete ({(idx/total_filings)*100:.2f}%)")
    
    return all_results



if __name__ == "__main__":
    articles_with_keywords = SEC_run_keyword_search(40)
    if articles_with_keywords:
        for result in articles_with_keywords:
            print(result)
    else:
        print("No articles found with audit-related keywords.")
