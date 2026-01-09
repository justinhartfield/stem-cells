#!/usr/bin/env python3
"""
Generate and inject SEO content into state and city landing pages.
Adds approximately 500 words of customized content with H1/H2 structure,
region-specific information, and internal links.
"""

import os
import re
from openai import OpenAI

# Initialize OpenAI client
client = OpenAI()

# State data with SEO information
STATE_DATA = {
    "alaska": {
        "name": "Alaska",
        "abbrev": "AK",
        "cities": ["Anchorage"],
        "avg_price_low": 4000,
        "avg_price_high": 12000,
        "regulation_level": "minimal",
        "popular_treatments": ["Knee Osteoarthritis", "Back Pain", "Joint Injuries"],
        "nearby_states": ["Washington"],
        "unique_factors": "Remote location means fewer clinics but highly specialized providers. Many Alaskans travel to Seattle or consider medical tourism to Mexico for more options.",
    },
    "arizona": {
        "name": "Arizona",
        "abbrev": "AZ",
        "cities": ["Phoenix", "Scottsdale", "Tucson"],
        "avg_price_low": 3500,
        "avg_price_high": 10000,
        "regulation_level": "moderate",
        "popular_treatments": ["Knee Osteoarthritis", "Shoulder Injuries", "Hip Pain", "Sports Injuries"],
        "nearby_states": ["California", "Nevada", "New Mexico"],
        "unique_factors": "Arizona is a hub for regenerative medicine with Scottsdale being known as a premier destination. Warm, dry climate supports year-round rehabilitation.",
    },
    "california": {
        "name": "California",
        "abbrev": "CA",
        "cities": ["Los Angeles", "San Diego", "San Francisco", "San Jose", "Fresno", "Sacramento"],
        "avg_price_low": 4000,
        "avg_price_high": 15000,
        "regulation_level": "strict",
        "popular_treatments": ["Knee Osteoarthritis", "Spine/Disc Issues", "Sports Injuries", "Anti-Aging"],
        "nearby_states": ["Arizona", "Nevada", "Oregon"],
        "unique_factors": "California has the most stem cell clinics in the US with cutting-edge research institutions. San Diego is close to Tijuana for medical tourism options.",
    },
    "colorado": {
        "name": "Colorado",
        "abbrev": "CO",
        "cities": ["Denver"],
        "avg_price_low": 3500,
        "avg_price_high": 9000,
        "regulation_level": "moderate",
        "popular_treatments": ["Knee Osteoarthritis", "Sports Injuries", "Skiing Injuries", "Joint Pain"],
        "nearby_states": ["Utah", "Arizona", "New Mexico"],
        "unique_factors": "Colorado attracts athletes and outdoor enthusiasts seeking regenerative treatments for sports injuries. Denver has several reputable orthopedic stem cell clinics.",
    },
    "florida": {
        "name": "Florida",
        "abbrev": "FL",
        "cities": ["Miami", "Tampa", "Orlando", "Jacksonville"],
        "avg_price_low": 3500,
        "avg_price_high": 12000,
        "regulation_level": "moderate",
        "popular_treatments": ["Knee Osteoarthritis", "Hip Replacement Alternative", "Anti-Aging", "Joint Pain"],
        "nearby_states": ["Georgia"],
        "unique_factors": "Florida is a major destination for stem cell therapy, particularly for retirees. Miami has luxury clinics catering to international patients.",
    },
    "georgia": {
        "name": "Georgia",
        "abbrev": "GA",
        "cities": ["Atlanta"],
        "avg_price_low": 3500,
        "avg_price_high": 10000,
        "regulation_level": "moderate",
        "popular_treatments": ["Knee Osteoarthritis", "Back Pain", "Joint Injuries"],
        "nearby_states": ["Florida", "Tennessee", "North Carolina"],
        "unique_factors": "Atlanta is the Southeast's medical hub with access to Emory University research. Growing number of regenerative medicine clinics serving the region.",
    },
    "hawaii": {
        "name": "Hawaii",
        "abbrev": "HI",
        "cities": ["Honolulu"],
        "avg_price_low": 5000,
        "avg_price_high": 15000,
        "regulation_level": "moderate",
        "popular_treatments": ["Knee Osteoarthritis", "Sports Injuries", "Joint Pain"],
        "nearby_states": [],
        "unique_factors": "Limited options due to island location. Higher prices reflect isolation. Many Hawaii residents travel to California or consider medical tourism for stem cell treatments.",
    },
    "idaho": {
        "name": "Idaho",
        "abbrev": "ID",
        "cities": ["Boise"],
        "avg_price_low": 3500,
        "avg_price_high": 9000,
        "regulation_level": "minimal",
        "popular_treatments": ["Knee Osteoarthritis", "Back Pain", "Joint Injuries"],
        "nearby_states": ["Utah", "Washington", "Oregon"],
        "unique_factors": "Growing regenerative medicine market. Boise has several quality clinics. Some patients travel to Salt Lake City or Seattle for more options.",
    },
    "illinois": {
        "name": "Illinois",
        "abbrev": "IL",
        "cities": ["Chicago"],
        "avg_price_low": 4000,
        "avg_price_high": 12000,
        "regulation_level": "strict",
        "popular_treatments": ["Knee Osteoarthritis", "Back Pain", "Sports Injuries", "Joint Pain"],
        "nearby_states": ["Indiana", "Wisconsin", "Michigan"],
        "unique_factors": "Chicago is a major medical hub with access to Northwestern, Rush, and University of Chicago medical centers. Strong research presence in regenerative medicine.",
    },
    "indiana": {
        "name": "Indiana",
        "abbrev": "IN",
        "cities": ["Indianapolis"],
        "avg_price_low": 3500,
        "avg_price_high": 9000,
        "regulation_level": "moderate",
        "popular_treatments": ["Knee Osteoarthritis", "Back Pain", "Joint Injuries"],
        "nearby_states": ["Illinois", "Ohio", "Kentucky"],
        "unique_factors": "Indianapolis has quality orthopedic clinics with competitive pricing. Central location makes it accessible from surrounding states.",
    },
    "kentucky": {
        "name": "Kentucky",
        "abbrev": "KY",
        "cities": ["Louisville"],
        "avg_price_low": 3000,
        "avg_price_high": 8000,
        "regulation_level": "moderate",
        "popular_treatments": ["Knee Osteoarthritis", "Back Pain", "Joint Injuries"],
        "nearby_states": ["Indiana", "Ohio", "Tennessee"],
        "unique_factors": "Louisville offers quality care at competitive Midwest prices. Growing regenerative medicine market serving Kentucky and surrounding states.",
    },
    "maryland": {
        "name": "Maryland",
        "abbrev": "MD",
        "cities": ["Baltimore"],
        "avg_price_low": 4500,
        "avg_price_high": 12000,
        "regulation_level": "strict",
        "popular_treatments": ["Knee Osteoarthritis", "Back Pain", "Sports Injuries"],
        "nearby_states": ["Pennsylvania", "Virginia"],
        "unique_factors": "Proximity to Johns Hopkins and NIH provides access to cutting-edge research. Baltimore has several reputable regenerative medicine clinics.",
    },
    "massachusetts": {
        "name": "Massachusetts",
        "abbrev": "MA",
        "cities": ["Boston"],
        "avg_price_low": 5000,
        "avg_price_high": 15000,
        "regulation_level": "strict",
        "popular_treatments": ["Knee Osteoarthritis", "Sports Injuries", "Joint Pain"],
        "nearby_states": ["New York", "Connecticut"],
        "unique_factors": "Boston is a world-renowned medical hub with Harvard, MIT, and numerous teaching hospitals. Access to clinical trials and cutting-edge treatments, but higher prices.",
    },
    "michigan": {
        "name": "Michigan",
        "abbrev": "MI",
        "cities": ["Detroit"],
        "avg_price_low": 3500,
        "avg_price_high": 10000,
        "regulation_level": "moderate",
        "popular_treatments": ["Knee Osteoarthritis", "Back Pain", "Sports Injuries"],
        "nearby_states": ["Ohio", "Indiana", "Illinois"],
        "unique_factors": "Detroit area has quality orthopedic clinics with competitive Midwest pricing. University of Michigan provides research opportunities.",
    },
    "minnesota": {
        "name": "Minnesota",
        "abbrev": "MN",
        "cities": ["Minneapolis"],
        "avg_price_low": 4000,
        "avg_price_high": 12000,
        "regulation_level": "strict",
        "popular_treatments": ["Knee Osteoarthritis", "Back Pain", "Sports Injuries"],
        "nearby_states": ["Wisconsin", "Iowa"],
        "unique_factors": "Home to Mayo Clinic, one of the world's premier medical institutions. Minneapolis-St. Paul has excellent regenerative medicine options.",
    },
    "missouri": {
        "name": "Missouri",
        "abbrev": "MO",
        "cities": ["St. Louis", "Kansas City"],
        "avg_price_low": 3500,
        "avg_price_high": 9000,
        "regulation_level": "moderate",
        "popular_treatments": ["Knee Osteoarthritis", "Back Pain", "Joint Injuries"],
        "nearby_states": ["Illinois", "Kansas", "Oklahoma"],
        "unique_factors": "St. Louis and Kansas City both offer quality stem cell clinics at competitive Midwest prices. Washington University provides research opportunities.",
    },
    "nevada": {
        "name": "Nevada",
        "abbrev": "NV",
        "cities": ["Las Vegas"],
        "avg_price_low": 4000,
        "avg_price_high": 11000,
        "regulation_level": "moderate",
        "popular_treatments": ["Knee Osteoarthritis", "Sports Injuries", "Anti-Aging"],
        "nearby_states": ["California", "Arizona", "Utah"],
        "unique_factors": "Las Vegas has become a medical tourism destination with luxury clinics. Attracts patients from across the country seeking treatment combined with travel.",
    },
    "new-mexico": {
        "name": "New Mexico",
        "abbrev": "NM",
        "cities": ["Albuquerque"],
        "avg_price_low": 3500,
        "avg_price_high": 9000,
        "regulation_level": "minimal",
        "popular_treatments": ["Knee Osteoarthritis", "Back Pain", "Joint Injuries"],
        "nearby_states": ["Arizona", "Colorado", "Texas"],
        "unique_factors": "Albuquerque has growing regenerative medicine options. Some patients travel to Phoenix or Denver for more choices.",
    },
    "new-york": {
        "name": "New York",
        "abbrev": "NY",
        "cities": ["New York City"],
        "avg_price_low": 5000,
        "avg_price_high": 18000,
        "regulation_level": "strict",
        "popular_treatments": ["Knee Osteoarthritis", "Sports Injuries", "Anti-Aging", "Joint Pain"],
        "nearby_states": ["New Jersey", "Connecticut", "Pennsylvania"],
        "unique_factors": "NYC has world-class medical facilities including Hospital for Special Surgery and NYU Langone. Premium pricing but access to top specialists.",
    },
    "north-carolina": {
        "name": "North Carolina",
        "abbrev": "NC",
        "cities": ["Charlotte", "Raleigh"],
        "avg_price_low": 3500,
        "avg_price_high": 10000,
        "regulation_level": "moderate",
        "popular_treatments": ["Knee Osteoarthritis", "Back Pain", "Sports Injuries"],
        "nearby_states": ["Virginia", "South Carolina", "Tennessee"],
        "unique_factors": "Charlotte and Raleigh-Durham both have quality regenerative medicine clinics. Duke University provides research opportunities.",
    },
    "ohio": {
        "name": "Ohio",
        "abbrev": "OH",
        "cities": ["Columbus", "Cleveland", "Cincinnati"],
        "avg_price_low": 3500,
        "avg_price_high": 10000,
        "regulation_level": "moderate",
        "popular_treatments": ["Knee Osteoarthritis", "Back Pain", "Sports Injuries"],
        "nearby_states": ["Pennsylvania", "Michigan", "Indiana", "Kentucky"],
        "unique_factors": "Cleveland Clinic is world-renowned for orthopedic care. Multiple major cities offer competitive options.",
    },
    "oklahoma": {
        "name": "Oklahoma",
        "abbrev": "OK",
        "cities": ["Oklahoma City"],
        "avg_price_low": 3000,
        "avg_price_high": 8000,
        "regulation_level": "minimal",
        "popular_treatments": ["Knee Osteoarthritis", "Back Pain", "Joint Injuries"],
        "nearby_states": ["Texas", "Kansas", "Arkansas"],
        "unique_factors": "Oklahoma City has growing regenerative medicine options at competitive prices. Among the most affordable markets in the US.",
    },
    "oregon": {
        "name": "Oregon",
        "abbrev": "OR",
        "cities": ["Portland"],
        "avg_price_low": 4000,
        "avg_price_high": 11000,
        "regulation_level": "moderate",
        "popular_treatments": ["Knee Osteoarthritis", "Sports Injuries", "Joint Pain"],
        "nearby_states": ["Washington", "California", "Idaho"],
        "unique_factors": "Portland has quality regenerative medicine clinics serving the Pacific Northwest. OHSU provides research opportunities.",
    },
    "pennsylvania": {
        "name": "Pennsylvania",
        "abbrev": "PA",
        "cities": ["Philadelphia", "Pittsburgh"],
        "avg_price_low": 4000,
        "avg_price_high": 12000,
        "regulation_level": "strict",
        "popular_treatments": ["Knee Osteoarthritis", "Back Pain", "Sports Injuries"],
        "nearby_states": ["New York", "New Jersey", "Ohio", "Maryland"],
        "unique_factors": "Philadelphia has Penn Medicine and other major academic centers. Pittsburgh has UPMC. Both offer cutting-edge treatments.",
    },
    "tennessee": {
        "name": "Tennessee",
        "abbrev": "TN",
        "cities": ["Nashville", "Memphis"],
        "avg_price_low": 3500,
        "avg_price_high": 9000,
        "regulation_level": "moderate",
        "popular_treatments": ["Knee Osteoarthritis", "Back Pain", "Joint Injuries"],
        "nearby_states": ["Kentucky", "Georgia", "Alabama", "Arkansas"],
        "unique_factors": "Nashville is a growing medical hub with Vanderbilt University. Competitive pricing for quality care.",
    },
    "texas": {
        "name": "Texas",
        "abbrev": "TX",
        "cities": ["Houston", "Dallas", "San Antonio", "Austin", "Fort Worth"],
        "avg_price_low": 3500,
        "avg_price_high": 11000,
        "regulation_level": "moderate",
        "popular_treatments": ["Knee Osteoarthritis", "Back Pain", "Sports Injuries", "Hip Pain"],
        "nearby_states": ["Oklahoma", "New Mexico", "Louisiana"],
        "unique_factors": "Texas has the second-most stem cell clinics in the US. Houston's Texas Medical Center is the world's largest. Multiple major cities offer competitive options.",
    },
    "utah": {
        "name": "Utah",
        "abbrev": "UT",
        "cities": ["Salt Lake City"],
        "avg_price_low": 3500,
        "avg_price_high": 9000,
        "regulation_level": "moderate",
        "popular_treatments": ["Knee Osteoarthritis", "Sports Injuries", "Skiing Injuries"],
        "nearby_states": ["Colorado", "Nevada", "Arizona", "Idaho"],
        "unique_factors": "Salt Lake City serves outdoor enthusiasts and athletes. University of Utah provides research opportunities. Popular for skiing injury treatments.",
    },
    "washington": {
        "name": "Washington",
        "abbrev": "WA",
        "cities": ["Seattle"],
        "avg_price_low": 4000,
        "avg_price_high": 12000,
        "regulation_level": "moderate",
        "popular_treatments": ["Knee Osteoarthritis", "Sports Injuries", "Joint Pain"],
        "nearby_states": ["Oregon", "Idaho"],
        "unique_factors": "Seattle has excellent medical facilities including UW Medicine. Serves the Pacific Northwest region including Alaska patients.",
    },
    "washington-dc": {
        "name": "Washington DC",
        "abbrev": "DC",
        "cities": ["Washington"],
        "avg_price_low": 5000,
        "avg_price_high": 15000,
        "regulation_level": "strict",
        "popular_treatments": ["Knee Osteoarthritis", "Back Pain", "Sports Injuries"],
        "nearby_states": ["Maryland", "Virginia"],
        "unique_factors": "Access to Georgetown, GW, and other major medical centers. NIH proximity provides research opportunities. Premium pricing.",
    },
    "wisconsin": {
        "name": "Wisconsin",
        "abbrev": "WI",
        "cities": ["Milwaukee"],
        "avg_price_low": 3500,
        "avg_price_high": 9000,
        "regulation_level": "moderate",
        "popular_treatments": ["Knee Osteoarthritis", "Back Pain", "Joint Injuries"],
        "nearby_states": ["Illinois", "Minnesota", "Michigan"],
        "unique_factors": "Milwaukee has quality orthopedic clinics. UW-Madison provides research opportunities. Competitive Midwest pricing.",
    },
}

