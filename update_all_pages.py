#!/usr/bin/env python3
"""
Update all HTML pages with standardized navigation and footer
"""
import os
import re
from pathlib import Path

# Standard navigation HTML
STANDARD_NAV = '''<header class="bg-white shadow-sm sticky top-0 z-50">
    <nav class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div class="flex justify-between h-16">
            <div class="flex items-center">
                <a href="/" class="flex items-center">
                    <img src="/assets/images/logo-dark.png" alt="StemCellPrices.com" class="h-8 w-auto">
                </a>
            </div>
            <div class="hidden md:flex items-center space-x-8">
                <a href="/" class="text-gray-700 hover:text-teal-600 font-medium">Home</a>
                <a href="/#cost-guide" class="text-gray-700 hover:text-teal-600 font-medium">Cost Guide</a>
                <div class="relative group">
                    <a href="/locations/" class="text-gray-700 hover:text-teal-600 font-medium inline-flex items-center">
                        Locations
                        <svg class="ml-1 h-4 w-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7"></path>
                        </svg>
                    </a>
                    <div class="absolute left-0 mt-0 w-56 opacity-0 invisible group-hover:opacity-100 group-hover:visible transition-all duration-200 ease-in-out z-50">
                        <div class="pt-2">
                            <div class="bg-white rounded-lg shadow-lg ring-1 ring-black ring-opacity-5 py-2">
                                <a href="/locations/" class="block px-4 py-2 text-sm text-gray-700 hover:bg-teal-50 hover:text-teal-600">All Locations</a>
                                <div class="border-t border-gray-100 my-1"></div>
                                <p class="px-4 py-1 text-xs text-gray-400 uppercase tracking-wider">Popular States</p>
                                <a href="/locations/california/" class="block px-4 py-2 text-sm text-gray-700 hover:bg-teal-50 hover:text-teal-600">California</a>
                                <a href="/locations/texas/" class="block px-4 py-2 text-sm text-gray-700 hover:bg-teal-50 hover:text-teal-600">Texas</a>
                                <a href="/locations/florida/" class="block px-4 py-2 text-sm text-gray-700 hover:bg-teal-50 hover:text-teal-600">Florida</a>
                                <a href="/locations/arizona/" class="block px-4 py-2 text-sm text-gray-700 hover:bg-teal-50 hover:text-teal-600">Arizona</a>
                                <a href="/locations/new-york/" class="block px-4 py-2 text-sm text-gray-700 hover:bg-teal-50 hover:text-teal-600">New York</a>
                                <div class="border-t border-gray-100 my-1"></div>
                                <p class="px-4 py-1 text-xs text-gray-400 uppercase tracking-wider">International</p>
                                <a href="/locations/mexico/" class="block px-4 py-2 text-sm text-gray-700 hover:bg-teal-50 hover:text-teal-600">🇲🇽 Mexico</a>
                                <div class="border-t border-gray-100 my-1"></div>
                                <a href="/locations/" class="block px-4 py-2 text-sm text-teal-600 font-medium hover:bg-teal-50">View All 30+ States →</a>
                            </div>
                        </div>
                    </div>
                </div>
                <a href="/compare-costs/" class="text-gray-700 hover:text-teal-600 font-medium">Compare Costs</a>
            </div>
            <div class="flex items-center md:hidden">
                <button type="button" onclick="document.getElementById('mobile-menu').classList.toggle('hidden')" class="text-gray-700 hover:text-teal-600">
                    <svg class="h-6 w-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 12h16M4 18h16"></path>
                    </svg>
                </button>
            </div>
        </div>
        <!-- Mobile menu -->
        <div id="mobile-menu" class="hidden md:hidden pb-4">
            <a href="/" class="block py-2 text-gray-700 hover:text-teal-600">Home</a>
            <a href="/#cost-guide" class="block py-2 text-gray-700 hover:text-teal-600">Cost Guide</a>
            <a href="/locations/" class="block py-2 text-gray-700 hover:text-teal-600">All Locations</a>
            <a href="/locations/california/" class="block py-2 pl-4 text-gray-600 hover:text-teal-600">→ California</a>
            <a href="/locations/texas/" class="block py-2 pl-4 text-gray-600 hover:text-teal-600">→ Texas</a>
            <a href="/locations/florida/" class="block py-2 pl-4 text-gray-600 hover:text-teal-600">→ Florida</a>
            <a href="/locations/mexico/" class="block py-2 pl-4 text-gray-600 hover:text-teal-600">→ Mexico</a>
            <a href="/compare-costs/" class="block py-2 text-gray-700 hover:text-teal-600">Compare Costs</a>
        </div>
    </nav>
</header>'''

