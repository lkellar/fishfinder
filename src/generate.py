from src.fetch import fetch_all_fish_instances
import dominate
from dominate.tags import * 
from datetime import datetime

def generate_page(fish_data):
    doc = dominate.document(title='Fish Finder - University of Michigan')
    
    with doc.head:
        meta(charset="UTF-8")
        meta(name="viewport", content="width=device-width, initial-scale=1")
        meta(name="description", content="The fastest way to locate dining hall fish at the University of Michigan")
        link(rel="stylesheet", href="style.css")
        
    with doc.body:
        with main():
            h1("Fish Finder")
            for index, day in enumerate(fish_data):
                with div(_class="day"):
                    h2(day['date'].strftime('%A, %B %d, %Y'))
                    for hall, courses in day["data"].items():
                        for course in courses:
                            h3(f'{hall} - {course["course"]}')
                            with ul():
                                for item in course["items"]:
                                    li(item)
                            
                if index < len(fish_data) - 1:
                    hr()
                
    with open('out.html', 'w') as f:
        f.write(doc.render())

EXAMPLE_FISH_DATA = [{'date': datetime(2023, 1, 4, 13, 41, 19, 149573), 'data': {'Twigs at Oxford': [{'course': 'Lunch', 'items': ['Whitefish w/ Mango Pineapple Salsa']}]}, 'days_until': 1}, {'date': datetime(2023, 1, 11, 13, 42, 39, 161323), 'data': {'South Quad': [{'course': 'Lunch', 'items': ['MSC Fish Sandwich on White Bun', 'Baked Rockfish']}, {'course': 'Dinner', 'items': ['Crispy Rockfish']}]}, 'days_until': 8}, {'date': datetime(2023, 1, 13, 13, 43, 4, 103163), 'data': {'South Quad': [{'course': 'Dinner', 'items': ['Smothered Catfish']}]}, 'days_until': 10}, {'date': datetime(2023, 1, 16, 13, 43, 44, 317924), 'data': {'South Quad': [{'course': 'Dinner', 'items': ['MSC Grilled Cod Fish Taco']}], 'Bursley': [{'course': 'Dinner', 'items': ['MSC Grilled Cod Fish Taco']}], 'Twigs at Oxford': [{'course': 'Dinner', 'items': ['MSC Grilled Cod Fish Taco']}]}, 'days_until': 13}]

generate_page(EXAMPLE_FISH_DATA)