#!/usr/bin/env python3
"""
Fix SEO content formatting and add proper internal links
"""

import os
import re
from pathlib import Path

# State data with cities and neighboring states for interlinking
STATE_DATA = {
    "alaska": {"name": "Alaska", "cities": ["anchorage"], "neighbors": ["washington"], "abbrev": "AK"},
    "arizona": {"name": "Arizona", "cities": ["phoenix", "scottsdale", "tucson"], "neighbors": ["california", "nevada", "new-mexico", "colorado", "utah"], "abbrev": "AZ"},
    "california": {"name": "California", "cities": ["los-angeles", "san-diego", "san-jose", "san-francisco", "fresno", "sacramento"], "neighbors": ["arizona", "nevada", "oregon"], "abbrev": "CA"},
    "colorado": {"name": "Colorado", "cities": ["denver"], "neighbors": ["arizona", "new-mexico", "utah", "kansas", "nebraska", "wyoming"], "abbrev": "CO"},
    "florida": {"name": "Florida", "cities": ["miami", "tampa", "orlando", "jacksonville"], "neighbors": ["georgia"], "abbrev": "FL"},
    "georgia": {"name": "Georgia", "cities": ["atlanta"], "neighbors": ["florida", "tennessee", "north-carolina"], "abbrev": "GA"},
    "hawaii": {"name": "Hawaii", "cities": ["honolulu"], "neighbors": ["california"], "abbrev": "HI"},
    "idaho": {"name": "Idaho", "cities": ["boise"], "neighbors": ["washington", "oregon", "nevada", "utah", "montana", "wyoming"], "abbrev": "ID"},
    "illinois": {"name": "Illinois", "cities": ["chicago"], "neighbors": ["indiana", "wisconsin", "missouri", "iowa", "kentucky"], "abbrev": "IL"},
    "indiana": {"name": "Indiana", "cities": ["indianapolis"], "neighbors": ["illinois", "michigan", "ohio", "kentucky"], "abbrev": "IN"},
    "kentucky": {"name": "Kentucky", "cities": ["louisville"], "neighbors": ["tennessee", "indiana", "ohio", "illinois", "missouri", "virginia", "west-virginia"], "abbrev": "KY"},
    "maryland": {"name": "Maryland", "cities": ["baltimore"], "neighbors": ["pennsylvania", "virginia", "washington-dc"], "abbrev": "MD"},
    "massachusetts": {"name": "Massachusetts", "cities": ["boston"], "neighbors": ["new-york", "connecticut", "rhode-island", "new-hampshire", "vermont"], "abbrev": "MA"},
    "michigan": {"name": "Michigan", "cities": ["detroit"], "neighbors": ["indiana", "ohio", "wisconsin"], "abbrev": "MI"},
    "minnesota": {"name": "Minnesota", "cities": ["minneapolis"], "neighbors": ["wisconsin", "iowa", "north-dakota", "south-dakota"], "abbrev": "MN"},
    "missouri": {"name": "Missouri", "cities": ["st-louis", "kansas-city"], "neighbors": ["illinois", "kansas", "oklahoma", "tennessee", "kentucky", "iowa", "nebraska", "arkansas"], "abbrev": "MO"},
    "nevada": {"name": "Nevada", "cities": ["las-vegas", "reno"], "neighbors": ["california", "arizona", "utah", "oregon", "idaho"], "abbrev": "NV"},
    "new-mexico": {"name": "New Mexico", "cities": ["albuquerque", "santa-fe"], "neighbors": ["arizona", "colorado", "texas", "oklahoma"], "abbrev": "NM"},
    "new-york": {"name": "New York", "cities": ["new-york-city"], "neighbors": ["pennsylvania", "new-jersey", "massachusetts", "connecticut", "vermont"], "abbrev": "NY"},
    "north-carolina": {"name": "North Carolina", "cities": ["charlotte", "raleigh"], "neighbors": ["georgia", "tennessee", "virginia", "south-carolina"], "abbrev": "NC"},
    "ohio": {"name": "Ohio", "cities": ["columbus", "cleveland"], "neighbors": ["michigan", "indiana", "kentucky", "pennsylvania", "west-virginia"], "abbrev": "OH"},
    "oklahoma": {"name": "Oklahoma", "cities": ["oklahoma-city", "tulsa"], "neighbors": ["texas", "kansas", "colorado", "new-mexico", "missouri", "arkansas"], "abbrev": "OK"},
    "oregon": {"name": "Oregon", "cities": ["portland"], "neighbors": ["california", "washington", "nevada", "idaho"], "abbrev": "OR"},
    "pennsylvania": {"name": "Pennsylvania", "cities": ["philadelphia", "pittsburgh"], "neighbors": ["new-york", "ohio", "new-jersey", "maryland", "west-virginia"], "abbrev": "PA"},
    "tennessee": {"name": "Tennessee", "cities": ["nashville", "memphis"], "neighbors": ["georgia", "kentucky", "north-carolina", "virginia", "missouri", "arkansas", "mississippi", "alabama"], "abbrev": "TN"},
    "texas": {"name": "Texas", "cities": ["houston", "dallas", "austin", "san-antonio"], "neighbors": ["new-mexico", "oklahoma", "louisiana", "arkansas"], "abbrev": "TX"},
    "utah": {"name": "Utah", "cities": ["salt-lake-city"], "neighbors": ["arizona", "colorado", "nevada", "idaho", "wyoming"], "abbrev": "UT"},
    "washington": {"name": "Washington", "cities": ["seattle"], "neighbors": ["oregon", "idaho"], "abbrev": "WA"},
    "washington-dc": {"name": "Washington DC", "cities": [], "neighbors": ["maryland", "virginia"], "abbrev": "DC"},
    "wisconsin": {"name": "Wisconsin", "cities": ["milwaukee", "madison"], "neighbors": ["illinois", "michigan", "minnesota", "iowa"], "abbrev": "WI"},
}

