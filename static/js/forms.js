class AjaxForm {
    constructor(form) {
        this.form = form;
        this.submitBtn = form.querySelector('button[type="submit"]');
        this.init();
    }
    
    init() {
        this.form.addEventListener('submit', (e) => this.handleSubmit(e));
    }
    
    async handleSubmit(e) {
        e.preventDefault();
        
        // Show loading state
        this.submitBtn.disabled = true;
        this.submitBtn.innerHTML = 'Submitting...';
        
        try {
            const formData = new FormData(this.form);
            const response = await fetch(this.form.action, {
                method: 'POST',
                body: formData,
                headers: {
                    'X-CSRFToken': formData.get('csrfmiddlewaretoken')
                }
            });
            
            const data = await response.json();
            
            if (response.ok) {
                // Show success message
                this.showMessage('success', data.message);
                this.form.reset();
            } else {
                // Show error message
                this.showMessage('error', data.message || 'An error occurred');
            }
        } catch (error) {
            this.showMessage('error', 'An error occurred');
        } finally {
            // Reset button state
            this.submitBtn.disabled = false;
            this.submitBtn.innerHTML = 'Submit';
        }
    }
    
    showMessage(type, text) {
        const message = document.createElement('div');
        message.className = `alert alert-${type}`;
        message.textContent = text;
        
        this.form.insertAdjacentElement('beforebegin', message);
        
        // Remove message after 5 seconds
        setTimeout(() => message.remove(), 5000);
    }
}

// Initialize all AJAX forms
document.addEventListener('DOMContentLoaded', () => {
    document.querySelectorAll('[data-ajax-form]').forEach(form => {
        new AjaxForm(form);
    });
}); 