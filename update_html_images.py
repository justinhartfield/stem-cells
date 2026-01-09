#!/usr/bin/env python3
"""
Update HTML templates to use optimized responsive images with:
- WebP format with JPG fallback using <picture> element
- Responsive srcset for different viewport sizes
- Lazy loading for images below the fold
- Proper width/height attributes to prevent CLS
"""

import os
import re
from pathlib import Path

def get_responsive_picture_tag(image_type, image_name, alt_text, css_class="", is_hero=False):
    """Generate a responsive picture tag with WebP and fallback"""
    
    base_path = f"/assets/images/{image_type}-optimized"
    
    # Determine loading strategy
    loading = "eager" if is_hero else "lazy"
    decoding = "sync" if is_hero else "async"
    fetchpriority = 'fetchpriority="high"' if is_hero else ""
    
    picture_html = f'''<picture>
    <source 
        type="image/webp"
        srcset="{base_path}/{image_name}-small.webp 480w,
                {base_path}/{image_name}-medium.webp 768w,
                {base_path}/{image_name}-large.webp 1200w,
                {base_path}/{image_name}-xlarge.webp 1920w"
        sizes="100vw">
    <img 
        src="{base_path}/{image_name}-large.jpg"
        srcset="{base_path}/{image_name}-small.jpg 480w,
                {base_path}/{image_name}-medium.jpg 768w,
                {base_path}/{image_name}-large.jpg 1200w,
                {base_path}/{image_name}-xlarge.jpg 1920w"
        sizes="100vw"
        alt="{alt_text}"
        class="{css_class}"
        loading="{loading}"
        decoding="{decoding}"
        {fetchpriority}
        width="1200"
        height="800">
</picture>'''
    
    return picture_html

def update_locations_index():
    """Update the main locations index page"""
    file_path = '/home/ubuntu/stem-cells/locations/index.html'
    
    with open(file_path, 'r') as f:
        content = f.read()
    
    # Replace state image references with responsive versions
    # Pattern: <img src="/assets/images/states/california.jpg"
    pattern = r'<img\s+src="/assets/images/states/([^"]+)\.jpg"([^>]*)>'
    
    def replace_state_img(match):
        state_name = match.group(1)
        attrs = match.group(2)
        alt_match = re.search(r'alt="([^"]*)"', attrs)
        alt_text = alt_match.group(1) if alt_match else f"{state_name.replace('-', ' ').title()} stem cell clinics"
        class_match = re.search(r'class="([^"]*)"', attrs)
        css_class = class_match.group(1) if class_match else "w-full h-48 object-cover"
        
        return f'''<picture>
                <source type="image/webp" srcset="/assets/images/states-optimized/{state_name}-small.webp 480w, /assets/images/states-optimized/{state_name}-medium.webp 768w, /assets/images/states-optimized/{state_name}-large.webp 1200w" sizes="(max-width: 640px) 100vw, (max-width: 1024px) 50vw, 25vw">
                <img src="/assets/images/states-optimized/{state_name}-medium.jpg" srcset="/assets/images/states-optimized/{state_name}-small.jpg 480w, /assets/images/states-optimized/{state_name}-medium.jpg 768w, /assets/images/states-optimized/{state_name}-large.jpg 1200w" sizes="(max-width: 640px) 100vw, (max-width: 1024px) 50vw, 25vw" alt="{alt_text}" class="{css_class}" loading="lazy" decoding="async" width="768" height="512">
            </picture>'''
    
    content = re.sub(pattern, replace_state_img, content)
    
    with open(file_path, 'w') as f:
        f.write(content)
    
    print(f"Updated: {file_path}")

