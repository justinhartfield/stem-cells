#!/usr/bin/env python3
"""
Generate SEO-friendly static pages for stem cell clinic directory
URL Structure: /locations/{state}/{city}/{clinic}.html
"""

import os
import json
import re

# All states and cities from the CLINIC_DATABASE
STATES_DATA = {
    'Alaska': {'cities': ['Anchorage'], 'abbr': 'AK'},
    'Arizona': {'cities': ['Phoenix', 'Tucson', 'Scottsdale'], 'abbr': 'AZ'},
    'California': {'cities': ['Los Angeles', 'San Diego', 'San Jose', 'San Francisco', 'Fresno', 'Sacramento'], 'abbr': 'CA'},
    'Colorado': {'cities': ['Denver'], 'abbr': 'CO'},
    'Florida': {'cities': ['Jacksonville', 'Miami', 'Tampa', 'Orlando'], 'abbr': 'FL'},
    'Georgia': {'cities': ['Atlanta'], 'abbr': 'GA'},
    'Hawaii': {'cities': ['Honolulu'], 'abbr': 'HI'},
    'Idaho': {'cities': ['Boise'], 'abbr': 'ID'},
    'Illinois': {'cities': ['Chicago'], 'abbr': 'IL'},
    'Indiana': {'cities': ['Indianapolis'], 'abbr': 'IN'},
    'Kentucky': {'cities': ['Louisville'], 'abbr': 'KY'},
    'Maryland': {'cities': ['Baltimore'], 'abbr': 'MD'},
    'Massachusetts': {'cities': ['Boston'], 'abbr': 'MA'},
    'Michigan': {'cities': ['Detroit'], 'abbr': 'MI'},
    'Minnesota': {'cities': ['Minneapolis'], 'abbr': 'MN'},
    'Missouri': {'cities': ['St. Louis', 'Kansas City'], 'abbr': 'MO'},
    'Nevada': {'cities': ['Las Vegas'], 'abbr': 'NV'},
    'New Mexico': {'cities': ['Albuquerque'], 'abbr': 'NM'},
    'New York': {'cities': ['New York City'], 'abbr': 'NY'},
    'North Carolina': {'cities': ['Charlotte', 'Raleigh'], 'abbr': 'NC'},
    'Ohio': {'cities': ['Columbus', 'Cleveland', 'Cincinnati'], 'abbr': 'OH'},
    'Oklahoma': {'cities': ['Oklahoma City'], 'abbr': 'OK'},
    'Oregon': {'cities': ['Portland'], 'abbr': 'OR'},
    'Pennsylvania': {'cities': ['Philadelphia', 'Pittsburgh'], 'abbr': 'PA'},
    'Tennessee': {'cities': ['Nashville', 'Memphis'], 'abbr': 'TN'},
    'Texas': {'cities': ['Houston', 'San Antonio', 'Dallas', 'Austin', 'Fort Worth'], 'abbr': 'TX'},
    'Utah': {'cities': ['Salt Lake City'], 'abbr': 'UT'},
    'Washington': {'cities': ['Seattle'], 'abbr': 'WA'},
    'Washington DC': {'cities': ['Washington'], 'abbr': 'DC'},
    'Wisconsin': {'cities': ['Milwaukee'], 'abbr': 'WI'},
}

def slugify(text):
    """Convert text to URL-friendly slug"""
    text = text.lower()
    text = re.sub(r'[^a-z0-9\s-]', '', text)
    text = re.sub(r'[\s_]+', '-', text)
    text = re.sub(r'-+', '-', text)
    return text.strip('-')

def create_directories():
    """Create all necessary directories"""
    base_path = '/home/ubuntu/stem-cells/locations'
    
    for state, data in STATES_DATA.items():
        state_slug = slugify(state)
        state_path = os.path.join(base_path, state_slug)
        os.makedirs(state_path, exist_ok=True)
        
        for city in data['cities']:
            city_slug = slugify(city)
            city_path = os.path.join(state_path, city_slug)
            os.makedirs(city_path, exist_ok=True)
    
    print(f"Created directories for {len(STATES_DATA)} states")

def get_all_locations():
    """Return list of all states and cities for image generation"""
    locations = {
        'states': list(STATES_DATA.keys()),
        'cities': []
    }
    for state, data in STATES_DATA.items():
        for city in data['cities']:
            locations['cities'].append({'city': city, 'state': state})
    return locations

if __name__ == '__main__':
    create_directories()
    locations = get_all_locations()
    print(f"States: {len(locations['states'])}")
    print(f"Cities: {len(locations['cities'])}")
    
    # Save locations for reference
    with open('/home/ubuntu/stem-cells/locations_data.json', 'w') as f:
        json.dump(locations, f, indent=2)
    print("Saved locations_data.json")