def format_city_name(slug):
    """Convert slug to proper city name"""
    special_names = {
        "los-angeles": "Los Angeles",
        "san-diego": "San Diego",
        "san-jose": "San Jose",
        "san-francisco": "San Francisco",
        "san-antonio": "San Antonio",
        "new-york-city": "New York City",
        "las-vegas": "Las Vegas",
        "salt-lake-city": "Salt Lake City",
        "kansas-city": "Kansas City",
        "st-louis": "St. Louis",
        "oklahoma-city": "Oklahoma City",
        "santa-fe": "Santa Fe",
        "washington-dc": "Washington DC",
    }
    return special_names.get(slug, slug.replace("-", " ").title())

def format_state_name(slug):
    """Convert slug to proper state name"""
    special_names = {
        "washington-dc": "Washington DC",
        "new-york": "New York",
        "new-mexico": "New Mexico",
        "north-carolina": "North Carolina",
    }
    return special_names.get(slug, slug.replace("-", " ").title())

def get_state_seo_content(state_slug, state_data):
    """Generate beautifully formatted SEO content for state pages"""
    state_name = state_data["name"]
    cities = state_data["cities"]
    neighbors = state_data["neighbors"]
    
    # Format city names for display
    city_names = [format_city_name(c) for c in cities]
    city_links = [f'<a href="/locations/{state_slug}/{c}/" class="text-blue-600 hover:text-blue-800 hover:underline">{format_city_name(c)}</a>' for c in cities]
    
    # Format neighbor links
    neighbor_links = []
    for n in neighbors[:3]:  # Limit to 3 neighbors
        if n in STATE_DATA:
            neighbor_links.append(f'<a href="/locations/{n}/" class="text-blue-600 hover:text-blue-800 hover:underline">{STATE_DATA[n]["name"]}</a>')
    
    cities_text = ", ".join(city_links[:-1]) + (f", and {city_links[-1]}" if len(city_links) > 1 else city_links[0] if city_links else "major cities")
    neighbors_text = ", ".join(neighbor_links) if neighbor_links else "neighboring states"
    
    content = f'''
    <!-- SEO Content Section -->
    <div class="bg-gradient-to-b from-gray-50 to-white py-16">
        <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
            <div class="max-w-4xl mx-auto">
                <h2 class="text-3xl font-bold text-gray-900 mb-6">Understanding Stem Cell Therapy in {state_name}</h2>
                <p class="text-gray-600 leading-relaxed mb-6">
                    {state_name} offers a growing network of stem cell clinics providing advanced regenerative medicine treatments. 
                    With facilities in {cities_text}, patients have access to cutting-edge therapies for conditions ranging from 
                    orthopedic injuries to degenerative diseases. The state's medical community continues to embrace innovative 
                    treatment protocols while maintaining strict safety standards.
                </p>
                <p class="text-gray-600 leading-relaxed mb-8">
                    Stem cell therapy in {state_name} typically involves the use of autologous cells (from the patient's own body) 
                    or allogeneic cells (from donors) to promote tissue repair and reduce inflammation. These treatments are 
                    particularly popular for joint conditions, sports injuries, and chronic pain management.
                </p>
                
                <div class="bg-white rounded-xl shadow-sm border border-gray-100 p-6 mb-8">
                    <h3 class="text-xl font-semibold text-gray-900 mb-4 flex items-center">
                        <svg class="w-6 h-6 text-blue-600 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8c-1.657 0-3 .895-3 2s1.343 2 3 2 3 .895 3 2-1.343 2-3 2m0-8c1.11 0 2.08.402 2.599 1M12 8V7m0 1v8m0 0v1m0-1c-1.11 0-2.08-.402-2.599-1M21 12a9 9 0 11-18 0 9 9 0 0118 0z"></path>
                        </svg>
                        Cost of Treatment in {state_name}
                    </h3>
                    <p class="text-gray-600 leading-relaxed mb-4">
                        Stem cell therapy costs in {state_name} typically range from <span class="font-semibold text-blue-600">$4,000 to $12,000</span> 
                        per treatment, depending on the procedure type, clinic location, and complexity of the condition being treated. 
                        Factors such as the source of stem cells, number of injections required, and facility fees all contribute to the final cost.
                    </p>
                    <p class="text-gray-600 leading-relaxed">
                        For patients seeking more affordable options, 
                        <a href="/locations/mexico/" class="text-blue-600 hover:text-blue-800 hover:underline font-medium">stem cell clinics in Mexico</a> 
                        offer comparable treatments at 40-60% lower costs, making medical tourism an attractive alternative for many patients.
                    </p>
                </div>
                
                <h3 class="text-xl font-semibold text-gray-900 mb-4">Popular Treatments Available</h3>
                <div class="grid grid-cols-1 md:grid-cols-2 gap-4 mb-8">
                    <div class="flex items-start p-4 bg-white rounded-lg border border-gray-100 hover:border-blue-200 transition-colors">
                        <div class="flex-shrink-0 w-10 h-10 bg-blue-100 rounded-lg flex items-center justify-center mr-4">
                            <svg class="w-5 h-5 text-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"></path>
                            </svg>
                        </div>
                        <div>
                            <h4 class="font-medium text-gray-900">Knee Osteoarthritis</h4>
                            <p class="text-sm text-gray-500">Cartilage regeneration and pain relief</p>
                        </div>
                    </div>
                    <div class="flex items-start p-4 bg-white rounded-lg border border-gray-100 hover:border-blue-200 transition-colors">
                        <div class="flex-shrink-0 w-10 h-10 bg-blue-100 rounded-lg flex items-center justify-center mr-4">
                            <svg class="w-5 h-5 text-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"></path>
                            </svg>
                        </div>
                        <div>
                            <h4 class="font-medium text-gray-900">Spine & Back Pain</h4>
                            <p class="text-sm text-gray-500">Disc regeneration and spinal treatments</p>
                        </div>
                    </div>
                    <div class="flex items-start p-4 bg-white rounded-lg border border-gray-100 hover:border-blue-200 transition-colors">
                        <div class="flex-shrink-0 w-10 h-10 bg-blue-100 rounded-lg flex items-center justify-center mr-4">
                            <svg class="w-5 h-5 text-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"></path>
                            </svg>
                        </div>
                        <div>
                            <h4 class="font-medium text-gray-900">Sports Injuries</h4>
                            <p class="text-sm text-gray-500">Tendon, ligament, and muscle repair</p>
                        </div>
                    </div>
                    <div class="flex items-start p-4 bg-white rounded-lg border border-gray-100 hover:border-blue-200 transition-colors">
                        <div class="flex-shrink-0 w-10 h-10 bg-blue-100 rounded-lg flex items-center justify-center mr-4">
                            <svg class="w-5 h-5 text-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"></path>
                            </svg>
                        </div>
                        <div>
                            <h4 class="font-medium text-gray-900">Hip & Shoulder</h4>
                            <p class="text-sm text-gray-500">Joint preservation and mobility</p>
                        </div>
                    </div>
                </div>
                
                <h3 class="text-xl font-semibold text-gray-900 mb-4">Explore More Options</h3>
                <p class="text-gray-600 leading-relaxed mb-4">
                    Looking for stem cell therapy options beyond {state_name}? Explore clinics in {neighbors_text}, 
                    or discover significant cost savings with our 
                    <a href="/locations/mexico/" class="text-blue-600 hover:text-blue-800 hover:underline font-medium">Mexico clinic directory</a>. 
                    You can also <a href="/compare-costs/" class="text-blue-600 hover:text-blue-800 hover:underline font-medium">compare treatment costs</a> 
                    across different locations to find the best value for your needs.
                </p>
                <div class="flex flex-wrap gap-2 mt-4">
                    <a href="/locations/" class="inline-flex items-center px-4 py-2 bg-gray-100 hover:bg-gray-200 text-gray-700 rounded-full text-sm font-medium transition-colors">
                        All Locations
                    </a>
                    <a href="/locations/mexico/" class="inline-flex items-center px-4 py-2 bg-blue-100 hover:bg-blue-200 text-blue-700 rounded-full text-sm font-medium transition-colors">
                        Mexico Clinics
                    </a>
                    <a href="/compare-costs/" class="inline-flex items-center px-4 py-2 bg-gray-100 hover:bg-gray-200 text-gray-700 rounded-full text-sm font-medium transition-colors">
                        Compare Costs
                    </a>
                </div>
            </div>
        </div>
    </div>
'''
    return content