# Standard footer HTML
STANDARD_FOOTER = '''<footer class="bg-gray-900 text-white">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
        <div class="grid grid-cols-1 md:grid-cols-4 gap-8">
            <div class="col-span-1 md:col-span-1">
                <a href="/" class="flex items-center mb-4">
                    <img src="/assets/images/logo-dark.png" alt="StemCellPrices.com" class="h-8 w-auto brightness-0 invert">
                </a>
                <p class="text-gray-400 text-sm">Compare stem cell therapy costs across the US and Mexico. Find verified clinics and transparent pricing.</p>
            </div>
            <div>
                <h3 class="text-white font-semibold mb-4">Popular States</h3>
                <ul class="space-y-2">
                    <li><a href="/locations/california/" class="text-gray-400 hover:text-teal-400 text-sm">California</a></li>
                    <li><a href="/locations/texas/" class="text-gray-400 hover:text-teal-400 text-sm">Texas</a></li>
                    <li><a href="/locations/florida/" class="text-gray-400 hover:text-teal-400 text-sm">Florida</a></li>
                    <li><a href="/locations/arizona/" class="text-gray-400 hover:text-teal-400 text-sm">Arizona</a></li>
                </ul>
            </div>
            <div>
                <h3 class="text-white font-semibold mb-4">Mexico</h3>
                <ul class="space-y-2">
                    <li><a href="/locations/mexico/" class="text-gray-400 hover:text-teal-400 text-sm">Mexico Overview</a></li>
                    <li><a href="/locations/mexico/tijuana/" class="text-gray-400 hover:text-teal-400 text-sm">Tijuana</a></li>
                    <li><a href="/locations/mexico/cancun/" class="text-gray-400 hover:text-teal-400 text-sm">Cancun</a></li>
                    <li><a href="/locations/mexico/puerto-vallarta/" class="text-gray-400 hover:text-teal-400 text-sm">Puerto Vallarta</a></li>
                </ul>
            </div>
            <div>
                <h3 class="text-white font-semibold mb-4">Resources</h3>
                <ul class="space-y-2">
                    <li><a href="/#cost-guide" class="text-gray-400 hover:text-teal-400 text-sm">Cost Guide</a></li>
                    <li><a href="/compare-costs/" class="text-gray-400 hover:text-teal-400 text-sm">Compare Costs</a></li>
                    <li><a href="/locations/" class="text-gray-400 hover:text-teal-400 text-sm">All Locations</a></li>
                </ul>
            </div>
        </div>
        <div class="border-t border-gray-800 mt-8 pt-8 text-center">
            <p class="text-gray-400 text-sm">&copy; 2025 StemCellPrices.com. All rights reserved.</p>
        </div>
    </div>
</footer>'''

def update_html_file(filepath):
    """Update a single HTML file with standardized nav and footer"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original = content
        
        # Skip if already has the new nav (check for group-hover pattern)
        if 'group-hover:opacity-100 group-hover:visible' in content:
            return False
        
        # Replace header/nav section
        # Pattern 1: <header...>...</header>
        header_pattern = r'<header[^>]*>.*?</header>'
        if re.search(header_pattern, content, re.DOTALL):
            content = re.sub(header_pattern, STANDARD_NAV, content, flags=re.DOTALL)
        
        # Replace footer section
        footer_pattern = r'<footer[^>]*>.*?</footer>'
        if re.search(footer_pattern, content, re.DOTALL):
            content = re.sub(footer_pattern, STANDARD_FOOTER, content, flags=re.DOTALL)
        
        if content != original:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            return True
        return False
    except Exception as e:
        print(f"Error updating {filepath}: {e}")
        return False

def main():
    base_dir = Path('/home/ubuntu/stem-cells')
    updated = 0
    
    # Find all HTML files
    html_files = list(base_dir.glob('**/*.html'))
    
    # Exclude certain directories
    exclude_dirs = ['node_modules', '.git', 'admin']
    
    for filepath in html_files:
        # Skip excluded directories
        if any(excl in str(filepath) for excl in exclude_dirs):
            continue
        
        if update_html_file(filepath):
            updated += 1
            print(f"✓ Updated: {filepath.relative_to(base_dir)}")
    
    print(f"\n{'='*50}")
    print(f"Updated {updated} HTML files")
    print(f"{'='*50}")

if __name__ == '__main__':
    main()
