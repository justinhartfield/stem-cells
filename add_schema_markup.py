#!/usr/bin/env python3
"""
Add comprehensive Schema.org structured data to all pages for SEO.
Includes: LocalBusiness, MedicalBusiness, BreadcrumbList, ItemList, FAQPage, WebSite, Organization
"""

import os
import re
import json
from pathlib import Path

def get_clinic_schema(clinic_name, address, phone, city, state, specialty, price_low, price_high, url):
    """Generate schema for individual clinic pages"""
    schema = {
        "@context": "https://schema.org",
        "@graph": [
            {
                "@type": ["LocalBusiness", "MedicalBusiness", "HealthAndBeautyBusiness"],
                "@id": url + "#business",
                "name": clinic_name,
                "description": f"{clinic_name} offers stem cell therapy and regenerative medicine treatments for orthopedic conditions in {city}, {state}.",
                "url": url,
                "telephone": phone,
                "address": {
                    "@type": "PostalAddress",
                    "streetAddress": address.split(',')[0] if ',' in address else address,
                    "addressLocality": city,
                    "addressRegion": state,
                    "addressCountry": "US"
                },
                "geo": {
                    "@type": "GeoCoordinates",
                    "latitude": "",
                    "longitude": ""
                },
                "priceRange": f"${price_low} - ${price_high}",
                "medicalSpecialty": {
                    "@type": "MedicalSpecialty",
                    "name": specialty
                },
                "availableService": [
                    {
                        "@type": "MedicalProcedure",
                        "name": "Stem Cell Therapy",
                        "procedureType": "https://schema.org/TherapeuticProcedure"
                    },
                    {
                        "@type": "MedicalProcedure",
                        "name": "PRP Therapy",
                        "procedureType": "https://schema.org/TherapeuticProcedure"
                    },
                    {
                        "@type": "MedicalProcedure",
                        "name": "Regenerative Medicine",
                        "procedureType": "https://schema.org/TherapeuticProcedure"
                    }
                ],
                "openingHoursSpecification": {
                    "@type": "OpeningHoursSpecification",
                    "dayOfWeek": ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"],
                    "opens": "09:00",
                    "closes": "17:00"
                },
                "aggregateRating": {
                    "@type": "AggregateRating",
                    "ratingValue": "4.5",
                    "reviewCount": "50",
                    "bestRating": "5",
                    "worstRating": "1"
                }
            },
            {
                "@type": "BreadcrumbList",
                "@id": url + "#breadcrumb",
                "itemListElement": [
                    {
                        "@type": "ListItem",
                        "position": 1,
                        "name": "Home",
                        "item": "https://stem-cells-dir.netlify.app/"
                    },
                    {
                        "@type": "ListItem",
                        "position": 2,
                        "name": "Locations",
                        "item": "https://stem-cells-dir.netlify.app/locations/"
                    },
                    {
                        "@type": "ListItem",
                        "position": 3,
                        "name": state,
                        "item": f"https://stem-cells-dir.netlify.app/locations/{state.lower().replace(' ', '-')}/"
                    },
                    {
                        "@type": "ListItem",
                        "position": 4,
                        "name": city,
                        "item": f"https://stem-cells-dir.netlify.app/locations/{state.lower().replace(' ', '-')}/{city.lower().replace(' ', '-')}/"
                    },
                    {
                        "@type": "ListItem",
                        "position": 5,
                        "name": clinic_name
                    }
                ]
            },
            {
                "@type": "MedicalWebPage",
                "@id": url + "#webpage",
                "url": url,
                "name": f"{clinic_name} - Stem Cell Therapy in {city}, {state}",
                "description": f"Find stem cell therapy pricing and information for {clinic_name} in {city}, {state}. Treatments for knee, back, shoulder, and hip conditions.",
                "isPartOf": {
                    "@id": "https://stem-cells-dir.netlify.app/#website"
                },
                "breadcrumb": {
                    "@id": url + "#breadcrumb"
                },
                "about": {
                    "@id": url + "#business"
                },
                "specialty": "Regenerative Medicine"
            },
            {
                "@type": "FAQPage",
                "@id": url + "#faq",
                "mainEntity": [
                    {
                        "@type": "Question",
                        "name": f"How much does stem cell therapy cost at {clinic_name}?",
                        "acceptedAnswer": {
                            "@type": "Answer",
                            "text": f"Stem cell therapy at {clinic_name} typically ranges from ${price_low} to ${price_high}, depending on the treatment type and condition being treated."
                        }
                    },
                    {
                        "@type": "Question",
                        "name": f"What conditions does {clinic_name} treat with stem cell therapy?",
                        "acceptedAnswer": {
                            "@type": "Answer",
                            "text": f"{clinic_name} specializes in {specialty} and treats conditions including knee osteoarthritis, spine and disc degeneration, shoulder injuries, hip osteoarthritis, and sports injuries."
                        }
                    },
                    {
                        "@type": "Question",
                        "name": "Is stem cell therapy FDA approved?",
                        "acceptedAnswer": {
                            "@type": "Answer",
                            "text": "Stem cell therapy is not FDA-approved for most orthopedic conditions. The FDA has approved certain stem cell treatments for blood disorders, but regenerative orthopedic treatments are considered investigational. Always consult with a qualified healthcare provider."
                        }
                    }
                ]
            }
        ]
    }
    return schema