def get_city_seo_content(state_slug, city_slug, state_data):
    """Generate beautifully formatted SEO content for city pages"""
    state_name = state_data["name"]
    city_name = format_city_name(city_slug)
    cities = state_data["cities"]
    
    # Get other cities in the same state for interlinking
    other_cities = [c for c in cities if c != city_slug]
    other_city_links = [f'<a href="/locations/{state_slug}/{c}/" class="text-blue-600 hover:text-blue-800 hover:underline">{format_city_name(c)}</a>' for c in other_cities[:3]]
    other_cities_text = ", ".join(other_city_links) if other_city_links else ""
    
    content = f'''
    <!-- SEO Content Section -->
    <div class="bg-gradient-to-b from-gray-50 to-white py-16">
        <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
            <div class="max-w-4xl mx-auto">
                <h2 class="text-3xl font-bold text-gray-900 mb-6">Stem Cell Therapy in {city_name}</h2>
                <p class="text-gray-600 leading-relaxed mb-6">
                    {city_name}, {state_name} is home to several reputable stem cell clinics offering advanced regenerative 
                    medicine treatments. Local providers specialize in treating orthopedic conditions, sports injuries, 
                    and degenerative diseases using cutting-edge stem cell technology. Whether you're dealing with chronic 
                    joint pain or recovering from an injury, {city_name}'s medical facilities offer personalized treatment plans.
                </p>
                <p class="text-gray-600 leading-relaxed mb-8">
                    Patients in {city_name} benefit from access to board-certified physicians, state-of-the-art facilities, 
                    and comprehensive care protocols. Many clinics offer free consultations to help you understand your 
                    treatment options and expected outcomes.
                </p>
                
                <div class="bg-white rounded-xl shadow-sm border border-gray-100 p-6 mb-8">
                    <h3 class="text-xl font-semibold text-gray-900 mb-4 flex items-center">
                        <svg class="w-6 h-6 text-blue-600 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8c-1.657 0-3 .895-3 2s1.343 2 3 2 3 .895 3 2-1.343 2-3 2m0-8c1.11 0 2.08.402 2.599 1M12 8V7m0 1v8m0 0v1m0-1c-1.11 0-2.08-.402-2.599-1M21 12a9 9 0 11-18 0 9 9 0 0118 0z"></path>
                        </svg>
                        Treatment Costs in {city_name}
                    </h3>
                    <p class="text-gray-600 leading-relaxed mb-4">
                        Stem cell therapy in {city_name} typically costs between <span class="font-semibold text-blue-600">$3,500 to $10,000</span> 
                        per treatment session. Prices vary based on the type of procedure, the clinic's expertise, and the 
                        complexity of your condition. Many clinics offer financing options to make treatment more accessible.
                    </p>
                    <p class="text-gray-600 leading-relaxed">
                        Looking for more affordable options? 
                        <a href="/locations/mexico/" class="text-blue-600 hover:text-blue-800 hover:underline font-medium">Stem cell clinics in Mexico</a> 
                        offer similar treatments at significantly lower costs, with many patients saving 50% or more compared to US prices.
                    </p>
                </div>
                
                <h3 class="text-xl font-semibold text-gray-900 mb-4">What to Expect</h3>
                <div class="space-y-4 mb-8">
                    <div class="flex items-start">
                        <div class="flex-shrink-0 w-8 h-8 bg-blue-600 text-white rounded-full flex items-center justify-center font-semibold text-sm mr-4">1</div>
                        <div>
                            <h4 class="font-medium text-gray-900">Initial Consultation</h4>
                            <p class="text-sm text-gray-500">Meet with a specialist to discuss your condition and treatment options</p>
                        </div>
                    </div>
                    <div class="flex items-start">
                        <div class="flex-shrink-0 w-8 h-8 bg-blue-600 text-white rounded-full flex items-center justify-center font-semibold text-sm mr-4">2</div>
                        <div>
                            <h4 class="font-medium text-gray-900">Treatment Planning</h4>
                            <p class="text-sm text-gray-500">Receive a personalized treatment plan based on your specific needs</p>
                        </div>
                    </div>
                    <div class="flex items-start">
                        <div class="flex-shrink-0 w-8 h-8 bg-blue-600 text-white rounded-full flex items-center justify-center font-semibold text-sm mr-4">3</div>
                        <div>
                            <h4 class="font-medium text-gray-900">Procedure Day</h4>
                            <p class="text-sm text-gray-500">Most stem cell procedures are outpatient and take 1-2 hours</p>
                        </div>
                    </div>
                    <div class="flex items-start">
                        <div class="flex-shrink-0 w-8 h-8 bg-blue-600 text-white rounded-full flex items-center justify-center font-semibold text-sm mr-4">4</div>
                        <div>
                            <h4 class="font-medium text-gray-900">Recovery & Follow-up</h4>
                            <p class="text-sm text-gray-500">Minimal downtime with follow-up appointments to track progress</p>
                        </div>
                    </div>
                </div>
                
                <h3 class="text-xl font-semibold text-gray-900 mb-4">Explore More Clinics</h3>
                <p class="text-gray-600 leading-relaxed mb-4">
                    Browse more stem cell clinics in <a href="/locations/{state_slug}/" class="text-blue-600 hover:text-blue-800 hover:underline font-medium">{state_name}</a>'''
    
    if other_cities_text:
        content += f''', including facilities in {other_cities_text}'''
    
    content += f'''. 
                    For significant cost savings, explore our 
                    <a href="/locations/mexico/" class="text-blue-600 hover:text-blue-800 hover:underline font-medium">Mexico clinic directory</a> 
                    where treatments can cost 50-70% less than US prices.
                </p>
                <div class="flex flex-wrap gap-2 mt-4">
                    <a href="/locations/{state_slug}/" class="inline-flex items-center px-4 py-2 bg-blue-100 hover:bg-blue-200 text-blue-700 rounded-full text-sm font-medium transition-colors">
                        All {state_name} Clinics
                    </a>
                    <a href="/locations/mexico/" class="inline-flex items-center px-4 py-2 bg-green-100 hover:bg-green-200 text-green-700 rounded-full text-sm font-medium transition-colors">
                        Mexico Clinics
                    </a>
                    <a href="/compare-costs/" class="inline-flex items-center px-4 py-2 bg-gray-100 hover:bg-gray-200 text-gray-700 rounded-full text-sm font-medium transition-colors">
                        Compare Costs
                    </a>
                </div>
            </div>
        </div>
    </div>
'''
    return content

