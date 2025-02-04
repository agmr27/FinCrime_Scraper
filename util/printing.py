import csv
# ANSI escape codes for color
RED = '\033[91m'
GREEN = '\033[92m'
YELLOW = '\033[93m'
BLUE = '\033[94m'
CYAN = '\033[96m'
ORANGE = '\033[38;5;214m'
PINK = '\033[38;5;213m'
RESET = '\033[0m'

source_colors = {
    'Hedge Week': BLUE,
    'BearCave': RED,
    'Hindenburg Research': YELLOW,
    'SEC': GREEN,
    'Law360': ORANGE,
    'Bleeker Street': PINK
}

def pretty_print_list(data):
    print(f"{CYAN}| {'Source':<20}| {'Date':<12}| {'Title':<60}| {'Keyword':<20}| {'Link'} |{RESET}")
    print(f"{'-'*150}")

    for entry in data:
        source, date, title, keyword, link = entry
        color = source_colors.get(source, RESET)
        print(f"{color}| {source:<20}| {date:<12}| {title:<60}| {keyword:<20}| {link} |{RESET}")

def write_to_csv(data, filename="mega_list.csv"):
    with open(filename, mode="w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(["Source", "Date", "Title", "Keyword", "Link"])
        writer.writerows(data)
    print(f"\n{GREEN}CSV file '{filename}' has been created successfully!{RESET}")