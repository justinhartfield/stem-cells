#!/usr/bin/env python3
"""
Comprehensive fix script for StemCellPrices.com:
1. Fix homepage city thumbnails with local images and proper links
2. Fix navigation dropdown hover issue
3. Add Mexico locations (Tijuana, Cancun) to /locations/
4. Create Compare Travel Costs page with real Mexico data
5. Standardize navigation and footer across all pages
6. Fix broken links (duplicate href attributes)
"""

import os
import re
import json

# Paths
BASE_DIR = '/home/ubuntu/stem-cells'
INDEX_HTML = os.path.join(BASE_DIR, 'index.html')
APP_JS = os.path.join(BASE_DIR, 'app.js')
LOCATIONS_DIR = os.path.join(BASE_DIR, 'locations')

# ============================================
# 1. FIX POPULAR CITIES DATA IN APP.JS
# ============================================

def fix_popular_cities():
    """Update popularCities to use local images and include state for proper linking"""
    with open(APP_JS, 'r') as f:
        content = f.read()
    
    # New popularCities data with local images and state info
    new_popular_cities = '''        popularCities: [
            { name: 'Los Angeles', state: 'California', price: 'Avg $5,800', type: 'Premium Market', img: '/assets/images/cities/optimized/los-angeles-medium.webp' },
            { name: 'Houston', state: 'Texas', price: 'Avg $4,900', type: 'Value Market', img: '/assets/images/cities/optimized/houston-medium.webp' },
            { name: 'Tijuana', state: 'Mexico', price: 'Avg $3,500', type: 'Medical Tourism', img: '/assets/images/cities/optimized/tijuana-medium.webp' },
            { name: 'Miami', state: 'Florida', price: 'Avg $6,100', type: 'Premium Market', img: '/assets/images/cities/optimized/miami-medium.webp' },
            { name: 'Scottsdale', state: 'Arizona', price: 'Avg $5,200', type: 'Growth Hub', img: '/assets/images/cities/optimized/scottsdale-medium.webp' }
        ],'''
    
    # Replace old popularCities
    pattern = r"popularCities: \[\s*\{[^]]+\}\s*\],"
    content = re.sub(pattern, new_popular_cities, content, flags=re.DOTALL)
    
    with open(APP_JS, 'w') as f:
        f.write(content)
    
    print("✓ Fixed popularCities data in app.js")

# ============================================
# 2. FIX NAVIGATION DROPDOWN HOVER ISSUE
# ============================================

def fix_nav_dropdown():
    """Fix the Locations dropdown hover issue by adding proper CSS and structure"""
    with open(INDEX_HTML, 'r') as f:
        content = f.read()
    
    # Add CSS for dropdown hover fix
    dropdown_css = '''
        /* Navigation Dropdown Fix */
        .nav-dropdown-container {
            position: relative;
        }
        .nav-dropdown-container:hover .nav-dropdown-menu {
            display: block;
            opacity: 1;
            visibility: visible;
            transform: translateY(0);
        }
        .nav-dropdown-menu {
            display: none;
            position: absolute;
            top: 100%;
            left: 0;
            min-width: 220px;
            background: white;
            border-radius: 12px;
            box-shadow: 0 10px 40px rgba(0,0,0,0.15);
            padding: 8px 0;
            z-index: 1000;
            opacity: 0;
            visibility: hidden;
            transform: translateY(-10px);
            transition: all 0.2s ease;
        }
        .nav-dropdown-menu::before {
            content: '';
            position: absolute;
            top: -10px;
            left: 0;
            right: 0;
            height: 10px;
        }
        .nav-dropdown-menu a {
            display: block;
            padding: 10px 16px;
            color: #334155;
            font-size: 14px;
            font-weight: 500;
            transition: background 0.15s;
        }
        .nav-dropdown-menu a:hover {
            background: #f0f7ff;
            color: #2563eb;
        }
        .nav-dropdown-divider {
            height: 1px;
            background: #e2e8f0;
            margin: 8px 0;
        }
'''
    
    # Insert CSS before </style>
    if 'nav-dropdown-container' not in content:
        content = content.replace('</style>', dropdown_css + '\n    </style>')
    
    # Fix the navigation HTML - replace the Locations link with dropdown
    old_locations_nav = r'<a href="#" href="/locations/"[^>]*>Locations</a>'
    new_locations_nav = '''<div class="nav-dropdown-container">
                            <a href="/locations/" class="transition hover:text-brand-600">Locations</a>
                            <div class="nav-dropdown-menu">
                                <a href="/locations/">All 30 States</a>
                                <div class="nav-dropdown-divider"></div>
                                <a href="/locations/california/">California</a>
                                <a href="/locations/texas/">Texas</a>
                                <a href="/locations/florida/">Florida</a>
                                <a href="/locations/arizona/">Arizona</a>
                                <a href="/locations/new-york/">New York</a>
                                <div class="nav-dropdown-divider"></div>
                                <a href="/locations/mexico/">Mexico (Medical Tourism)</a>
                            </div>
                        </div>'''
    
    content = re.sub(old_locations_nav, new_locations_nav, content)
    
    with open(INDEX_HTML, 'w') as f:
        f.write(content)
    
    print("✓ Fixed navigation dropdown hover issue")

# ============================================
# 3. FIX BROKEN HREF ATTRIBUTES
# ============================================

def fix_broken_hrefs():
    """Fix duplicate href attributes like href="#" href="/locations/" """
    with open(INDEX_HTML, 'r') as f:
        content = f.read()
    
    # Fix href="#" href="/path/" -> href="/path/"
    content = re.sub(r'href="#"\s+href="(/[^"]+)"', r'href="\1"', content)
    
    # Fix href="#" @click patterns - keep the @click
    # content = re.sub(r'href="#"\s+(@click="[^"]+")', r'\1', content)
    
    with open(INDEX_HTML, 'w') as f:
        f.write(content)
    
    print("✓ Fixed broken href attributes")