def update_state_page(state_slug):
    """Update a state page with new formatted SEO content"""
    file_path = Path(f"locations/{state_slug}/index.html")
    if not file_path.exists():
        print(f"  Skipping {state_slug} - file not found")
        return False
    
    if state_slug not in STATE_DATA:
        print(f"  Skipping {state_slug} - not in state data")
        return False
    
    content = file_path.read_text()
    
    # Remove old SEO content section
    pattern = r'<!-- SEO Content Section -->.*?</div>\s*</div>\s*</div>\s*(?=<div class="bg-amber-50)'
    new_seo_content = get_state_seo_content(state_slug, STATE_DATA[state_slug])
    
    if re.search(pattern, content, re.DOTALL):
        content = re.sub(pattern, new_seo_content + '\n\n    ', content, flags=re.DOTALL)
    else:
        # Insert before the medical disclaimer
        disclaimer_pattern = r'(<div class="bg-amber-50 border-l-4 border-amber-400)'
        content = re.sub(disclaimer_pattern, new_seo_content + '\n\n    \\1', content)
    
    file_path.write_text(content)
    return True

def update_city_page(state_slug, city_slug):
    """Update a city page with new formatted SEO content"""
    file_path = Path(f"locations/{state_slug}/{city_slug}/index.html")
    if not file_path.exists():
        print(f"  Skipping {state_slug}/{city_slug} - file not found")
        return False
    
    if state_slug not in STATE_DATA:
        print(f"  Skipping {state_slug}/{city_slug} - state not in data")
        return False
    
    content = file_path.read_text()
    
    # Remove old SEO content section
    pattern = r'<!-- SEO Content Section -->.*?</div>\s*</div>\s*</div>\s*(?=<div class="bg-amber-50)'
    new_seo_content = get_city_seo_content(state_slug, city_slug, STATE_DATA[state_slug])
    
    if re.search(pattern, content, re.DOTALL):
        content = re.sub(pattern, new_seo_content + '\n\n    ', content, flags=re.DOTALL)
    else:
        # Insert before the medical disclaimer
        disclaimer_pattern = r'(<div class="bg-amber-50 border-l-4 border-amber-400)'
        content = re.sub(disclaimer_pattern, new_seo_content + '\n\n    \\1', content)
    
    file_path.write_text(content)
    return True

def main():
    os.chdir("/home/ubuntu/stem-cells")
    
    print("Updating state pages with formatted SEO content...")
    state_count = 0
    for state_slug in STATE_DATA.keys():
        if update_state_page(state_slug):
            state_count += 1
            print(f"  Updated: {state_slug}")
    
    print(f"\nUpdated {state_count} state pages")
    
    print("\nUpdating city pages with formatted SEO content...")
    city_count = 0
    for state_slug, data in STATE_DATA.items():
        for city_slug in data["cities"]:
            if update_city_page(state_slug, city_slug):
                city_count += 1
                print(f"  Updated: {state_slug}/{city_slug}")
    
    print(f"\nUpdated {city_count} city pages")
    print(f"\nTotal pages updated: {state_count + city_count}")

if __name__ == "__main__":
    main()
