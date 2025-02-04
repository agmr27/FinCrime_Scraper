import time
from src.BearCave_Integrated import bear_find_and_display_articles
from src.Hinenburg_Integrated import hinden_find_and_display_articles
from src.HedgeWeek_Integrated import hedge_find_and_display_articles
from src.SEC_Integrated import SEC_run_keyword_search
from src.law360_Integrated import scrape_law360_articles
from src.Bleeker_Street_Integrated import bleeker_scrape_and_check_keywords
from util.printing import pretty_print_list, write_to_csv

# ANSI escape codes for color
RED = '\033[91m'
RESET = '\033[0m'

#######################################################
#How Many 8K filings do you want to do (40 reccommended):
SEC_filings_number = 40

#How far back do you want to start Bear searches (225 [Spring 2024] reccommended):
bear_start_number = 240
#######################################################

tasks = [
    ("HEDGEWEEK", hedge_find_and_display_articles),
    ("Bear Cave", lambda: bear_find_and_display_articles(bear_start_number)),
    ("HindenBurg Research", hinden_find_and_display_articles),
    ("Law360", scrape_law360_articles),
    ("Bleeker Street", bleeker_scrape_and_check_keywords),
    ("SEC Edgar", lambda: SEC_run_keyword_search(SEC_filings_number))
]

results = []
for name, func in tasks:
    print(f"{RED}****************** RUNNING {name} ******************{RESET}\n")
    time.sleep(0.5)
    results.extend(func())
    print("\n")

seen = set()
unique_results = [item for item in results if not (tuple(item[:3]) in seen or seen.add(tuple(item[:3])))]

pretty_print_list(unique_results)
write_to_csv(unique_results)