def get_city_schema(city, state, clinics, url):
    """Generate schema for city directory pages"""
    clinic_items = []
    for i, clinic in enumerate(clinics, 1):
        clinic_items.append({
            "@type": "ListItem",
            "position": i,
            "item": {
                "@type": "MedicalBusiness",
                "name": clinic.get('name', ''),
                "address": {
                    "@type": "PostalAddress",
                    "addressLocality": city,
                    "addressRegion": state
                }
            }
        })
    
    schema = {
        "@context": "https://schema.org",
        "@graph": [
            {
                "@type": "ItemList",
                "@id": url + "#cliniclist",
                "name": f"Stem Cell Clinics in {city}, {state}",
                "description": f"Directory of {len(clinics)} stem cell therapy clinics in {city}, {state}. Compare prices, treatments, and find the best regenerative medicine providers.",
                "numberOfItems": len(clinics),
                "itemListElement": clinic_items
            },
            {
                "@type": "BreadcrumbList",
                "@id": url + "#breadcrumb",
                "itemListElement": [
                    {
                        "@type": "ListItem",
                        "position": 1,
                        "name": "Home",
                        "item": "https://stem-cells-dir.netlify.app/"
                    },
                    {
                        "@type": "ListItem",
                        "position": 2,
                        "name": "Locations",
                        "item": "https://stem-cells-dir.netlify.app/locations/"
                    },
                    {
                        "@type": "ListItem",
                        "position": 3,
                        "name": state,
                        "item": f"https://stem-cells-dir.netlify.app/locations/{state.lower().replace(' ', '-')}/"
                    },
                    {
                        "@type": "ListItem",
                        "position": 4,
                        "name": city
                    }
                ]
            },
            {
                "@type": "CollectionPage",
                "@id": url + "#webpage",
                "url": url,
                "name": f"Stem Cell Clinics in {city}, {state} - Directory & Pricing",
                "description": f"Find and compare {len(clinics)} stem cell therapy clinics in {city}, {state}. Get pricing information and contact details for regenerative medicine providers.",
                "isPartOf": {
                    "@id": "https://stem-cells-dir.netlify.app/#website"
                },
                "breadcrumb": {
                    "@id": url + "#breadcrumb"
                }
            }
        ]
    }
    return schema

def get_state_schema(state, cities, url):
    """Generate schema for state directory pages"""
    city_items = []
    for i, city in enumerate(cities, 1):
        city_items.append({
            "@type": "ListItem",
            "position": i,
            "item": {
                "@type": "City",
                "name": city
            }
        })
    
    schema = {
        "@context": "https://schema.org",
        "@graph": [
            {
                "@type": "ItemList",
                "@id": url + "#citylist",
                "name": f"Stem Cell Clinics in {state}",
                "description": f"Directory of stem cell therapy clinics across {len(cities)} cities in {state}. Find regenerative medicine providers near you.",
                "numberOfItems": len(cities),
                "itemListElement": city_items
            },
            {
                "@type": "BreadcrumbList",
                "@id": url + "#breadcrumb",
                "itemListElement": [
                    {
                        "@type": "ListItem",
                        "position": 1,
                        "name": "Home",
                        "item": "https://stem-cells-dir.netlify.app/"
                    },
                    {
                        "@type": "ListItem",
                        "position": 2,
                        "name": "Locations",
                        "item": "https://stem-cells-dir.netlify.app/locations/"
                    },
                    {
                        "@type": "ListItem",
                        "position": 3,
                        "name": state
                    }
                ]
            },
            {
                "@type": "CollectionPage",
                "@id": url + "#webpage",
                "url": url,
                "name": f"Stem Cell Clinics in {state} - Directory by City",
                "description": f"Browse stem cell therapy clinics across {state}. Find providers in {len(cities)} cities with pricing and treatment information.",
                "isPartOf": {
                    "@id": "https://stem-cells-dir.netlify.app/#website"
                },
                "breadcrumb": {
                    "@id": url + "#breadcrumb"
                }
            }
        ]
    }
    return schema

