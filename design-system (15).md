This Design System documentation is reverse-engineered from the provided HTML and configuration for **OrthoFinder**.

---

# Design System: OrthoFinder

## 1. Core Principles
*   **Modern Medical Trust**: The aesthetic combines a clean, clinical feel with modern UI trends like glassmorphism to establish authority and accessibility in the healthcare space.
*   **Clarity & Transparency**: High-contrast typography and specific "price" accents emphasize the application's goal: making therapy costs and clinic data easy to digest.
*   **Soft Professionalism**: The use of radial gradients and rounded corners (implied by Tailwind defaults) moves away from "stark" medical interfaces toward a more user-friendly, concierge-style experience.

## 2. Color Palette

### Brand Colors (Primary)
The brand uses a sophisticated blue scale, conveying stability and medical professionalism.
*   **Brand 50**: `#f0f7ff` (Ultra-light background/hover)
*   **Brand 100**: `#e0effe` (Soft accents/rings)
*   **Brand 600**: `#2563eb` (Primary Action / Brand Hero)
*   **Brand 700**: `#1d4ed8` (Hover states / Emphasis)
*   **Brand 800/900**: `#1e40af` / `#1e3a8a` (Deep text / Headers)

### Functional Colors (Accents)
Used specifically for financial data and price-related callouts.
*   **Price Light**: `#0ea5e9` (Sky Blue)
*   **Price Dark**: `#0369a1` (Deep Sky)
*   **Price Gradient**: `linear-gradient(135deg, #0ea5e9 0%, #2563eb 100%)`

### Backgrounds & Surfaces
*   **Main Background**: Radial gradient from `#e0effe` (top right) to `#ffffff`.
*   **Glass Surface**: `rgba(255, 255, 255, 0.8)` with `12px` backdrop blur.
*   **Border**: `rgba(255, 255, 255, 0.3)` (Subtle white borders for glass effect).

## 3. Typography
*   **Primary Font**: `Manrope`, sans-serif.
*   **Characteristics**: A modern geometric sans-serif that balances functional legibility with a friendly, contemporary tone.
*   **Weights**: 
    *   `300` (Light) - Secondary labels.
    *   `400/500` (Regular/Medium) - Body text.
    *   `600/700/800` (Semi-Bold to Extra-Bold) - Headings and UI emphasis.

## 4. Spacing & Layout
*   **Grid/Flex**: Utilizes Tailwind’s standard spacing scale.
*   **Container**: Likely uses standard responsive containers with a focus on centered, readable widths.
*   **Visual Hierarchy**: Achieved through the `glass-panel` class, which creates a layered "Z-axis" effect over the `gradient-bg`.

## 5. Components

### Glass Panels
The primary container for content.
*   **Class**: `.glass-panel`
*   **Styles**: Semi-transparent white background, heavy backdrop blur, and a subtle internal border to simulate depth.

### Step Indicators
Used for multi-step forms or progress tracking.
*   **Active State**: `.step-active`
*   **Styles**: `border-brand-600`, `text-brand-700`, and a `ring-2 ring-brand-100` for a soft "glow" effect.

### Price Badges
High-visibility labels for cost information.
*   **Class**: `.price-badge`
*   **Styles**: Linear gradient from Sky Blue to Brand Blue. Designed to stand out against white or glass backgrounds.

## 6. Iconography
*   **Style**: While not explicitly linked in the snippet, the design language strongly suggests **Line Icons** (e.g., Lucide or Heroicons) with a stroke weight of `1.5px` or `2px` to match the clean lines of the Manrope typeface.

---

## Reference HTML

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>OrthoFinder | Stem Cell Therapy Costs & Clinic Directory</title>
    <!-- Google Fonts: Manrope -->
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Manrope:wght@300;400;500;600;700;800&display=swap" rel="stylesheet">
    
    <!-- Tailwind CSS -->
    <script src="https://cdn.tailwindcss.com"></script>
    
    <!-- Alpine.js -->
    <script defer src="https://unpkg.com/alpinejs@3.x.x/dist/cdn.min.js"></script>

    <script>
        tailwind.config = {
            theme: {
                extend: {
                    fontFamily: {
                        sans: ['Manrope', 'sans-serif'],
                    },
                    colors: {
                        brand: {
                            50: '#f0f7ff',
                            100: '#e0effe',
                            200: '#bae0fd',
                            600: '#2563eb',
                            700: '#1d4ed8',
                            800: '#1e40af',
                            900: '#1e3a8a',
                        },
                        price: {
                            light: '#0ea5e9',
                            dark: '#0369a1',
                        }
                    }
                }
            }
        }
    </script>

    <style>
        [x-cloak] { display: none !important; }
        
        .glass-panel {
            background: rgba(255, 255, 255, 0.8);
            backdrop-filter: blur(12px);
            border: 1px solid rgba(255, 255, 255, 0.3);
        }

        .gradient-bg {
            background: radial-gradient(circle at top right, #e0effe 0%, #f8fafc 40%, #ffffff 100%);
        }

        .step-active {
            @apply border-brand-600 text-brand-700 ring-2 ring-brand-100;
        }

        .price-badge {
            background: linear-gradient(135deg, #0ea5e9 0%, #2563eb 100%);
        }
    </style>
</head>
```