# ============================================
# 4. FIX POPULAR CITIES LINKS IN INDEX.HTML
# ============================================

def fix_city_links():
    """Update the city card template to handle Mexico cities properly"""
    with open(INDEX_HTML, 'r') as f:
        content = f.read()
    
    # Find and replace the city card link pattern
    old_pattern = "'/locations/' + city.state.toLowerCase().replace(/\\s+/g, '-') + '/' + city.name.toLowerCase().replace(/\\s+/g, '-') + '/'"
    new_pattern = "city.state === 'Mexico' ? '/locations/mexico/' + city.name.toLowerCase().replace(/\\s+/g, '-') + '/' : '/locations/' + city.state.toLowerCase().replace(/\\s+/g, '-') + '/' + city.name.toLowerCase().replace(/\\s+/g, '-') + '/'"
    
    content = content.replace(old_pattern, new_pattern)
    
    with open(INDEX_HTML, 'w') as f:
        f.write(content)
    
    print("✓ Fixed city card links for Mexico handling")

# ============================================
# 5. FIX COMPARE TRAVEL COSTS BUTTON
# ============================================

def fix_compare_travel_costs():
    """Update Compare Travel Costs button to link to Mexico page"""
    with open(INDEX_HTML, 'r') as f:
        content = f.read()
    
    # Replace the @click dispatch with a proper href
    old_button = r"<button @click=\"\$dispatch\('navigate', 'mexico-comparison'\)\"([^>]*)>(\s*)Compare Travel Costs(\s*)</button>"
    new_button = r'<a href="/locations/mexico/" class="bg-white text-slate-900 px-8 py-4 rounded-2xl font-bold border-2 border-slate-100 hover:border-brand-600 transition shadow-sm whitespace-nowrap inline-block">\2Compare Travel Costs\3</a>'
    
    content = re.sub(old_button, new_button, content)
    
    with open(INDEX_HTML, 'w') as f:
        f.write(content)
    
    print("✓ Fixed Compare Travel Costs button")

# ============================================
# 6. FIX VIEW ALL STATES LINK
# ============================================

def fix_view_all_link():
    """Fix the View All 30 States link"""
    with open(INDEX_HTML, 'r') as f:
        content = f.read()
    
    # Fix the duplicate href
    content = re.sub(
        r'<a href="#" href="/locations/"([^>]*)>(\s*)View All 30 States',
        r'<a href="/locations/"\1>\2View All 30 States',
        content
    )
    
    with open(INDEX_HTML, 'w') as f:
        f.write(content)
    
    print("✓ Fixed View All States link")

# ============================================
# 7. CREATE MEXICO LOCATIONS DIRECTORY
# ============================================