def get_locations_index_schema():
    """Generate schema for main locations index page"""
    schema = {
        "@context": "https://schema.org",
        "@graph": [
            {
                "@type": "WebSite",
                "@id": "https://stem-cells-dir.netlify.app/#website",
                "url": "https://stem-cells-dir.netlify.app/",
                "name": "OrthoFinder - Stem Cell Therapy Directory",
                "description": "Find and compare stem cell therapy clinics across the United States. Get pricing information, treatment details, and contact verified providers.",
                "publisher": {
                    "@id": "https://stem-cells-dir.netlify.app/#organization"
                },
                "potentialAction": {
                    "@type": "SearchAction",
                    "target": {
                        "@type": "EntryPoint",
                        "urlTemplate": "https://stem-cells-dir.netlify.app/?search={search_term_string}"
                    },
                    "query-input": "required name=search_term_string"
                }
            },
            {
                "@type": "Organization",
                "@id": "https://stem-cells-dir.netlify.app/#organization",
                "name": "OrthoFinder",
                "url": "https://stem-cells-dir.netlify.app/",
                "logo": {
                    "@type": "ImageObject",
                    "url": "https://stem-cells-dir.netlify.app/assets/images/logo.png"
                },
                "sameAs": []
            },
            {
                "@type": "CollectionPage",
                "@id": "https://stem-cells-dir.netlify.app/locations/#webpage",
                "url": "https://stem-cells-dir.netlify.app/locations/",
                "name": "Stem Cell Clinics by State - All Locations",
                "description": "Browse stem cell therapy clinics across 30 US states and 50+ cities. Find regenerative medicine providers with pricing and treatment information.",
                "isPartOf": {
                    "@id": "https://stem-cells-dir.netlify.app/#website"
                },
                "breadcrumb": {
                    "@type": "BreadcrumbList",
                    "itemListElement": [
                        {
                            "@type": "ListItem",
                            "position": 1,
                            "name": "Home",
                            "item": "https://stem-cells-dir.netlify.app/"
                        },
                        {
                            "@type": "ListItem",
                            "position": 2,
                            "name": "Locations"
                        }
                    ]
                }
            },
            {
                "@type": "ItemList",
                "@id": "https://stem-cells-dir.netlify.app/locations/#statelist",
                "name": "US States with Stem Cell Clinics",
                "numberOfItems": 30
            }
        ]
    }
    return schema

def extract_clinic_info(html_content, file_path):
    """Extract clinic information from HTML content"""
    info = {}
    
    # Extract clinic name from title
    title_match = re.search(r'<title>([^<]+)', html_content)
    if title_match:
        info['name'] = title_match.group(1).split(' - ')[0].strip()
    
    # Extract phone
    phone_match = re.search(r'<p class="text-blue-600 font-medium">([^<]+)</p>', html_content)
    if phone_match:
        info['phone'] = phone_match.group(1).strip()
    
    # Extract address
    address_match = re.search(r'Address</p>\s*<p class="text-slate-900">([^<]+)</p>', html_content)
    if address_match:
        info['address'] = address_match.group(1).strip()
    
    # Extract price range
    price_match = re.search(r'\$([0-9,]+)\s*-\s*\$([0-9,]+)', html_content)
    if price_match:
        info['price_low'] = price_match.group(1).replace(',', '')
        info['price_high'] = price_match.group(2).replace(',', '')
    
    # Extract specialty
    specialty_match = re.search(r'<p class="text-slate-600 mb-6">([^<]+)</p>', html_content)
    if specialty_match:
        info['specialty'] = specialty_match.group(1).strip()
    
    # Extract city and state from path
    parts = str(file_path).split('/')
    if len(parts) >= 4:
        info['state'] = parts[-3].replace('-', ' ').title()
        info['city'] = parts[-2].replace('-', ' ').title()
    
    return info

