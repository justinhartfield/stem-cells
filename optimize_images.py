#!/usr/bin/env python3
"""
Image Optimization Script for Stem Cells Website
- Compresses JPG images
- Converts to WebP format
- Creates responsive sizes (small, medium, large)
- Optimizes for page speed
"""

import os
import subprocess
from PIL import Image
from pathlib import Path
import shutil

# Configuration
QUALITY_JPG = 75  # JPEG quality (0-100)
QUALITY_WEBP = 80  # WebP quality (0-100)

# Responsive sizes for different viewports
SIZES = {
    'small': 480,   # Mobile
    'medium': 768,  # Tablet
    'large': 1200,  # Desktop
    'xlarge': 1920  # Full HD
}

def get_image_files(directory):
    """Get all image files in directory"""
    extensions = ['.jpg', '.jpeg', '.png']
    files = []
    for ext in extensions:
        files.extend(Path(directory).glob(f'*{ext}'))
        files.extend(Path(directory).glob(f'*{ext.upper()}'))
    return files

def optimize_jpg(input_path, output_path, quality=75, max_width=None):
    """Optimize JPG image"""
    img = Image.open(input_path)
    
    # Convert to RGB if necessary
    if img.mode in ('RGBA', 'P'):
        img = img.convert('RGB')
    
    # Resize if max_width specified
    if max_width and img.width > max_width:
        ratio = max_width / img.width
        new_height = int(img.height * ratio)
        img = img.resize((max_width, new_height), Image.LANCZOS)
    
    # Save with optimization
    img.save(output_path, 'JPEG', quality=quality, optimize=True, progressive=True)
    return os.path.getsize(output_path)

def convert_to_webp(input_path, output_path, quality=80, max_width=None):
    """Convert image to WebP format"""
    img = Image.open(input_path)
    
    # Convert to RGB if necessary (WebP doesn't support all modes)
    if img.mode in ('RGBA', 'P'):
        img = img.convert('RGBA')
    elif img.mode != 'RGB':
        img = img.convert('RGB')
    
    # Resize if max_width specified
    if max_width and img.width > max_width:
        ratio = max_width / img.width
        new_height = int(img.height * ratio)
        img = img.resize((max_width, new_height), Image.LANCZOS)
    
    # Save as WebP
    img.save(output_path, 'WEBP', quality=quality, method=6)
    return os.path.getsize(output_path)

def create_responsive_images(input_path, output_dir, base_name):
    """Create responsive image sizes in both JPG and WebP"""
    results = {}
    
    for size_name, max_width in SIZES.items():
        # Create JPG version
        jpg_output = os.path.join(output_dir, f"{base_name}-{size_name}.jpg")
        jpg_size = optimize_jpg(input_path, jpg_output, QUALITY_JPG, max_width)
        results[f'{size_name}_jpg'] = jpg_size
        
        # Create WebP version
        webp_output = os.path.join(output_dir, f"{base_name}-{size_name}.webp")
        webp_size = convert_to_webp(input_path, webp_output, QUALITY_WEBP, max_width)
        results[f'{size_name}_webp'] = webp_size
    
    return results

def process_directory(input_dir, output_dir):
    """Process all images in a directory"""
    os.makedirs(output_dir, exist_ok=True)
    
    images = get_image_files(input_dir)
    total_original = 0
    total_optimized = 0
    
    print(f"\nProcessing {len(images)} images from {input_dir}")
    print("-" * 60)
    
    for img_path in sorted(images):
        original_size = os.path.getsize(img_path)
        total_original += original_size
        
        base_name = img_path.stem
        print(f"Processing: {base_name}")
        
        # Create responsive versions
        results = create_responsive_images(str(img_path), output_dir, base_name)
        
        # Calculate optimized size (using medium WebP as primary)
        optimized_size = results.get('medium_webp', 0)
        total_optimized += optimized_size
        
        # Print stats
        savings = ((original_size - optimized_size) / original_size) * 100
        print(f"  Original: {original_size/1024/1024:.2f}MB -> Medium WebP: {optimized_size/1024:.0f}KB ({savings:.1f}% smaller)")
    
    return total_original, total_optimized

def main():
    base_dir = '/home/ubuntu/stem-cells/assets/images'
    
    # Create optimized directories
    states_input = os.path.join(base_dir, 'states')
    states_output = os.path.join(base_dir, 'states-optimized')
    
    cities_input = os.path.join(base_dir, 'cities')
    cities_output = os.path.join(base_dir, 'cities-optimized')
    
    print("=" * 60)
    print("IMAGE OPTIMIZATION FOR STEM CELLS WEBSITE")
    print("=" * 60)
    
    # Process states
    states_orig, states_opt = process_directory(states_input, states_output)
    
    # Process cities
    cities_orig, cities_opt = process_directory(cities_input, cities_output)
    
    # Summary
    total_orig = states_orig + cities_orig
    total_opt = states_opt + cities_opt
    
    print("\n" + "=" * 60)
    print("OPTIMIZATION SUMMARY")
    print("=" * 60)
    print(f"States - Original: {states_orig/1024/1024:.1f}MB, Optimized: {states_opt/1024/1024:.1f}MB")
    print(f"Cities - Original: {cities_orig/1024/1024:.1f}MB, Optimized: {cities_opt/1024/1024:.1f}MB")
    print(f"TOTAL  - Original: {total_orig/1024/1024:.1f}MB, Optimized: {total_opt/1024/1024:.1f}MB")
    print(f"SAVINGS: {((total_orig - total_opt) / total_orig) * 100:.1f}%")
    print("=" * 60)

if __name__ == '__main__':
    main()