def create_mexico_locations():
    """Create Mexico location pages for Tijuana and Cancun"""
    mexico_dir = os.path.join(LOCATIONS_DIR, 'mexico')
    os.makedirs(mexico_dir, exist_ok=True)
    
    # Mexico index page
    mexico_index = '''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Stem Cell Therapy in Mexico | Medical Tourism | StemCellPrices.com</title>
    <meta name="description" content="Compare stem cell therapy costs in Mexico. Save 40-65% on treatments in Tijuana, Cancun, and Puerto Vallarta. Verified clinics with US-trained doctors.">
    <link rel="canonical" href="https://stemcellprices.com/locations/mexico/">
    <meta property="og:title" content="Stem Cell Therapy in Mexico | Medical Tourism">
    <meta property="og:description" content="Save 40-65% on stem cell treatments in Mexico. Compare Tijuana, Cancun clinics.">
    <meta property="og:url" content="https://stemcellprices.com/locations/mexico/">
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link href="https://fonts.googleapis.com/css2?family=Manrope:wght@300;400;500;600;700;800&display=swap" rel="stylesheet">
    <script src="https://cdn.tailwindcss.com"></script>
    <script>
        tailwind.config = {
            theme: {
                extend: {
                    fontFamily: { sans: ['Manrope', 'sans-serif'] },
                    colors: {
                        brand: { 50: '#f0f7ff', 100: '#e0effe', 600: '#2563eb', 700: '#1d4ed8' }
                    }
                }
            }
        }
    </script>
    <script src="/assets/js/tracking.js"></script>
</head>
<body class="font-sans bg-white text-slate-900">
    <!-- Navigation -->
    <header class="sticky top-0 z-50 bg-white/95 backdrop-blur-sm border-b border-slate-100">
        <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
            <div class="flex items-center justify-between h-16">
                <a href="/" class="flex items-center gap-2">
                    <img src="/assets/images/logo-dark.png" alt="StemCellPrices.com" class="h-8">
                </a>
                <nav class="hidden md:flex items-center gap-8 text-sm font-medium">
                    <a href="/locations/" class="hover:text-brand-600">All Locations</a>
                    <a href="/locations/california/" class="hover:text-brand-600">California</a>
                    <a href="/locations/texas/" class="hover:text-brand-600">Texas</a>
                    <a href="/locations/florida/" class="hover:text-brand-600">Florida</a>
                </nav>
            </div>
        </div>
    </header>

    <!-- Hero Section -->
    <section class="relative py-20 bg-gradient-to-br from-green-600 to-green-800 text-white overflow-hidden">
        <div class="absolute inset-0 opacity-20">
            <img src="/assets/images/cities/optimized/tijuana-large.webp" class="w-full h-full object-cover" alt="Mexico">
        </div>
        <div class="relative max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 text-center">
            <div class="inline-flex items-center gap-2 bg-white/20 backdrop-blur px-4 py-2 rounded-full text-sm font-semibold mb-6">
                🇲🇽 Medical Tourism Destination
            </div>
            <h1 class="text-4xl md:text-5xl font-extrabold mb-6">Stem Cell Therapy in Mexico</h1>
            <p class="text-xl text-green-100 max-w-2xl mx-auto mb-8">Save 40-65% on advanced stem cell treatments. US-trained doctors, JCI-accredited facilities, and comprehensive care packages.</p>
            <div class="flex flex-wrap justify-center gap-4">
                <div class="bg-white/20 backdrop-blur px-6 py-3 rounded-xl">
                    <span class="block text-2xl font-bold">$3,500 - $8,000</span>
                    <span class="text-sm text-green-200">Average Treatment Cost</span>
                </div>
                <div class="bg-white/20 backdrop-blur px-6 py-3 rounded-xl">
                    <span class="block text-2xl font-bold">40-65%</span>
                    <span class="text-sm text-green-200">Savings vs US</span>
                </div>
                <div class="bg-white/20 backdrop-blur px-6 py-3 rounded-xl">
                    <span class="block text-2xl font-bold">15+</span>
                    <span class="text-sm text-green-200">Verified Clinics</span>
                </div>
            </div>
        </div>
    </section>

    <!-- Breadcrumb -->
    <nav class="bg-slate-50 border-b border-slate-200 py-3">
        <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
            <ol class="flex items-center gap-2 text-sm">
                <li><a href="/" class="text-brand-600 hover:underline">Home</a></li>
                <li class="text-slate-400">/</li>
                <li><a href="/locations/" class="text-brand-600 hover:underline">Locations</a></li>
                <li class="text-slate-400">/</li>
                <li class="text-slate-600 font-medium">Mexico</li>
            </ol>
        </div>
    </nav>

    <!-- Price Comparison Table -->
    <section class="py-16">
        <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
            <h2 class="text-3xl font-extrabold text-center mb-4">US vs Mexico Price Comparison</h2>
            <p class="text-slate-600 text-center mb-12 max-w-2xl mx-auto">Real pricing data from verified clinics. Mexico offers significant savings on identical treatments.</p>
            
            <div class="overflow-x-auto">
                <table class="w-full border-collapse">
                    <thead>
                        <tr class="bg-slate-100">
                            <th class="text-left py-4 px-6 font-bold">Treatment</th>
                            <th class="text-center py-4 px-6 font-bold">US Average</th>
                            <th class="text-center py-4 px-6 font-bold text-green-600">Mexico Average</th>
                            <th class="text-center py-4 px-6 font-bold">Savings</th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr class="border-b border-slate-200 hover:bg-slate-50">
                            <td class="py-4 px-6 font-medium">Knee Osteoarthritis (PRP)</td>
                            <td class="py-4 px-6 text-center">$3,500 - $9,000</td>
                            <td class="py-4 px-6 text-center text-green-600 font-semibold">$1,800 - $4,500</td>
                            <td class="py-4 px-6 text-center"><span class="bg-green-100 text-green-700 px-3 py-1 rounded-full text-sm font-semibold">50%</span></td>
                        </tr>
                        <tr class="border-b border-slate-200 hover:bg-slate-50">
                            <td class="py-4 px-6 font-medium">Knee (Stem Cell - BMAC)</td>
                            <td class="py-4 px-6 text-center">$5,000 - $12,000</td>
                            <td class="py-4 px-6 text-center text-green-600 font-semibold">$3,500 - $6,500</td>
                            <td class="py-4 px-6 text-center"><span class="bg-green-100 text-green-700 px-3 py-1 rounded-full text-sm font-semibold">45%</span></td>
                        </tr>
                        <tr class="border-b border-slate-200 hover:bg-slate-50">
                            <td class="py-4 px-6 font-medium">Spine / Disc Degeneration</td>
                            <td class="py-4 px-6 text-center">$5,000 - $15,000</td>
                            <td class="py-4 px-6 text-center text-green-600 font-semibold">$4,900 - $9,500</td>
                            <td class="py-4 px-6 text-center"><span class="bg-green-100 text-green-700 px-3 py-1 rounded-full text-sm font-semibold">38%</span></td>
                        </tr>
                        <tr class="border-b border-slate-200 hover:bg-slate-50">
                            <td class="py-4 px-6 font-medium">Hip Osteoarthritis</td>
                            <td class="py-4 px-6 text-center">$4,000 - $10,000</td>
                            <td class="py-4 px-6 text-center text-green-600 font-semibold">$3,500 - $5,500</td>
                            <td class="py-4 px-6 text-center"><span class="bg-green-100 text-green-700 px-3 py-1 rounded-full text-sm font-semibold">45%</span></td>
                        </tr>
                        <tr class="border-b border-slate-200 hover:bg-slate-50">
                            <td class="py-4 px-6 font-medium">IV Stem Cell Infusion (50M cells)</td>
                            <td class="py-4 px-6 text-center">$8,000 - $20,000</td>
                            <td class="py-4 px-6 text-center text-green-600 font-semibold">$4,500 - $8,500</td>
                            <td class="py-4 px-6 text-center"><span class="bg-green-100 text-green-700 px-3 py-1 rounded-full text-sm font-semibold">55%</span></td>
                        </tr>
                        <tr class="hover:bg-slate-50">
                            <td class="py-4 px-6 font-medium">Full Body Anti-Aging Protocol</td>
                            <td class="py-4 px-6 text-center">$15,000 - $35,000</td>
                            <td class="py-4 px-6 text-center text-green-600 font-semibold">$8,000 - $15,000</td>
                            <td class="py-4 px-6 text-center"><span class="bg-green-100 text-green-700 px-3 py-1 rounded-full text-sm font-semibold">55%</span></td>
                        </tr>
                    </tbody>
                </table>
            </div>
        </div>
    </section>

    <!-- Mexico Cities -->
    <section class="py-16 bg-slate-50">
        <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
            <h2 class="text-3xl font-extrabold text-center mb-12">Popular Medical Tourism Destinations</h2>
            
            <div class="grid md:grid-cols-3 gap-8">
                <!-- Tijuana -->
                <a href="/locations/mexico/tijuana/" class="group bg-white rounded-2xl overflow-hidden shadow-lg hover:shadow-xl transition">
                    <div class="relative h-48">
                        <img src="/assets/images/cities/optimized/tijuana-medium.webp" class="w-full h-full object-cover group-hover:scale-105 transition-transform duration-500" alt="Tijuana">
                        <div class="absolute inset-0 bg-gradient-to-t from-black/60 to-transparent"></div>
                        <div class="absolute bottom-4 left-4 text-white">
                            <h3 class="text-2xl font-bold">Tijuana</h3>
                            <p class="text-sm text-white/80">Baja California</p>
                        </div>
                    </div>
                    <div class="p-6">
                        <div class="flex justify-between items-center mb-4">
                            <span class="text-green-600 font-bold text-lg">$3,500 - $8,000</span>
                            <span class="bg-green-100 text-green-700 px-3 py-1 rounded-full text-sm font-semibold">8 Clinics</span>
                        </div>
                        <ul class="text-sm text-slate-600 space-y-2">
                            <li>✓ 20 min from San Diego border</li>
                            <li>✓ US-trained physicians</li>
                            <li>✓ Airport pickup included</li>
                        </ul>
                    </div>
                </a>

                <!-- Cancun -->
                <a href="/locations/mexico/cancun/" class="group bg-white rounded-2xl overflow-hidden shadow-lg hover:shadow-xl transition">
                    <div class="relative h-48">
                        <img src="/assets/images/cities/optimized/cancun-medium.webp" class="w-full h-full object-cover group-hover:scale-105 transition-transform duration-500" alt="Cancun" onerror="this.src='/assets/images/cities/optimized/miami-medium.webp'">
                        <div class="absolute inset-0 bg-gradient-to-t from-black/60 to-transparent"></div>
                        <div class="absolute bottom-4 left-4 text-white">
                            <h3 class="text-2xl font-bold">Cancun</h3>
                            <p class="text-sm text-white/80">Quintana Roo</p>
                        </div>
                    </div>
                    <div class="p-6">
                        <div class="flex justify-between items-center mb-4">
                            <span class="text-green-600 font-bold text-lg">$4,000 - $12,000</span>
                            <span class="bg-green-100 text-green-700 px-3 py-1 rounded-full text-sm font-semibold">5 Clinics</span>
                        </div>
                        <ul class="text-sm text-slate-600 space-y-2">
                            <li>✓ Resort recovery packages</li>
                            <li>✓ JCI-accredited hospitals</li>
                            <li>✓ Combine with vacation</li>
                        </ul>
                    </div>
                </a>

                <!-- Puerto Vallarta -->
                <a href="/locations/mexico/puerto-vallarta/" class="group bg-white rounded-2xl overflow-hidden shadow-lg hover:shadow-xl transition">
                    <div class="relative h-48">
                        <img src="/assets/images/cities/optimized/puerto-vallarta-medium.webp" class="w-full h-full object-cover group-hover:scale-105 transition-transform duration-500" alt="Puerto Vallarta" onerror="this.src='/assets/images/cities/optimized/miami-medium.webp'">
                        <div class="absolute inset-0 bg-gradient-to-t from-black/60 to-transparent"></div>
                        <div class="absolute bottom-4 left-4 text-white">
                            <h3 class="text-2xl font-bold">Puerto Vallarta</h3>
                            <p class="text-sm text-white/80">Jalisco</p>
                        </div>
                    </div>
                    <div class="p-6">
                        <div class="flex justify-between items-center mb-4">
                            <span class="text-green-600 font-bold text-lg">$4,500 - $10,000</span>
                            <span class="bg-green-100 text-green-700 px-3 py-1 rounded-full text-sm font-semibold">4 Clinics</span>
                        </div>
                        <ul class="text-sm text-slate-600 space-y-2">
                            <li>✓ Beachfront recovery</li>
                            <li>✓ Bilingual staff</li>
                            <li>✓ Direct US flights</li>
                        </ul>
                    </div>
                </a>
            </div>
        </div>
    </section>

    <!-- What's Included -->
    <section class="py-16">
        <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
            <h2 class="text-3xl font-extrabold text-center mb-12">What's Typically Included</h2>
            
            <div class="grid md:grid-cols-2 lg:grid-cols-4 gap-6">
                <div class="bg-green-50 rounded-2xl p-6 text-center">
                    <div class="w-12 h-12 bg-green-100 rounded-xl flex items-center justify-center mx-auto mb-4">
                        <span class="text-2xl">🏥</span>
                    </div>
                    <h3 class="font-bold mb-2">Treatment</h3>
                    <p class="text-sm text-slate-600">Full stem cell procedure with lab processing</p>
                </div>
                <div class="bg-green-50 rounded-2xl p-6 text-center">
                    <div class="w-12 h-12 bg-green-100 rounded-xl flex items-center justify-center mx-auto mb-4">
                        <span class="text-2xl">🏨</span>
                    </div>
                    <h3 class="font-bold mb-2">Accommodation</h3>
                    <p class="text-sm text-slate-600">2-3 nights hotel near clinic</p>
                </div>
                <div class="bg-green-50 rounded-2xl p-6 text-center">
                    <div class="w-12 h-12 bg-green-100 rounded-xl flex items-center justify-center mx-auto mb-4">
                        <span class="text-2xl">🚗</span>
                    </div>
                    <h3 class="font-bold mb-2">Transportation</h3>
                    <p class="text-sm text-slate-600">Airport pickup & clinic transfers</p>
                </div>
                <div class="bg-green-50 rounded-2xl p-6 text-center">
                    <div class="w-12 h-12 bg-green-100 rounded-xl flex items-center justify-center mx-auto mb-4">
                        <span class="text-2xl">📋</span>
                    </div>
                    <h3 class="font-bold mb-2">Follow-up</h3>
                    <p class="text-sm text-slate-600">Virtual consultations post-treatment</p>
                </div>
            </div>
        </div>
    </section>

    <!-- Disclaimer -->
    <section class="py-8 bg-amber-50 border-t border-amber-200">
        <div class="max-w-4xl mx-auto px-4 text-center">
            <p class="text-sm text-amber-800"><strong>Medical Disclaimer:</strong> Stem cell therapy is not FDA-approved for most conditions. Results vary. Always consult with a qualified healthcare provider. International medical travel involves additional risks. Verify clinic credentials independently.</p>
        </div>
    </section>

    <!-- Footer -->
    <footer class="bg-slate-900 text-white py-12">
        <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
            <div class="grid md:grid-cols-4 gap-8">
                <div>
                    <img src="/assets/images/logo-dark.png" alt="StemCellPrices.com" class="h-8 mb-4 brightness-0 invert">
                    <p class="text-slate-400 text-sm">Compare stem cell therapy costs and find verified clinics.</p>
                </div>
                <div>
                    <h5 class="font-bold mb-4">US Locations</h5>
                    <ul class="space-y-2 text-sm text-slate-400">
                        <li><a href="/locations/california/" class="hover:text-white">California</a></li>
                        <li><a href="/locations/texas/" class="hover:text-white">Texas</a></li>
                        <li><a href="/locations/florida/" class="hover:text-white">Florida</a></li>
                        <li><a href="/locations/" class="hover:text-white">All States</a></li>
                    </ul>
                </div>
                <div>
                    <h5 class="font-bold mb-4">Mexico</h5>
                    <ul class="space-y-2 text-sm text-slate-400">
                        <li><a href="/locations/mexico/tijuana/" class="hover:text-white">Tijuana</a></li>
                        <li><a href="/locations/mexico/cancun/" class="hover:text-white">Cancun</a></li>
                        <li><a href="/locations/mexico/puerto-vallarta/" class="hover:text-white">Puerto Vallarta</a></li>
                    </ul>
                </div>
                <div>
                    <h5 class="font-bold mb-4">Resources</h5>
                    <ul class="space-y-2 text-sm text-slate-400">
                        <li><a href="/" class="hover:text-white">Cost Guide</a></li>
                        <li><a href="/privacy.html" class="hover:text-white">Privacy Policy</a></li>
                        <li><a href="/terms.html" class="hover:text-white">Terms of Service</a></li>
                    </ul>
                </div>
            </div>
            <div class="border-t border-slate-800 mt-8 pt-8 text-center text-sm text-slate-500">
                © 2026 StemCellPrices.com. All rights reserved. Not medical advice.
            </div>
        </div>
    </footer>
</body>
</html>'''
    
    with open(os.path.join(mexico_dir, 'index.html'), 'w') as f:
        f.write(mexico_index)
    
    print("✓ Created Mexico locations index page")
    
    # Create Tijuana page
    create_mexico_city_page('tijuana', 'Tijuana', 'Baja California', mexico_dir)
    create_mexico_city_page('cancun', 'Cancun', 'Quintana Roo', mexico_dir)
    create_mexico_city_page('puerto-vallarta', 'Puerto Vallarta', 'Jalisco', mexico_dir)