# City-specific data
CITY_DATA = {
    "anchorage": {"state": "alaska", "name": "Anchorage", "population": "290,000", "specialties": ["Orthopedic Medicine", "Sports Injuries"]},
    "phoenix": {"state": "arizona", "name": "Phoenix", "population": "1.6 million", "specialties": ["Orthopedic Medicine", "Sports Injuries", "Senior Care"]},
    "scottsdale": {"state": "arizona", "name": "Scottsdale", "population": "250,000", "specialties": ["Luxury Regenerative Medicine", "Anti-Aging", "Sports Medicine"]},
    "tucson": {"state": "arizona", "name": "Tucson", "population": "550,000", "specialties": ["Orthopedic Medicine", "Joint Treatments"]},
    "los-angeles": {"state": "california", "name": "Los Angeles", "population": "4 million", "specialties": ["Sports Medicine", "Anti-Aging", "Orthopedic Regeneration"]},
    "san-diego": {"state": "california", "name": "San Diego", "population": "1.4 million", "specialties": ["Orthopedic Medicine", "Sports Injuries", "Military Medicine"], "mexico_note": "Tijuana is just 20 minutes away, offering savings of 40-60% on stem cell treatments."},
    "san-francisco": {"state": "california", "name": "San Francisco", "population": "870,000", "specialties": ["Cutting-Edge Research", "Biotech Innovation", "Orthopedic Medicine"]},
    "san-jose": {"state": "california", "name": "San Jose", "population": "1 million", "specialties": ["Orthopedic Medicine", "Sports Injuries"]},
    "fresno": {"state": "california", "name": "Fresno", "population": "540,000", "specialties": ["Orthopedic Medicine", "Joint Treatments"]},
    "sacramento": {"state": "california", "name": "Sacramento", "population": "525,000", "specialties": ["Orthopedic Medicine", "Sports Injuries"]},
    "denver": {"state": "colorado", "name": "Denver", "population": "715,000", "specialties": ["Sports Medicine", "Skiing Injuries", "Orthopedic Regeneration"]},
    "miami": {"state": "florida", "name": "Miami", "population": "450,000", "specialties": ["Anti-Aging", "Cosmetic Regeneration", "Sports Medicine"], "mexico_note": "Cancun is just 1.5 hours by flight, offering resort-style medical tourism."},
    "tampa": {"state": "florida", "name": "Tampa", "population": "400,000", "specialties": ["Orthopedic Medicine", "Senior Care", "Joint Treatments"]},
    "orlando": {"state": "florida", "name": "Orlando", "population": "310,000", "specialties": ["Orthopedic Medicine", "Sports Injuries"]},
    "jacksonville": {"state": "florida", "name": "Jacksonville", "population": "950,000", "specialties": ["Orthopedic Medicine", "Joint Treatments"]},
    "atlanta": {"state": "georgia", "name": "Atlanta", "population": "500,000", "specialties": ["Orthopedic Medicine", "Sports Injuries", "Joint Treatments"]},
    "honolulu": {"state": "hawaii", "name": "Honolulu", "population": "350,000", "specialties": ["Orthopedic Medicine", "Sports Injuries"]},
    "boise": {"state": "idaho", "name": "Boise", "population": "235,000", "specialties": ["Orthopedic Medicine", "Joint Treatments"]},
    "chicago": {"state": "illinois", "name": "Chicago", "population": "2.7 million", "specialties": ["Orthopedic Medicine", "Sports Medicine", "Research-Based Treatments"]},
    "indianapolis": {"state": "indiana", "name": "Indianapolis", "population": "880,000", "specialties": ["Orthopedic Medicine", "Sports Injuries"]},
    "louisville": {"state": "kentucky", "name": "Louisville", "population": "620,000", "specialties": ["Orthopedic Medicine", "Joint Treatments"]},
    "baltimore": {"state": "maryland", "name": "Baltimore", "population": "575,000", "specialties": ["Research-Based Treatments", "Orthopedic Medicine"]},
    "boston": {"state": "massachusetts", "name": "Boston", "population": "675,000", "specialties": ["Research-Based Treatments", "Sports Medicine", "Orthopedic Innovation"]},
    "detroit": {"state": "michigan", "name": "Detroit", "population": "640,000", "specialties": ["Orthopedic Medicine", "Sports Injuries"]},
    "minneapolis": {"state": "minnesota", "name": "Minneapolis", "population": "430,000", "specialties": ["Mayo Clinic Access", "Orthopedic Medicine", "Sports Injuries"]},
    "st-louis": {"state": "missouri", "name": "St. Louis", "population": "300,000", "specialties": ["Orthopedic Medicine", "Research-Based Treatments"]},
    "kansas-city": {"state": "missouri", "name": "Kansas City", "population": "510,000", "specialties": ["Orthopedic Medicine", "Sports Injuries"]},
    "las-vegas": {"state": "nevada", "name": "Las Vegas", "population": "650,000", "specialties": ["Luxury Regenerative Medicine", "Anti-Aging", "Sports Medicine"]},
    "albuquerque": {"state": "new-mexico", "name": "Albuquerque", "population": "560,000", "specialties": ["Orthopedic Medicine", "Joint Treatments"]},
    "new-york-city": {"state": "new-york", "name": "New York City", "population": "8.3 million", "specialties": ["Sports Medicine", "Orthopedic Surgery Alternatives", "Anti-Aging"]},
    "charlotte": {"state": "north-carolina", "name": "Charlotte", "population": "880,000", "specialties": ["Orthopedic Medicine", "Sports Injuries"]},
    "raleigh": {"state": "north-carolina", "name": "Raleigh", "population": "470,000", "specialties": ["Research-Based Treatments", "Orthopedic Medicine"]},
    "columbus": {"state": "ohio", "name": "Columbus", "population": "905,000", "specialties": ["Orthopedic Medicine", "Sports Injuries"]},
    "cleveland": {"state": "ohio", "name": "Cleveland", "population": "370,000", "specialties": ["Cleveland Clinic", "Orthopedic Excellence", "Research-Based Treatments"]},
    "cincinnati": {"state": "ohio", "name": "Cincinnati", "population": "310,000", "specialties": ["Orthopedic Medicine", "Sports Injuries"]},
    "oklahoma-city": {"state": "oklahoma", "name": "Oklahoma City", "population": "680,000", "specialties": ["Orthopedic Medicine", "Joint Treatments"]},
    "portland": {"state": "oregon", "name": "Portland", "population": "650,000", "specialties": ["Orthopedic Medicine", "Sports Injuries", "OHSU Research"]},
    "philadelphia": {"state": "pennsylvania", "name": "Philadelphia", "population": "1.6 million", "specialties": ["Penn Medicine", "Orthopedic Excellence", "Research-Based Treatments"]},
    "pittsburgh": {"state": "pennsylvania", "name": "Pittsburgh", "population": "300,000", "specialties": ["UPMC", "Orthopedic Medicine", "Research-Based Treatments"]},
    "nashville": {"state": "tennessee", "name": "Nashville", "population": "690,000", "specialties": ["Vanderbilt Medicine", "Orthopedic Medicine", "Sports Injuries"]},
    "memphis": {"state": "tennessee", "name": "Memphis", "population": "630,000", "specialties": ["Orthopedic Medicine", "Joint Treatments"]},
    "houston": {"state": "texas", "name": "Houston", "population": "2.3 million", "specialties": ["Texas Medical Center", "Orthopedic Medicine", "Research-Based Treatments"]},
    "dallas": {"state": "texas", "name": "Dallas", "population": "1.3 million", "specialties": ["UT Southwestern", "Orthopedic Medicine", "Sports Injuries"]},
    "san-antonio": {"state": "texas", "name": "San Antonio", "population": "1.5 million", "specialties": ["Orthopedic Medicine", "Military Medicine", "Joint Treatments"]},
    "austin": {"state": "texas", "name": "Austin", "population": "1 million", "specialties": ["Orthopedic Medicine", "Sports Injuries", "Active Lifestyle Medicine"]},
    "fort-worth": {"state": "texas", "name": "Fort Worth", "population": "940,000", "specialties": ["Orthopedic Medicine", "Joint Treatments"]},
    "salt-lake-city": {"state": "utah", "name": "Salt Lake City", "population": "200,000", "specialties": ["Sports Medicine", "Skiing Injuries", "University of Utah Research"]},
    "seattle": {"state": "washington", "name": "Seattle", "population": "750,000", "specialties": ["UW Medicine", "Orthopedic Medicine", "Research-Based Treatments"]},
    "washington": {"state": "washington-dc", "name": "Washington DC", "population": "690,000", "specialties": ["NIH Research Access", "Georgetown Medicine", "Orthopedic Excellence"]},
    "milwaukee": {"state": "wisconsin", "name": "Milwaukee", "population": "575,000", "specialties": ["Orthopedic Medicine", "Sports Injuries"]},
}