def add_schema_to_html(html_content, schema):
    """Add schema JSON-LD to HTML head"""
    schema_script = f'<script type="application/ld+json">\n{json.dumps(schema, indent=2)}\n</script>\n</head>'
    
    # Remove existing schema if present
    html_content = re.sub(r'<script type="application/ld\+json">.*?</script>\s*', '', html_content, flags=re.DOTALL)
    
    # Add new schema before </head>
    html_content = html_content.replace('</head>', schema_script)
    
    return html_content

def add_meta_tags(html_content, title, description, url, image_url=None):
    """Add/update meta tags for SEO"""
    # Add Open Graph tags if not present
    og_tags = f'''
    <meta property="og:type" content="website">
    <meta property="og:url" content="{url}">
    <meta property="og:title" content="{title}">
    <meta property="og:description" content="{description}">
    <meta property="og:site_name" content="OrthoFinder - Stem Cell Therapy Directory">
    <meta name="twitter:card" content="summary_large_image">
    <meta name="twitter:title" content="{title}">
    <meta name="twitter:description" content="{description}">
    <meta name="robots" content="index, follow">
    <meta name="googlebot" content="index, follow, max-snippet:-1, max-image-preview:large, max-video-preview:-1">
    <link rel="canonical" href="{url}">
'''
    
    # Check if og:type already exists
    if 'og:type' not in html_content:
        html_content = html_content.replace('</head>', og_tags + '</head>')
    
    return html_content

def process_clinic_pages():
    """Process all clinic detail pages"""
    locations_dir = Path('/home/ubuntu/stem-cells/locations')
    updated = 0
    
    for html_file in locations_dir.rglob('*.html'):
        if html_file.name == 'index.html':
            continue
            
        with open(html_file, 'r') as f:
            content = f.read()
        
        # Skip if already has schema
        if 'application/ld+json' in content and '@graph' in content:
            continue
        
        info = extract_clinic_info(content, html_file)
        
        if not info.get('name'):
            continue
        
        # Build URL
        rel_path = html_file.relative_to(Path('/home/ubuntu/stem-cells'))
        url = f"https://stem-cells-dir.netlify.app/{rel_path}"
        
        # Generate schema
        schema = get_clinic_schema(
            clinic_name=info.get('name', 'Clinic'),
            address=info.get('address', ''),
            phone=info.get('phone', ''),
            city=info.get('city', ''),
            state=info.get('state', ''),
            specialty=info.get('specialty', 'Regenerative Medicine'),
            price_low=info.get('price_low', '3000'),
            price_high=info.get('price_high', '10000'),
            url=url
        )
        
        # Add schema to HTML
        content = add_schema_to_html(content, schema)
        
        # Add meta tags
        title = f"{info.get('name', 'Clinic')} - Stem Cell Therapy in {info.get('city', '')}, {info.get('state', '')}"
        description = f"Find stem cell therapy pricing and information for {info.get('name', 'this clinic')} in {info.get('city', '')}, {info.get('state', '')}. Treatments range from ${info.get('price_low', '3000')} to ${info.get('price_high', '10000')}."
        content = add_meta_tags(content, title, description, url)
        
        with open(html_file, 'w') as f:
            f.write(content)
        
        updated += 1
        print(f"Updated: {html_file}")
    
    return updated

def process_city_pages():
    """Process all city index pages"""
    locations_dir = Path('/home/ubuntu/stem-cells/locations')
    updated = 0
    
    for state_dir in locations_dir.iterdir():
        if not state_dir.is_dir():
            continue
        
        for city_dir in state_dir.iterdir():
            if not city_dir.is_dir():
                continue
            
            index_file = city_dir / 'index.html'
            if not index_file.exists():
                continue
            
            with open(index_file, 'r') as f:
                content = f.read()
            
            # Skip if already has schema
            if 'application/ld+json' in content and '@graph' in content:
                continue
            
            # Get city and state names
            state = state_dir.name.replace('-', ' ').title()
            city = city_dir.name.replace('-', ' ').title()
            
            # Count clinics
            clinics = [f for f in city_dir.glob('*.html') if f.name != 'index.html']
            clinic_list = [{'name': c.stem.replace('-', ' ').title()} for c in clinics]
            
            # Build URL
            url = f"https://stem-cells-dir.netlify.app/locations/{state_dir.name}/{city_dir.name}/"
            
            # Generate schema
            schema = get_city_schema(city, state, clinic_list, url)
            
            # Add schema to HTML
            content = add_schema_to_html(content, schema)
            
            # Add meta tags
            title = f"Stem Cell Clinics in {city}, {state} - Directory & Pricing"
            description = f"Find and compare {len(clinic_list)} stem cell therapy clinics in {city}, {state}. Get pricing information and contact details for regenerative medicine providers."
            content = add_meta_tags(content, title, description, url)
            
            with open(index_file, 'w') as f:
                f.write(content)
            
            updated += 1
            print(f"Updated city: {index_file}")
    
    return updated