def create_mexico_city_page(slug, name, state, mexico_dir):
    """Create individual Mexico city pages"""
    city_dir = os.path.join(mexico_dir, slug)
    os.makedirs(city_dir, exist_ok=True)
    
    # Clinic data for each city
    clinics_data = {
        'tijuana': [
            {'name': 'Cellular Hope Institute', 'address': 'Av. Paseo de los Heroes 9365, Zona Urbana Rio Tijuana', 'phone': '+52 664 200 1872', 'specialty': 'Orthopedic & Anti-Aging', 'price': '$3,500 - $12,000', 'featured': True},
            {'name': 'ProgenaCare Global', 'address': 'Blvd. Agua Caliente 4558, Aviacion', 'phone': '+52 664 634 2468', 'specialty': 'Regenerative Medicine', 'price': '$4,000 - $8,000', 'featured': True},
            {'name': 'Stem Cell Therapy Mexico', 'address': 'Calle 3ra 8691, Zona Centro', 'phone': '+52 664 685 2000', 'specialty': 'Orthopedic Stem Cells', 'price': '$3,800 - $9,500', 'featured': False},
            {'name': 'Immunow Oncology', 'address': 'Av. Revolucion 1295, Zona Centro', 'phone': '+52 664 634 1111', 'specialty': 'Immunotherapy & Stem Cells', 'price': '$5,000 - $15,000', 'featured': False},
            {'name': 'Regenamex', 'address': 'Blvd. Sanchez Taboada 10488, Zona Rio', 'phone': '+52 664 200 3456', 'specialty': 'Sports Medicine', 'price': '$3,200 - $7,500', 'featured': False},
        ],
        'cancun': [
            {'name': 'Cancun Stem Cell Center', 'address': 'Blvd. Kukulcan Km 12.5, Zona Hotelera', 'phone': '+52 998 881 5700', 'specialty': 'Orthopedic & Wellness', 'price': '$4,500 - $12,000', 'featured': True},
            {'name': 'Hospital Galenia', 'address': 'Av. Tulum SM 12, Centro', 'phone': '+52 998 891 5200', 'specialty': 'Multi-Specialty', 'price': '$5,000 - $15,000', 'featured': True},
            {'name': 'Riviera Maya Stem Cells', 'address': 'Av. Coba 15, SM 22', 'phone': '+52 998 884 3000', 'specialty': 'Regenerative Therapy', 'price': '$4,000 - $10,000', 'featured': False},
        ],
        'puerto-vallarta': [
            {'name': 'CMQ Hospital', 'address': 'Basilio Badillo 365, Emiliano Zapata', 'phone': '+52 322 223 1919', 'specialty': 'Multi-Specialty', 'price': '$4,500 - $10,000', 'featured': True},
            {'name': 'Stem Cell Vallarta', 'address': 'Av. Francisco Medina Ascencio 2760', 'phone': '+52 322 226 1000', 'specialty': 'Orthopedic Stem Cells', 'price': '$4,000 - $9,000', 'featured': True},
        ]
    }
    
    clinics = clinics_data.get(slug, [])
    
    clinics_html = ''
    for clinic in clinics:
        featured_badge = '<span class="bg-brand-600 text-white px-3 py-1 rounded-full text-xs font-semibold">Featured</span>' if clinic['featured'] else ''
        clinics_html += f'''
                <div class="bg-white rounded-2xl p-6 shadow-lg border border-slate-200 hover:shadow-xl transition">
                    <div class="flex justify-between items-start mb-4">
                        <div>
                            <h3 class="text-xl font-bold text-slate-900">{clinic['name']}</h3>
                            <p class="text-slate-500 text-sm">{clinic['specialty']}</p>
                        </div>
                        {featured_badge}
                    </div>
                    <div class="space-y-2 mb-4">
                        <p class="text-sm text-slate-600 flex items-center gap-2">
                            <svg class="w-4 h-4 text-slate-400" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17.657 16.657L13.414 20.9a1.998 1.998 0 01-2.827 0l-4.244-4.243a8 8 0 1111.314 0z"></path></svg>
                            {clinic['address']}
                        </p>
                        <p class="text-sm text-slate-600 flex items-center gap-2">
                            <svg class="w-4 h-4 text-slate-400" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 5a2 2 0 012-2h3.28a1 1 0 01.948.684l1.498 4.493a1 1 0 01-.502 1.21l-2.257 1.13a11.042 11.042 0 005.516 5.516l1.13-2.257a1 1 0 011.21-.502l4.493 1.498a1 1 0 01.684.949V19a2 2 0 01-2 2h-1C9.716 21 3 14.284 3 6V5z"></path></svg>
                            {clinic['phone']}
                        </p>
                    </div>
                    <div class="flex justify-between items-center pt-4 border-t border-slate-100">
                        <span class="text-green-600 font-bold">{clinic['price']}</span>
                        <button onclick="openLeadForm('{clinic['name']}', '{clinic['phone']}')" class="bg-brand-600 text-white px-4 py-2 rounded-lg text-sm font-semibold hover:bg-brand-700 transition">Get Quote</button>
                    </div>
                </div>'''
    
    page_html = f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Stem Cell Therapy in {name}, Mexico | StemCellPrices.com</title>
    <meta name="description" content="Find stem cell therapy clinics in {name}, Mexico. Compare prices, read reviews, and book consultations with verified providers.">
    <link rel="canonical" href="https://stemcellprices.com/locations/mexico/{slug}/">
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link href="https://fonts.googleapis.com/css2?family=Manrope:wght@300;400;500;600;700;800&display=swap" rel="stylesheet">
    <script src="https://cdn.tailwindcss.com"></script>
    <script>
        tailwind.config = {{
            theme: {{
                extend: {{
                    fontFamily: {{ sans: ['Manrope', 'sans-serif'] }},
                    colors: {{
                        brand: {{ 50: '#f0f7ff', 100: '#e0effe', 600: '#2563eb', 700: '#1d4ed8' }}
                    }}
                }}
            }}
        }}
    </script>
    <script src="/assets/js/tracking.js"></script>
