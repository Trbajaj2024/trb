// Accessibility Enhancements
document.addEventListener('DOMContentLoaded', function() {
    // Add aria-current to active navigation items
    const currentPath = window.location.pathname;
    document.querySelectorAll('nav a').forEach(link => {
        if (link.getAttribute('href') === currentPath) {
            link.setAttribute('aria-current', 'page');
        }
    });

    // Ensure all images have alt text
    document.querySelectorAll('img').forEach(img => {
        if (!img.hasAttribute('alt')) {
            console.warn('Missing alt text:', img);
            img.alt = ''; // Empty alt for decorative images
        }
    });

    // Add aria-labels to form controls
    document.querySelectorAll('input, select, textarea').forEach(field => {
        const label = document.querySelector(`label[for="${field.id}"]`);
        if (!label) {
            console.warn('Missing label for:', field);
        }
    });

    // Enhance keyboard navigation
    document.addEventListener('keydown', function(e) {
        if (e.key === 'Tab') {
            document.body.classList.add('keyboard-nav');
        }
    });

    document.addEventListener('mousedown', function() {
        document.body.classList.remove('keyboard-nav');
    });
});

// Focus trap for modals
function trapFocus(element) {
    const focusableElements = element.querySelectorAll(
        'a[href], button, textarea, input[type="text"], input[type="radio"], input[type="checkbox"], select'
    );
    const firstFocusableElement = focusableElements[0];
    const lastFocusableElement = focusableElements[focusableElements.length - 1];

    element.addEventListener('keydown', function(e) {
        if (e.key === 'Tab') {
            if (e.shiftKey) {
                if (document.activeElement === firstFocusableElement) {
                    lastFocusableElement.focus();
                    e.preventDefault();
                }
            } else {
                if (document.activeElement === lastFocusableElement) {
                    firstFocusableElement.focus();
                    e.preventDefault();
                }
            }
        }
    });
} 