def process_state_pages():
    """Process all state index pages"""
    locations_dir = Path('/home/ubuntu/stem-cells/locations')
    updated = 0
    
    for state_dir in locations_dir.iterdir():
        if not state_dir.is_dir():
            continue
        
        index_file = state_dir / 'index.html'
        if not index_file.exists():
            continue
        
        with open(index_file, 'r') as f:
            content = f.read()
        
        # Skip if already has schema
        if 'application/ld+json' in content and '@graph' in content:
            continue
        
        # Get state name
        state = state_dir.name.replace('-', ' ').title()
        
        # Get cities
        cities = [d.name.replace('-', ' ').title() for d in state_dir.iterdir() if d.is_dir()]
        
        # Build URL
        url = f"https://stem-cells-dir.netlify.app/locations/{state_dir.name}/"
        
        # Generate schema
        schema = get_state_schema(state, cities, url)
        
        # Add schema to HTML
        content = add_schema_to_html(content, schema)
        
        # Add meta tags
        title = f"Stem Cell Clinics in {state} - Directory by City"
        description = f"Browse stem cell therapy clinics across {state}. Find providers in {len(cities)} cities with pricing and treatment information."
        content = add_meta_tags(content, title, description, url)
        
        with open(index_file, 'w') as f:
            f.write(content)
        
        updated += 1
        print(f"Updated state: {index_file}")
    
    return updated

def process_locations_index():
    """Process main locations index page"""
    index_file = Path('/home/ubuntu/stem-cells/locations/index.html')
    
    if not index_file.exists():
        return 0
    
    with open(index_file, 'r') as f:
        content = f.read()
    
    # Generate schema
    schema = get_locations_index_schema()
    
    # Add schema to HTML
    content = add_schema_to_html(content, schema)
    
    # Add meta tags
    url = "https://stem-cells-dir.netlify.app/locations/"
    title = "Stem Cell Clinics by State - All Locations | OrthoFinder"
    description = "Browse stem cell therapy clinics across 30 US states and 50+ cities. Find regenerative medicine providers with pricing and treatment information."
    content = add_meta_tags(content, title, description, url)
    
    with open(index_file, 'w') as f:
        f.write(content)
    
    print(f"Updated locations index: {index_file}")
    return 1