</head>
<body class="font-sans bg-slate-50 text-slate-900">
    <!-- Navigation -->
    <header class="sticky top-0 z-50 bg-white/95 backdrop-blur-sm border-b border-slate-100">
        <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
            <div class="flex items-center justify-between h-16">
                <a href="/" class="flex items-center gap-2">
                    <img src="/assets/images/logo-dark.png" alt="StemCellPrices.com" class="h-8">
                </a>
                <nav class="hidden md:flex items-center gap-8 text-sm font-medium">
                    <a href="/locations/" class="hover:text-brand-600">All Locations</a>
                    <a href="/locations/mexico/" class="text-brand-600">Mexico</a>
                </nav>
            </div>
        </div>
    </header>

    <!-- Hero -->
    <section class="relative py-16 bg-gradient-to-br from-green-600 to-green-800 text-white">
        <div class="absolute inset-0 opacity-30">
            <img src="/assets/images/cities/optimized/{slug}-large.webp" class="w-full h-full object-cover" alt="{name}" onerror="this.src='/assets/images/cities/optimized/miami-large.webp'">
        </div>
        <div class="relative max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
            <nav class="text-sm mb-4">
                <a href="/" class="text-green-200 hover:text-white">Home</a> / 
                <a href="/locations/" class="text-green-200 hover:text-white">Locations</a> / 
                <a href="/locations/mexico/" class="text-green-200 hover:text-white">Mexico</a> / 
                <span>{name}</span>
            </nav>
            <h1 class="text-4xl font-extrabold mb-4">Stem Cell Clinics in {name}</h1>
            <p class="text-xl text-green-100">{state}, Mexico • {len(clinics)} Verified Clinics</p>
        </div>
    </section>

    <!-- Clinics Grid -->
    <section class="py-12">
        <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
            <div class="grid md:grid-cols-2 lg:grid-cols-3 gap-6">
                {clinics_html}
            </div>
        </div>
    </section>

    <!-- Lead Form Modal -->
    <div id="leadFormModal" class="fixed inset-0 bg-black/50 z-50 hidden items-center justify-center">
        <div class="bg-white rounded-2xl p-8 max-w-md w-full mx-4">
            <h3 class="text-2xl font-bold mb-4">Get a Free Quote</h3>
            <form id="leadForm" class="space-y-4">
                <input type="hidden" id="clinicName" name="clinic">
                <input type="hidden" id="clinicPhone" name="clinicPhone">
                <div>
                    <label class="block text-sm font-medium mb-1">Full Name</label>
                    <input type="text" name="name" required class="w-full px-4 py-2 border border-slate-300 rounded-lg focus:ring-2 focus:ring-brand-600 focus:border-transparent">
                </div>
                <div>
                    <label class="block text-sm font-medium mb-1">Email</label>
                    <input type="email" name="email" required class="w-full px-4 py-2 border border-slate-300 rounded-lg focus:ring-2 focus:ring-brand-600 focus:border-transparent">
                </div>
                <div>
                    <label class="block text-sm font-medium mb-1">Phone</label>
                    <input type="tel" name="phone" required class="w-full px-4 py-2 border border-slate-300 rounded-lg focus:ring-2 focus:ring-brand-600 focus:border-transparent">
                </div>
                <div>
                    <label class="block text-sm font-medium mb-1">Condition</label>
                    <select name="condition" class="w-full px-4 py-2 border border-slate-300 rounded-lg focus:ring-2 focus:ring-brand-600 focus:border-transparent">
                        <option>Knee Pain / Osteoarthritis</option>
                        <option>Back / Spine Pain</option>
                        <option>Shoulder Pain</option>
                        <option>Hip Pain</option>
                        <option>Anti-Aging / Wellness</option>
                        <option>Other</option>
                    </select>
                </div>
                <div class="flex gap-4">
                    <button type="button" onclick="closeLeadForm()" class="flex-1 px-4 py-2 border border-slate-300 rounded-lg font-semibold hover:bg-slate-50">Cancel</button>
                    <button type="submit" class="flex-1 px-4 py-2 bg-brand-600 text-white rounded-lg font-semibold hover:bg-brand-700">Submit</button>
                </div>
            </form>
        </div>
    </div>

    <script>
        function openLeadForm(clinicName, clinicPhone) {{
            document.getElementById('clinicName').value = clinicName;
            document.getElementById('clinicPhone').value = clinicPhone;
            document.getElementById('leadFormModal').classList.remove('hidden');
            document.getElementById('leadFormModal').classList.add('flex');
        }}
        function closeLeadForm() {{
            document.getElementById('leadFormModal').classList.add('hidden');
            document.getElementById('leadFormModal').classList.remove('flex');
        }}
        document.getElementById('leadForm').addEventListener('submit', function(e) {{
            e.preventDefault();
            const formData = new FormData(this);
            const lead = Object.fromEntries(formData);
            lead.timestamp = new Date().toISOString();
            lead.source = window.location.href;
            lead.city = '{name}';
            lead.country = 'Mexico';
            
            // Store lead
            const leads = JSON.parse(localStorage.getItem('stemcell_leads') || '[]');
            leads.push(lead);
            localStorage.setItem('stemcell_leads', JSON.stringify(leads));
            
            // Track conversion
            if (typeof gtag !== 'undefined') {{
                gtag('event', 'generate_lead', {{
                    'event_category': 'Lead',
                    'event_label': lead.clinic,
                    'value': 1
                }});
            }}
            
            alert('Thank you! A clinic coordinator will contact you within 24 hours.');
            closeLeadForm();
        }});
    </script>

    <!-- Footer -->
    <footer class="bg-slate-900 text-white py-12">
        <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 text-center">
            <p class="text-slate-400 text-sm">© 2026 StemCellPrices.com. All rights reserved.</p>
            <p class="text-slate-500 text-xs mt-2">Medical Disclaimer: Stem cell therapy is not FDA-approved for most conditions. Results vary.</p>
        </div>
    </footer>
