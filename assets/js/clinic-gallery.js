/**
 * Clinic Image Gallery Component
 * Dynamically loads and displays multiple clinic images with lightbox support
 */

function clinicGallery(clinicSlug, maxImages = 6) {
    return {
        clinicSlug: clinicSlug,
        images: [],
        currentIndex: 0,
        lightboxOpen: false,
        loading: true,
        baseUrl: 'https://cfls.b-cdn.net/stem-cell-clinics',

        async init() {
            await this.loadImages();
            this.loading = false;
        },

        async loadImages() {
            // Try to load primary image (check .jpg, .webp, and .png)
            const formats = ['jpg', 'webp', 'png'];
            let primaryUrl = null;

            for (const fmt of formats) {
                const url = `${this.baseUrl}/${this.clinicSlug}/primary.${fmt}`;
                if (await this.imageExists(url)) {
                    primaryUrl = url;
                    break;
                }
            }

            if (primaryUrl) {
                this.images.push({
                    url: primaryUrl,
                    alt: 'Clinic primary image'
                });
            }

            // Try to load additional numbered images (2.jpg/webp/png, 3.jpg/webp/png, etc.)
            for (let i = 2; i <= maxImages; i++) {
                let url = null;

                for (const fmt of formats) {
                    const testUrl = `${this.baseUrl}/${this.clinicSlug}/${i}.${fmt}`;
                    if (await this.imageExists(testUrl)) {
                        url = testUrl;
                        break;
                    }
                }

                if (url) {
                    this.images.push({
                        url: url,
                        alt: `Clinic image ${i}`
                    });
                } else {
                    // Stop checking if we hit a missing image
                    break;
                }
            }
        },

        imageExists(url) {
            return new Promise((resolve) => {
                const img = new Image();
                img.onload = () => resolve(true);
                img.onerror = () => resolve(false);
                img.src = url;
            });
        },

        get hasMultipleImages() {
            return this.images.length > 1;
        },

        get currentImage() {
            return this.images[this.currentIndex] || null;
        },

        openLightbox(index) {
            this.currentIndex = index;
            this.lightboxOpen = true;
            document.body.style.overflow = 'hidden';
        },

        closeLightbox() {
            this.lightboxOpen = false;
            document.body.style.overflow = '';
        },

        nextImage() {
            this.currentIndex = (this.currentIndex + 1) % this.images.length;
        },

        prevImage() {
            this.currentIndex = (this.currentIndex - 1 + this.images.length) % this.images.length;
        },

        handleKeydown(e) {
            if (!this.lightboxOpen) return;
            if (e.key === 'Escape') this.closeLightbox();
            if (e.key === 'ArrowRight') this.nextImage();
            if (e.key === 'ArrowLeft') this.prevImage();
        }
    };
}