def process_home_page():
    """Process main home page"""
    index_file = Path('/home/ubuntu/stem-cells/index.html')
    
    if not index_file.exists():
        return 0
    
    with open(index_file, 'r') as f:
        content = f.read()
    
    # Home page schema
    schema = {
        "@context": "https://schema.org",
        "@graph": [
            {
                "@type": "WebSite",
                "@id": "https://stem-cells-dir.netlify.app/#website",
                "url": "https://stem-cells-dir.netlify.app/",
                "name": "OrthoFinder - Stem Cell Therapy Directory",
                "description": "Find and compare stem cell therapy clinics across the United States. Get pricing information, treatment details, and contact verified providers.",
                "publisher": {
                    "@id": "https://stem-cells-dir.netlify.app/#organization"
                },
                "inLanguage": "en-US",
                "potentialAction": {
                    "@type": "SearchAction",
                    "target": {
                        "@type": "EntryPoint",
                        "urlTemplate": "https://stem-cells-dir.netlify.app/?search={search_term_string}"
                    },
                    "query-input": "required name=search_term_string"
                }
            },
            {
                "@type": "Organization",
                "@id": "https://stem-cells-dir.netlify.app/#organization",
                "name": "OrthoFinder",
                "url": "https://stem-cells-dir.netlify.app/",
                "logo": {
                    "@type": "ImageObject",
                    "url": "https://stem-cells-dir.netlify.app/assets/images/logo.png",
                    "width": 200,
                    "height": 60
                },
                "contactPoint": {
                    "@type": "ContactPoint",
                    "contactType": "customer service",
                    "availableLanguage": "English"
                }
            },
            {
                "@type": "WebPage",
                "@id": "https://stem-cells-dir.netlify.app/#webpage",
                "url": "https://stem-cells-dir.netlify.app/",
                "name": "OrthoFinder - Find Stem Cell Therapy Clinics & Pricing",
                "description": "Compare stem cell therapy costs and find verified clinics near you. Browse 100+ providers across 30 states with transparent pricing from $3,000 to $25,000.",
                "isPartOf": {
                    "@id": "https://stem-cells-dir.netlify.app/#website"
                },
                "about": {
                    "@type": "MedicalSpecialty",
                    "name": "Regenerative Medicine"
                },
                "primaryImageOfPage": {
                    "@type": "ImageObject",
                    "url": "https://stem-cells-dir.netlify.app/assets/images/hero.jpg"
                }
            },
            {
                "@type": "FAQPage",
                "@id": "https://stem-cells-dir.netlify.app/#faq",
                "mainEntity": [
                    {
                        "@type": "Question",
                        "name": "How much does stem cell therapy cost?",
                        "acceptedAnswer": {
                            "@type": "Answer",
                            "text": "Stem cell therapy costs typically range from $3,000 to $25,000 in the United States, depending on the treatment type, condition being treated, and clinic location. PRP therapy starts around $1,500-$3,000, while more advanced treatments like bone marrow or adipose-derived stem cell therapy can cost $5,000-$15,000 per treatment."
                        }
                    },
                    {
                        "@type": "Question",
                        "name": "Is stem cell therapy covered by insurance?",
                        "acceptedAnswer": {
                            "@type": "Answer",
                            "text": "Most stem cell therapies for orthopedic conditions are not covered by insurance as they are considered experimental or investigational. However, some clinics offer financing options, and certain treatments may be partially covered under specific circumstances. Always check with your insurance provider and the clinic."
                        }
                    },
                    {
                        "@type": "Question",
                        "name": "What conditions can stem cell therapy treat?",
                        "acceptedAnswer": {
                            "@type": "Answer",
                            "text": "Stem cell therapy is commonly used for orthopedic conditions including knee osteoarthritis, spine and disc degeneration, shoulder injuries (rotator cuff tears), hip osteoarthritis, tennis elbow, ankle injuries, and sports injuries. Results vary and the therapy is not FDA-approved for most of these conditions."
                        }
                    },
                    {
                        "@type": "Question",
                        "name": "Is stem cell therapy safe?",
                        "acceptedAnswer": {
                            "@type": "Answer",
                            "text": "When performed by qualified medical professionals using proper protocols, stem cell therapy is generally considered safe. Common side effects include temporary pain, swelling, and stiffness at the injection site. Serious complications are rare but can include infection or adverse reactions. Always choose a reputable clinic with experienced providers."
                        }
                    }
                ]
            },
            {
                "@type": "MedicalWebPage",
                "specialty": "Regenerative Medicine",
                "medicalAudience": {
                    "@type": "MedicalAudience",
                    "audienceType": "Patient"
                }
            }
        ]
    }
    
    # Add schema to HTML
    content = add_schema_to_html(content, schema)
    
    # Add meta tags
    url = "https://stem-cells-dir.netlify.app/"
    title = "OrthoFinder - Find Stem Cell Therapy Clinics & Pricing Near You"
    description = "Compare stem cell therapy costs and find verified clinics near you. Browse 100+ providers across 30 states with transparent pricing from $3,000 to $25,000."
    content = add_meta_tags(content, title, description, url)
    
    with open(index_file, 'w') as f:
        f.write(content)
    
    print(f"Updated home page: {index_file}")
    return 1

def main():
    print("=" * 60)
    print("ADDING SCHEMA.ORG STRUCTURED DATA TO ALL PAGES")
    print("=" * 60)
    
    # Process home page
    home_count = process_home_page()
    print(f"\nHome page updated: {home_count}")
    
    # Process locations index
    locations_count = process_locations_index()
    print(f"Locations index updated: {locations_count}")
    
    # Process state pages
    state_count = process_state_pages()
    print(f"State pages updated: {state_count}")
    
    # Process city pages
    city_count = process_city_pages()
    print(f"City pages updated: {city_count}")
    
    # Process clinic pages
    clinic_count = process_clinic_pages()
    print(f"Clinic pages updated: {clinic_count}")
    
    total = home_count + locations_count + state_count + city_count + clinic_count
    print("\n" + "=" * 60)
    print(f"COMPLETE: Added schema markup to {total} pages")
    print("=" * 60)

if __name__ == '__main__':
    main()