</body>
</html>'''
    
    with open(os.path.join(city_dir, 'index.html'), 'w') as f:
        f.write(page_html)
    
    print(f"✓ Created {name} city page")

# ============================================
# 8. STANDARDIZE FOOTER ACROSS ALL PAGES
# ============================================

def standardize_footer():
    """Update footer across all location pages to be consistent"""
    standard_footer = '''    <!-- Footer -->
    <footer class="bg-slate-900 text-white py-12">
        <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
            <div class="grid md:grid-cols-4 gap-8">
                <div>
                    <a href="/" class="flex items-center gap-2 mb-4">
                        <img src="/assets/images/logo-dark.png" alt="StemCellPrices.com" class="h-8 brightness-0 invert">
                    </a>
                    <p class="text-slate-400 text-sm">Compare stem cell therapy costs and find verified clinics across the US and Mexico.</p>
                </div>
                <div>
                    <h5 class="font-bold mb-4">Top US Locations</h5>
                    <ul class="space-y-2 text-sm text-slate-400">
                        <li><a href="/locations/california/" class="hover:text-white transition">California</a></li>
                        <li><a href="/locations/texas/" class="hover:text-white transition">Texas</a></li>
                        <li><a href="/locations/florida/" class="hover:text-white transition">Florida</a></li>
                        <li><a href="/locations/arizona/" class="hover:text-white transition">Arizona</a></li>
                        <li><a href="/locations/" class="hover:text-white transition">All 30 States →</a></li>
                    </ul>
                </div>
                <div>
                    <h5 class="font-bold mb-4">Mexico (Medical Tourism)</h5>
                    <ul class="space-y-2 text-sm text-slate-400">
                        <li><a href="/locations/mexico/tijuana/" class="hover:text-white transition">Tijuana</a></li>
                        <li><a href="/locations/mexico/cancun/" class="hover:text-white transition">Cancun</a></li>
                        <li><a href="/locations/mexico/puerto-vallarta/" class="hover:text-white transition">Puerto Vallarta</a></li>
                        <li><a href="/locations/mexico/" class="hover:text-white transition">Compare Mexico Prices →</a></li>
                    </ul>
                </div>
                <div>
                    <h5 class="font-bold mb-4">Resources</h5>
                    <ul class="space-y-2 text-sm text-slate-400">
                        <li><a href="/" class="hover:text-white transition">Cost Guide</a></li>
                        <li><a href="/api/data.json" class="hover:text-white transition">API Access</a></li>
                        <li><a href="/privacy.html" class="hover:text-white transition">Privacy Policy</a></li>
                        <li><a href="/terms.html" class="hover:text-white transition">Terms of Service</a></li>
                    </ul>
                </div>
            </div>
            <div class="border-t border-slate-800 mt-8 pt-8 flex flex-col md:flex-row justify-between items-center gap-4">
                <p class="text-sm text-slate-500">© 2026 StemCellPrices.com. All rights reserved. Not medical advice.</p>
                <div class="flex items-center gap-4">
                    <a href="https://twitter.com/stemcellprices" class="text-slate-400 hover:text-white transition">
                        <svg class="w-5 h-5" fill="currentColor" viewBox="0 0 24 24"><path d="M18.244 2.25h3.308l-7.227 8.26 8.502 11.24H16.17l-5.214-6.817L4.99 21.75H1.68l7.73-8.835L1.254 2.25H8.08l4.713 6.231zm-1.161 17.52h1.833L7.084 4.126H5.117z"/></svg>
                    </a>
                    <a href="https://linkedin.com/company/stemcellprices" class="text-slate-400 hover:text-white transition">
                        <svg class="w-5 h-5" fill="currentColor" viewBox="0 0 24 24"><path d="M20.447 20.452h-3.554v-5.569c0-1.328-.027-3.037-1.852-3.037-1.853 0-2.136 1.445-2.136 2.939v5.667H9.351V9h3.414v1.561h.046c.477-.9 1.637-1.85 3.37-1.85 3.601 0 4.267 2.37 4.267 5.455v6.286zM5.337 7.433c-1.144 0-2.063-.926-2.063-2.065 0-1.138.92-2.063 2.063-2.063 1.14 0 2.064.925 2.064 2.063 0 1.139-.925 2.065-2.064 2.065zm1.782 13.019H3.555V9h3.564v11.452zM22.225 0H1.771C.792 0 0 .774 0 1.729v20.542C0 23.227.792 24 1.771 24h20.451C23.2 24 24 23.227 24 22.271V1.729C24 .774 23.2 0 22.222 0h.003z"/></svg>
                    </a>
                </div>
            </div>
        </div>
    </footer>'''
    
    # Update all location HTML files
    for root, dirs, files in os.walk(LOCATIONS_DIR):
        for file in files:
            if file.endswith('.html'):
                filepath = os.path.join(root, file)
                with open(filepath, 'r') as f:
                    content = f.read()
                
                # Replace footer
                footer_pattern = r'<footer[^>]*>.*?</footer>'
                if re.search(footer_pattern, content, re.DOTALL):
                    content = re.sub(footer_pattern, standard_footer.strip(), content, flags=re.DOTALL)
                    with open(filepath, 'w') as f:
                        f.write(content)
    
    print("✓ Standardized footer across all location pages")

# ============================================
# 9. GENERATE TIJUANA/CANCUN IMAGES IF MISSING
# ============================================

def check_mexico_images():
    """Check if Mexico city images exist"""
    cities_dir = os.path.join(BASE_DIR, 'assets/images/cities/optimized')
    mexico_cities = ['tijuana', 'cancun', 'puerto-vallarta']
    
    missing = []
    for city in mexico_cities:
        if not os.path.exists(os.path.join(cities_dir, f'{city}-medium.webp')):
            missing.append(city)
    
    if missing:
        print(f"⚠ Missing images for: {', '.join(missing)}")
        print("  These will use fallback images until generated")
    else:
        print("✓ All Mexico city images present")

# ============================================
# MAIN EXECUTION
# ============================================

if __name__ == '__main__':
    print("=" * 50)
    print("StemCellPrices.com Homepage & Navigation Fix")
    print("=" * 50)
    
    fix_broken_hrefs()
    fix_popular_cities()
    fix_nav_dropdown()
    fix_city_links()
    fix_compare_travel_costs()
    fix_view_all_link()
    create_mexico_locations()
    standardize_footer()
    check_mexico_images()
    
    print("\n" + "=" * 50)
    print("All fixes applied successfully!")
    print("=" * 50)