def generate_state_seo_content(state_slug, state_data):
    """Generate SEO content for a state page using OpenAI."""
    
    cities_list = ", ".join(state_data["cities"])
    treatments_list = ", ".join(state_data["popular_treatments"])
    nearby_list = ", ".join(state_data["nearby_states"]) if state_data["nearby_states"] else "none nearby"
    
    prompt = f"""Write approximately 500 words of SEO-optimized content for a stem cell therapy directory page for {state_data['name']}. 

Key information to include:
- State: {state_data['name']} ({state_data['abbrev']})
- Cities with clinics: {cities_list}
- Price range: ${state_data['avg_price_low']:,} - ${state_data['avg_price_high']:,}
- Regulation level: {state_data['regulation_level']}
- Popular treatments: {treatments_list}
- Nearby states: {nearby_list}
- Unique factors: {state_data['unique_factors']}

Requirements:
1. Use proper H2 subheadings (NOT H1 - that's already on the page)
2. Include the main keyword "stem cell therapy in {state_data['name']}" naturally 2-3 times
3. Include secondary keywords like "regenerative medicine {state_data['name']}", "stem cell clinics {state_data['name']}"
4. Mention specific cities where clinics are located
5. Discuss pricing expectations for the region
6. Explain any state-specific regulations or considerations
7. Include a section about what treatments are most commonly sought
8. Mention Mexico medical tourism as an alternative option for cost savings (link to /locations/mexico/)
9. Use professional, informative tone suitable for medical content
10. Include internal link suggestions using [link text](/url/) format

Structure the content with these H2 sections:
- Understanding Stem Cell Therapy in {state_data['name']}
- Cost of Stem Cell Treatment in {state_data['name']}
- Popular Stem Cell Treatments
- Finding the Right Clinic

Write in HTML format with proper <h2>, <p>, and <a> tags. Do not include any wrapper div or section tags - just the content elements."""

    response = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=[
            {"role": "system", "content": "You are an expert medical content writer specializing in SEO-optimized healthcare content. Write informative, accurate, and engaging content that helps patients make informed decisions about stem cell therapy."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.7,
        max_tokens=1500
    )
    
    return response.choices[0].message.content


def generate_city_seo_content(city_slug, city_data, state_data):
    """Generate SEO content for a city page using OpenAI."""
    
    specialties_list = ", ".join(city_data["specialties"])
    treatments_list = ", ".join(state_data["popular_treatments"])
    mexico_note = city_data.get("mexico_note", "")
    
    prompt = f"""Write approximately 500 words of SEO-optimized content for a stem cell therapy directory page for {city_data['name']}, {state_data['name']}. 

Key information to include:
- City: {city_data['name']}, {state_data['name']}
- Population: {city_data['population']}
- Specialties: {specialties_list}
- State price range: ${state_data['avg_price_low']:,} - ${state_data['avg_price_high']:,}
- Popular treatments: {treatments_list}
- State unique factors: {state_data['unique_factors']}
{f'- Mexico proximity note: {mexico_note}' if mexico_note else ''}

Requirements:
1. Use proper H2 subheadings (NOT H1 - that's already on the page)
2. Include the main keyword "stem cell therapy in {city_data['name']}" naturally 2-3 times
3. Include secondary keywords like "stem cell clinics {city_data['name']}", "regenerative medicine {city_data['name']}"
4. Discuss what makes this city unique for stem cell treatments
5. Mention pricing expectations
6. Include information about local medical institutions or specialties
7. Mention Mexico medical tourism as an alternative option for cost savings (link to /locations/mexico/)
8. Use professional, informative tone suitable for medical content
9. Include internal link suggestions using [link text](/url/) format
10. Link back to the state page: /locations/{city_data['state']}/

Structure the content with these H2 sections:
- Stem Cell Therapy Options in {city_data['name']}
- Cost of Treatment in {city_data['name']}
- What to Expect from Local Clinics
- Choosing a Provider

Write in HTML format with proper <h2>, <p>, and <a> tags. Do not include any wrapper div or section tags - just the content elements."""

    response = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=[
            {"role": "system", "content": "You are an expert medical content writer specializing in SEO-optimized healthcare content. Write informative, accurate, and engaging content that helps patients make informed decisions about stem cell therapy."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.7,
        max_tokens=1500
    )
    
    return response.choices[0].message.content


def inject_seo_content_into_page(file_path, seo_content):
    """Inject SEO content into an existing HTML page."""
    
    with open(file_path, 'r', encoding='utf-8') as f:
        html_content = f.read()
    
    # Create the SEO content section
    seo_section = f'''
    <!-- SEO Content Section -->
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12 bg-white">
        <div class="prose prose-lg max-w-none">
            {seo_content}
        </div>
    </div>
'''
    
    # Find the position to insert - after the city/clinic grid and before the disclaimer
    # Look for the disclaimer section
    disclaimer_pattern = r'(<div class="bg-amber-50 border-l-4 border-amber-400)'
    
    if re.search(disclaimer_pattern, html_content):
        # Insert before the disclaimer
        html_content = re.sub(
            disclaimer_pattern,
            seo_section + r'\n    \1',
            html_content,
            count=1
        )
    else:
        # Fallback: insert before footer
        footer_pattern = r'(<!-- Footer -->)'
        html_content = re.sub(
            footer_pattern,
            seo_section + r'\n    \1',
            html_content,
            count=1
        )
    
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    return True


def process_state_page(state_slug):
    """Process a single state page."""
    if state_slug not in STATE_DATA:
        print(f"  Skipping {state_slug} - no data available")
        return False
    
    state_data = STATE_DATA[state_slug]
    file_path = f"/home/ubuntu/stem-cells/locations/{state_slug}/index.html"
    
    if not os.path.exists(file_path):
        print(f"  File not found: {file_path}")
        return False
    
    # Check if SEO content already exists
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    if '<!-- SEO Content Section -->' in content:
        print(f"  SEO content already exists for {state_slug}")
        return True
    
    print(f"  Generating SEO content for {state_data['name']}...")
    seo_content = generate_state_seo_content(state_slug, state_data)
    
    print(f"  Injecting content into {file_path}...")
    inject_seo_content_into_page(file_path, seo_content)
    
    return True


def process_city_page(city_slug, state_slug):
    """Process a single city page."""
    if city_slug not in CITY_DATA:
        print(f"  Skipping {city_slug} - no data available")
        return False
    
    if state_slug not in STATE_DATA:
        print(f"  Skipping {city_slug} - state data not available")
        return False
    
    city_data = CITY_DATA[city_slug]
    state_data = STATE_DATA[state_slug]
    file_path = f"/home/ubuntu/stem-cells/locations/{state_slug}/{city_slug}/index.html"
    
    if not os.path.exists(file_path):
        print(f"  File not found: {file_path}")
        return False
    
    # Check if SEO content already exists
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    if '<!-- SEO Content Section -->' in content:
        print(f"  SEO content already exists for {city_slug}")
        return True
    
    print(f"  Generating SEO content for {city_data['name']}, {state_data['name']}...")
    seo_content = generate_city_seo_content(city_slug, city_data, state_data)
    
    print(f"  Injecting content into {file_path}...")
    inject_seo_content_into_page(file_path, seo_content)
    
    return True


def main():
    """Main function to process all state and city pages."""
    
    print("=" * 60)
    print("SEO Content Generator for StemCellPrices.com")
    print("=" * 60)
    
    # Process state pages
    print("\n[1/2] Processing State Pages...")
    state_count = 0
    for state_slug in STATE_DATA.keys():
        print(f"\nProcessing state: {state_slug}")
        if process_state_page(state_slug):
            state_count += 1
    
    print(f"\nCompleted {state_count} state pages")
    
    # Process city pages
    print("\n[2/2] Processing City Pages...")
    city_count = 0
    for city_slug, city_data in CITY_DATA.items():
        state_slug = city_data["state"]
        print(f"\nProcessing city: {city_slug} ({state_slug})")
        if process_city_page(city_slug, state_slug):
            city_count += 1
    
    print(f"\nCompleted {city_count} city pages")
    
    print("\n" + "=" * 60)
    print(f"SUMMARY: Processed {state_count} state pages and {city_count} city pages")
    print("=" * 60)


if __name__ == "__main__":
    main()
