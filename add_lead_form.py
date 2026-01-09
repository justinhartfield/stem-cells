#!/usr/bin/env python3
"""
Replace Call Now buttons with lead capture onboarding forms on all clinic pages.
"""

import os
import re
from pathlib import Path

# The lead capture form HTML to replace the Call Now button
LEAD_FORM_HTML = '''<div x-data="{ 
                            showForm: false, 
                            submitted: false,
                            formData: {
                                name: '',
                                email: '',
                                phone: '',
                                condition: '',
                                message: ''
                            },
                            submitForm() {
                                // Store lead data in localStorage for now
                                const leads = JSON.parse(localStorage.getItem('stemCellLeads') || '[]');
                                leads.push({
                                    ...this.formData,
                                    clinic: '{clinic_name}',
                                    clinicPhone: '{clinic_phone}',
                                    city: '{city}',
                                    state: '{state}',
                                    timestamp: new Date().toISOString(),
                                    source: window.location.href
                                });
                                localStorage.setItem('stemCellLeads', JSON.stringify(leads));
                                this.submitted = true;
                                
                                // Also send to webhook if configured
                                fetch('https://hooks.zapier.com/hooks/catch/YOUR_WEBHOOK_ID/', {
                                    method: 'POST',
                                    headers: { 'Content-Type': 'application/json' },
                                    body: JSON.stringify({
                                        ...this.formData,
                                        clinic: '{clinic_name}',
                                        clinicPhone: '{clinic_phone}',
                                        city: '{city}',
                                        state: '{state}',
                                        timestamp: new Date().toISOString(),
                                        source: window.location.href
                                    })
                                }).catch(() => {});
                            }
                        }">
                            <!-- Initial CTA Button -->
                            <button x-show="!showForm && !submitted" 
                                    @click="showForm = true"
                                    class="w-full bg-blue-600 text-white text-center px-6 py-3 rounded-lg hover:bg-blue-700 transition font-medium">
                                Get Free Consultation
                            </button>
                            
                            <!-- Lead Capture Form -->
                            <div x-show="showForm && !submitted" x-cloak class="space-y-4">
                                <h4 class="text-lg font-bold text-slate-900">Request Information</h4>
                                <p class="text-sm text-slate-600">Fill out the form below and a specialist will contact you.</p>
                                
                                <div>
                                    <label class="block text-sm font-medium text-slate-700 mb-1">Full Name *</label>
                                    <input type="text" x-model="formData.name" required
                                           class="w-full px-4 py-2 border border-slate-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
                                           placeholder="John Smith">
                                </div>
                                
                                <div>
                                    <label class="block text-sm font-medium text-slate-700 mb-1">Email Address *</label>
                                    <input type="email" x-model="formData.email" required
                                           class="w-full px-4 py-2 border border-slate-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
                                           placeholder="john@example.com">
                                </div>
                                
                                <div>
                                    <label class="block text-sm font-medium text-slate-700 mb-1">Phone Number *</label>
                                    <input type="tel" x-model="formData.phone" required
                                           class="w-full px-4 py-2 border border-slate-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
                                           placeholder="(555) 123-4567">
                                </div>
                                
                                <div>
                                    <label class="block text-sm font-medium text-slate-700 mb-1">Condition / Area of Pain *</label>
                                    <select x-model="formData.condition" required
                                            class="w-full px-4 py-2 border border-slate-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500">
                                        <option value="">Select your condition</option>
                                        <option value="Knee Pain / Osteoarthritis">Knee Pain / Osteoarthritis</option>
                                        <option value="Back / Spine / Disc Pain">Back / Spine / Disc Pain</option>
                                        <option value="Shoulder Pain / Rotator Cuff">Shoulder Pain / Rotator Cuff</option>
                                        <option value="Hip Pain / Osteoarthritis">Hip Pain / Osteoarthritis</option>
                                        <option value="Elbow / Tennis Elbow">Elbow / Tennis Elbow</option>
                                        <option value="Ankle / Foot Pain">Ankle / Foot Pain</option>
                                        <option value="Wrist / Hand Pain">Wrist / Hand Pain</option>
                                        <option value="Sports Injury">Sports Injury</option>
                                        <option value="Other">Other</option>
                                    </select>
                                </div>
                                
                                <div>
                                    <label class="block text-sm font-medium text-slate-700 mb-1">Additional Information</label>
                                    <textarea x-model="formData.message" rows="3"
                                              class="w-full px-4 py-2 border border-slate-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
                                              placeholder="Tell us more about your condition..."></textarea>
                                </div>
                                
                                <button @click="submitForm()" 
                                        :disabled="!formData.name || !formData.email || !formData.phone || !formData.condition"
                                        class="w-full bg-green-600 text-white text-center px-6 py-3 rounded-lg hover:bg-green-700 transition font-medium disabled:bg-slate-400 disabled:cursor-not-allowed">
                                    Submit Request
                                </button>
                                
                                <button @click="showForm = false" 
                                        class="w-full text-slate-600 text-center px-6 py-2 hover:text-slate-800 transition text-sm">
                                    Cancel
                                </button>
                                
                                <p class="text-xs text-slate-500 text-center">
                                    By submitting, you agree to be contacted about stem cell treatment options.
                                </p>
                            </div>
                            
                            <!-- Success Message -->
                            <div x-show="submitted" x-cloak class="text-center py-4">
                                <div class="w-16 h-16 bg-green-100 rounded-full flex items-center justify-center mx-auto mb-4">
                                    <svg class="w-8 h-8 text-green-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"></path>
                                    </svg>
                                </div>
                                <h4 class="text-lg font-bold text-slate-900 mb-2">Request Submitted!</h4>
                                <p class="text-sm text-slate-600">A specialist will contact you within 24-48 hours to discuss your treatment options.</p>
                            </div>
                        </div>'''

