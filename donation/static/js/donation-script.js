// Donation Platform JavaScript

document.addEventListener('DOMContentLoaded', function() {
    // Initialize all components
    initializeAmountButtons();
    initializeProgressBars();
    initializeDonationForm();
    initializeNewsletterForm();
    initializeAnimations();
});

// Amount Button Selection
function initializeAmountButtons() {
    const amountButtons = document.querySelectorAll('.amount-btn');
    const customAmountInput = document.getElementById('customAmount');
    
    if (amountButtons.length > 0 && customAmountInput) {
        amountButtons.forEach(btn => {
            btn.addEventListener('click', function() {
                // Remove active class from all buttons
                amountButtons.forEach(b => b.classList.remove('active'));
                
                // Add active class to clicked button
                this.classList.add('active');
                
                // Set the amount in the input field
                const amount = this.dataset.amount;
                customAmountInput.value = amount;
                
                // Trigger input event for validation
                customAmountInput.dispatchEvent(new Event('input'));
            });
        });
        
        // Handle custom amount input
        customAmountInput.addEventListener('input', function() {
            // Remove active class from all buttons when typing custom amount
            amountButtons.forEach(b => b.classList.remove('active'));
            
            // Validate amount
            validateAmount(this.value);
        });
    }
}

// Progress Bar Animations
function initializeProgressBars() {
    const progressBars = document.querySelectorAll('.progress-fill, .progress-bar');
    
    // Animate progress bars when they come into view
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                const progressBar = entry.target;
                const width = progressBar.style.width || progressBar.dataset.width;
                
                if (width) {
                    progressBar.style.width = '0%';
                    setTimeout(() => {
                        progressBar.style.transition = 'width 1.5s ease-out';
                        progressBar.style.width = width;
                    }, 100);
                }
                
                observer.unobserve(progressBar);
            }
        });
    }, { threshold: 0.5 });
    
    progressBars.forEach(bar => observer.observe(bar));
}

// Donation Form Handling
function initializeDonationForm() {
    const donationForm = document.getElementById('donationForm');
    
    if (donationForm) {
        donationForm.addEventListener('submit', function(e) {
            const amount = parseFloat(document.getElementById('customAmount').value);
            
            // Validate amount
            if (!amount || amount < 1) {
                e.preventDefault();
                showAlert('Please enter a valid donation amount of at least $1.', 'danger');
                return false;
            }
            
            // Show loading state
            const submitBtn = this.querySelector('button[type="submit"]');
            const originalText = submitBtn.innerHTML;
            submitBtn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Processing...';
            submitBtn.disabled = true;
            
            // Re-enable after 3 seconds if form doesn't submit
            setTimeout(() => {
                if (submitBtn.disabled) {
                    submitBtn.innerHTML = originalText;
                    submitBtn.disabled = false;
                }
            }, 3000);
        });
    }
}

// Newsletter Form Handling
function initializeNewsletterForm() {
    const newsletterForms = document.querySelectorAll('#newsletter-form, .newsletter-form');
    
    newsletterForms.forEach(form => {
        form.addEventListener('submit', function(e) {
            e.preventDefault();
            
            const submitBtn = this.querySelector('.newsletter-btn, button[type="submit"]');
            const emailInput = this.querySelector('input[type="email"]');
            const messageDiv = document.getElementById('newsletter-message') || 
                              this.querySelector('.newsletter-message') ||
                              createMessageDiv(this);
            
            if (!emailInput.value.trim()) {
                showMessage(messageDiv, 'Please enter a valid email address.', 'danger');
                return;
            }
            
            // Show loading state
            const originalText = submitBtn.textContent;
            submitBtn.textContent = 'Subscribing...';
            submitBtn.disabled = true;
            
            // Prepare form data
            const formData = new FormData(this);
            
            // Submit form
            fetch(this.action || '/newsletter/subscribe', {
                method: 'POST',
                body: formData
            })
            .then(response => response.json())
            .then(data => {
                const alertType = data.status === 'error' ? 'danger' : 
                                data.status === 'info' ? 'info' : 'success';
                
                showMessage(messageDiv, data.message, alertType);
                
                if (data.status === 'success') {
                    this.reset();
                }
            })
            .catch(error => {
                console.error('Error:', error);
                showMessage(messageDiv, 'An error occurred. Please try again.', 'danger');
            })
            .finally(() => {
                submitBtn.textContent = originalText;
                submitBtn.disabled = false;
                
                // Auto-hide message after 5 seconds
                setTimeout(() => {
                    hideMessage(messageDiv);
                }, 5000);
            });
        });
    });
}

