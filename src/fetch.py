import requests
from datetime import datetime, timedelta
import pytz
from bs4 import BeautifulSoup

EASTERN = pytz.timezone('America/New_York')

DINING_HALLS = ["Mosher-Jordan", "South Quad", "Bursley", "East Quad", "North Quad", "South Quad", "Twigs at Oxford"]

MAX_DAYS = 15

def fetch_all_fish_instances():
    matches = {}
    
    for days_offset in range(0, MAX_DAYS):
        print(f'Now Checking {days_offset} days')
        current_date = datetime.now(tz=EASTERN) + timedelta(days=days_offset)
        formatted_date = current_date.strftime('%Y-%m-%d')

        for dining_hall in DINING_HALLS:
            # i know I could use := here, but the version of python on my Pi is too old and every time i try to upgrade it, something horrible happens
            local_matches = fetch_for_dining_hall_and_date(dining_hall, formatted_date)

            if local_matches:
                if formatted_date not in matches:
                    matches[formatted_date] = {}
                matches[formatted_date][dining_hall] = local_matches
                
    print(matches)
            
def fetch_for_dining_hall_and_date(dining_hall: str, formatted_date: str):
    dining_hall_id = dining_hall.replace(' ', '-').lower()
    r = requests.get(f'https://dining.umich.edu/menus-locations/dining-halls/{dining_hall_id}/?menuDate={formatted_date}')
    
    items = parse_items(r.text, formatted_date)
    
    matches = check_for_fish(items)
    return matches

def parse_items(html: str, formatted_date: str) -> dict:
    soup = BeautifulSoup(html, 'html.parser')
    courses = {}
    
    # if we're looking at a future menu, make sure the dates line up. if they don't, we've gone too far and are duplicating menus
    if 'today' not in soup.find('h2', class_="menuTitle").get_text().lower():
        menu_date = datetime.strptime(soup.find('span', class_='date').get_text(), '%A, %B %d, %Y').strftime('%Y-%m-%d')
        
        if menu_date != formatted_date:
            print(f'Dates do not match up, skipping. Requested Date: {formatted_date}; Provided Date: {menu_date}')
            return courses
    
    for meal in soup.find_all('div', class_='courses'):
        course = meal.find_previous_sibling('h3').get_text().strip()
        items = [div.get_text().strip() for div in meal.find_all('div', class_='item-name')]
        courses[course] = items
    
    return courses

def check_for_fish(courses):
    matches = []
    for course, items in courses.items():
        fish_matches = [item for item in items if 'fish' in item.lower()]
        for match in fish_matches:
            matches.append({"course": course, "item": match})
            
    return matches

fetch_all_fish_instances()