# Pattern to find the Call Now button/link
CALL_NOW_PATTERN = r'<a href="tel:[^"]*"\s*\n?\s*class="[^"]*"\s*>\s*Call Now\s*</a>'

def get_clinic_info_from_html(content):
    """Extract clinic info from the HTML content"""
    # Extract clinic name from title
    title_match = re.search(r'<title>([^<]+)', content)
    clinic_name = "Clinic"
    if title_match:
        clinic_name = title_match.group(1).split(' - ')[0].strip()
    
    # Extract phone number
    phone_match = re.search(r'<p class="text-blue-600 font-medium">([^<]+)</p>', content)
    clinic_phone = ""
    if phone_match:
        clinic_phone = phone_match.group(1).strip()
    
    # Extract city from breadcrumb
    city_match = re.search(r'/locations/[^/]+/([^/]+)/', content)
    city = ""
    if city_match:
        city = city_match.group(1).replace('-', ' ').title()
    
    # Extract state from breadcrumb
    state_match = re.search(r'/locations/([^/]+)/', content)
    state = ""
    if state_match:
        state = state_match.group(1).replace('-', ' ').title()
    
    return clinic_name, clinic_phone, city, state

def update_clinic_page(file_path):
    """Update a single clinic page with the lead form"""
    with open(file_path, 'r') as f:
        content = f.read()
    
    # Check if already has the form
    if 'Get Free Consultation' in content:
        print(f"Skipped (already has form): {file_path}")
        return False
    
    # Check if has Call Now button
    if not re.search(CALL_NOW_PATTERN, content, re.IGNORECASE | re.MULTILINE):
        print(f"Skipped (no Call Now button): {file_path}")
        return False
    
    # Get clinic info
    clinic_name, clinic_phone, city, state = get_clinic_info_from_html(content)
    
    # Create customized form
    form_html = LEAD_FORM_HTML.replace('{clinic_name}', clinic_name.replace("'", "\\'"))
    form_html = form_html.replace('{clinic_phone}', clinic_phone)
    form_html = form_html.replace('{city}', city)
    form_html = form_html.replace('{state}', state)
    
    # Replace Call Now button with form
    new_content = re.sub(CALL_NOW_PATTERN, form_html, content, flags=re.IGNORECASE | re.MULTILINE)
    
    # Add x-cloak style if not present
    if '[x-cloak]' not in new_content:
        new_content = new_content.replace('</style>', '        [x-cloak] { display: none !important; }\n    </style>')
    
    with open(file_path, 'w') as f:
        f.write(new_content)
    
    print(f"Updated: {file_path}")
    return True

def main():
    print("=" * 60)
    print("ADDING LEAD CAPTURE FORMS TO CLINIC PAGES")
    print("=" * 60)
    
    locations_dir = Path('/home/ubuntu/stem-cells/locations')
    updated_count = 0
    
    # Find all clinic HTML files (not index.html)
    for html_file in locations_dir.rglob('*.html'):
        if html_file.name != 'index.html':
            if update_clinic_page(html_file):
                updated_count += 1
    
    print("\n" + "=" * 60)
    print(f"COMPLETE: Updated {updated_count} clinic pages with lead forms")
    print("=" * 60)

if __name__ == '__main__':
    main()