def update_state_pages():
    """Update all state directory pages"""
    states_dir = '/home/ubuntu/stem-cells/locations'
    
    for state_dir in Path(states_dir).iterdir():
        if state_dir.is_dir() and state_dir.name != 'index.html':
            index_file = state_dir / 'index.html'
            if index_file.exists():
                with open(index_file, 'r') as f:
                    content = f.read()
                
                state_name = state_dir.name
                
                # Update hero background image to use optimized version
                # Pattern for background-image in style
                bg_pattern = r"background-image:\s*url\('/assets/images/states/([^']+)\.jpg'\)"
                content = re.sub(
                    bg_pattern,
                    f"background-image: url('/assets/images/states-optimized/\\1-large.webp')",
                    content
                )
                
                # Update city images
                city_pattern = r'<img\s+src="/assets/images/cities/([^"]+)\.jpg"([^>]*)>'
                
                def replace_city_img(match):
                    city_name = match.group(1)
                    attrs = match.group(2)
                    alt_match = re.search(r'alt="([^"]*)"', attrs)
                    alt_text = alt_match.group(1) if alt_match else f"{city_name.replace('-', ' ').title()} stem cell clinics"
                    class_match = re.search(r'class="([^"]*)"', attrs)
                    css_class = class_match.group(1) if class_match else "w-full h-48 object-cover"
                    
                    return f'''<picture>
                <source type="image/webp" srcset="/assets/images/cities-optimized/{city_name}-small.webp 480w, /assets/images/cities-optimized/{city_name}-medium.webp 768w, /assets/images/cities-optimized/{city_name}-large.webp 1200w" sizes="(max-width: 640px) 100vw, (max-width: 1024px) 50vw, 33vw">
                <img src="/assets/images/cities-optimized/{city_name}-medium.jpg" srcset="/assets/images/cities-optimized/{city_name}-small.jpg 480w, /assets/images/cities-optimized/{city_name}-medium.jpg 768w, /assets/images/cities-optimized/{city_name}-large.jpg 1200w" sizes="(max-width: 640px) 100vw, (max-width: 1024px) 50vw, 33vw" alt="{alt_text}" class="{css_class}" loading="lazy" decoding="async" width="768" height="512">
            </picture>'''
                
                content = re.sub(city_pattern, replace_city_img, content)
                
                with open(index_file, 'w') as f:
                    f.write(content)
                
                print(f"Updated: {index_file}")

def update_city_pages():
    """Update all city directory pages"""
    states_dir = '/home/ubuntu/stem-cells/locations'
    
    for state_dir in Path(states_dir).iterdir():
        if state_dir.is_dir():
            for city_dir in state_dir.iterdir():
                if city_dir.is_dir():
                    index_file = city_dir / 'index.html'
                    if index_file.exists():
                        with open(index_file, 'r') as f:
                            content = f.read()
                        
                        city_name = city_dir.name
                        
                        # Update hero background image
                        bg_pattern = r"background-image:\s*url\('/assets/images/cities/([^']+)\.jpg'\)"
                        content = re.sub(
                            bg_pattern,
                            f"background-image: url('/assets/images/cities-optimized/\\1-large.webp')",
                            content
                        )
                        
                        with open(index_file, 'w') as f:
                            f.write(content)
                        
                        print(f"Updated: {index_file}")

def update_clinic_pages():
    """Update all clinic detail pages"""
    states_dir = '/home/ubuntu/stem-cells/locations'
    
    for state_dir in Path(states_dir).iterdir():
        if state_dir.is_dir():
            for city_dir in state_dir.iterdir():
                if city_dir.is_dir():
                    for clinic_file in city_dir.glob('*.html'):
                        if clinic_file.name != 'index.html':
                            with open(clinic_file, 'r') as f:
                                content = f.read()
                            
                            city_name = city_dir.name
                            
                            # Update hero background image
                            bg_pattern = r"background-image:\s*url\('/assets/images/cities/([^']+)\.jpg'\)"
                            content = re.sub(
                                bg_pattern,
                                f"background-image: url('/assets/images/cities-optimized/\\1-large.webp')",
                                content
                            )
                            
                            with open(clinic_file, 'w') as f:
                                f.write(content)
                            
                            print(f"Updated: {clinic_file}")

def add_preload_hints():
    """Add preload hints for critical images to all HTML files"""
    preload_css = '''
    <!-- Preload critical CSS -->
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    '''
    
    # This would be added to each HTML file's head section
    # For now, we'll add it to the main templates

def main():
    print("=" * 60)
    print("UPDATING HTML TEMPLATES WITH OPTIMIZED IMAGES")
    print("=" * 60)
    
    print("\n1. Updating locations index page...")
    update_locations_index()
    
    print("\n2. Updating state pages...")
    update_state_pages()
    
    print("\n3. Updating city pages...")
    update_city_pages()
    
    print("\n4. Updating clinic pages...")
    update_clinic_pages()
    
    print("\n" + "=" * 60)
    print("HTML TEMPLATE UPDATE COMPLETE")
    print("=" * 60)

if __name__ == '__main__':
    main()