// Animation Initialization
function initializeAnimations() {
    // Fade in cards when they come into view
    const cards = document.querySelectorAll('.project-card, .card, .donation-item');
    
    const cardObserver = new IntersectionObserver((entries) => {
        entries.forEach((entry, index) => {
            if (entry.isIntersecting) {
                setTimeout(() => {
                    entry.target.classList.add('fade-in');
                }, index * 100); // Stagger animation
                
                cardObserver.unobserve(entry.target);
            }
        });
    }, { threshold: 0.1 });
    
    cards.forEach(card => cardObserver.observe(card));
    
    // Smooth scroll for anchor links
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function(e) {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                target.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            }
        });
    });
}

// Utility Functions
function validateAmount(amount) {
    const numAmount = parseFloat(amount);
    const customInput = document.getElementById('customAmount');
    
    if (customInput) {
        if (!amount || isNaN(numAmount) || numAmount < 1) {
            customInput.classList.add('is-invalid');
            return false;
        } else {
            customInput.classList.remove('is-invalid');
            return true;
        }
    }
    return true;
}

function showAlert(message, type = 'info') {
    const alertDiv = document.createElement('div');
    alertDiv.className = `alert alert-${type} alert-dismissible fade show`;
    alertDiv.innerHTML = `
        ${message}
        <button type="button" class="btn-close" onclick="this.parentElement.remove()"></button>
    `;
    
    // Insert at top of main content
    const main = document.querySelector('main') || document.body;
    main.insertBefore(alertDiv, main.firstChild);
    
    // Auto-remove after 5 seconds
    setTimeout(() => {
        if (alertDiv.parentNode) {
            alertDiv.remove();
        }
    }, 5000);
}

function createMessageDiv(form) {
    const messageDiv = document.createElement('div');
    messageDiv.className = 'newsletter-message';
    messageDiv.style.marginTop = '10px';
    messageDiv.style.display = 'none';
    form.appendChild(messageDiv);
    return messageDiv;
}

function showMessage(messageDiv, message, type) {
    messageDiv.className = `newsletter-message alert alert-${type}`;
    messageDiv.textContent = message;
    messageDiv.style.display = 'block';
}

function hideMessage(messageDiv) {
    if (messageDiv) {
        messageDiv.style.opacity = '0';
        setTimeout(() => {
            messageDiv.style.display = 'none';
            messageDiv.style.opacity = '1';
        }, 300);
    }
}

// Format currency
function formatCurrency(amount) {
    return new Intl.NumberFormat('en-US', {
        style: 'currency',
        currency: 'USD'
    }).format(amount);
}

// Update progress display
function updateProgress(current, goal) {
    const percentage = Math.min(100, (current / goal) * 100);
    return {
        percentage: percentage.toFixed(1),
        current: formatCurrency(current),
        goal: formatCurrency(goal)
    };
}

// Copy to clipboard functionality
function copyToClipboard(text) {
    navigator.clipboard.writeText(text).then(() => {
        showAlert('Copied to clipboard!', 'success');
    }).catch(() => {
        showAlert('Failed to copy to clipboard.', 'danger');
    });
}

// Share functionality
function shareProject(title, url) {
    if (navigator.share) {
        navigator.share({
            title: `Support: ${title}`,
            url: url
        }).catch(console.error);
    } else {
        copyToClipboard(url);
    }
}

// Export for global use
window.DonationPlatform = {
    validateAmount,
    showAlert,
    formatCurrency,
    updateProgress,
    copyToClipboard,
    shareProject
};
