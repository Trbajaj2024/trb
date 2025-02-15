class Carousel {
    constructor(element) {
        this.carousel = element;
        this.slides = Array.from(this.carousel.querySelectorAll('.carousel-slide'));
        this.prevBtn = this.carousel.querySelector('[data-carousel-prev]');
        this.nextBtn = this.carousel.querySelector('[data-carousel-next]');
        this.currentIndex = 0;
        this.autoplayInterval = null;
        
        this.init();
    }
    
    init() {
        // Add event listeners
        this.prevBtn.addEventListener('click', () => this.prev());
        this.nextBtn.addEventListener('click', () => this.next());
        
        // Start autoplay
        this.startAutoplay();
        
        // Pause autoplay on hover
        this.carousel.addEventListener('mouseenter', () => this.stopAutoplay());
        this.carousel.addEventListener('mouseleave', () => this.startAutoplay());
        
        // Add keyboard navigation
        this.carousel.addEventListener('keydown', (e) => {
            if (e.key === 'ArrowLeft') this.prev();
            if (e.key === 'ArrowRight') this.next();
        });
    }
    
    showSlide(index) {
        this.slides.forEach(slide => {
            slide.classList.remove('active');
            slide.setAttribute('aria-hidden', 'true');
        });
        
        this.slides[index].classList.add('active');
        this.slides[index].setAttribute('aria-hidden', 'false');
        this.currentIndex = index;
    }
    
    next() {
        const nextIndex = (this.currentIndex + 1) % this.slides.length;
        this.showSlide(nextIndex);
    }
    
    prev() {
        const prevIndex = (this.currentIndex - 1 + this.slides.length) % this.slides.length;
        this.showSlide(prevIndex);
    }
    
    startAutoplay() {
        this.autoplayInterval = setInterval(() => this.next(), 5000);
    }
    
    stopAutoplay() {
        clearInterval(this.autoplayInterval);
    }
}

// Initialize all carousels
document.addEventListener('DOMContentLoaded', () => {
    document.querySelectorAll('[data-carousel]').forEach(carousel => {
        new Carousel(carousel);
    });
}); 