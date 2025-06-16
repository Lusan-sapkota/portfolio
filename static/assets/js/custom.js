$(document).ready(function(){
    "use strict";

    // Initialize all components
    initializeDarkMode();
    initializeScrollEffects();
    initializeSmoothScrolling();
    initializeProgressBars();
    initializeOwlCarousel(); // FIXED: Separated owl carousel initialization
    initializeContactForm();
    initializeAnimations();

    // FIXED: Dark Mode Implementation
    function initializeDarkMode() {
        const currentTheme = localStorage.getItem('theme') || 
            (window.matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light');
        
        // Apply the theme immediately
        document.documentElement.setAttribute('data-theme', currentTheme);
        
        // Update toggle icons
        updateThemeIcons(currentTheme);
        
        // Set up theme toggle functionality
        $('#theme-toggle, #mobile-theme-toggle').on('click', function(e) {
            e.preventDefault();
            
            const current = document.documentElement.getAttribute('data-theme') || 'light';
            const newTheme = current === 'dark' ? 'light' : 'dark';
            
            // Add transition class
            document.body.classList.add('theme-transitioning');
            
            // Apply new theme
            document.documentElement.setAttribute('data-theme', newTheme);
            localStorage.setItem('theme', newTheme);
            
            // Update icons
            updateThemeIcons(newTheme);
            
            // Remove transition class
            setTimeout(() => {
                document.body.classList.remove('theme-transitioning');
            }, 300);
        });
    }

    function updateThemeIcons(theme) {
        const moonIcons = $('.fa-moon');
        const sunIcons = $('.fa-sun');
        
        if (theme === 'dark') {
            moonIcons.hide();
            sunIcons.show();
        } else {
            sunIcons.hide();
            moonIcons.show();
        }
    }

    // 1. Scroll To Top 
    function initializeScrollEffects() {
        $(window).on('scroll', function () {
            if ($(this).scrollTop() > 600) {
                $('.return-to-top').fadeIn();
            } else {
                $('.return-to-top').fadeOut();
            }
        });
        
        $('.return-to-top').on('click', function(){
            $('html, body').animate({
                scrollTop: 0
            }, 1500);
            return false;
        });
    }

    // 2. Smooth Scroll spy
    function initializeSmoothScrolling() {
        $('.smooth-menu a, a.smooth-menu, a[href^="#"]').on('click', function(event) {
            if(this.hash !== "") {
                event.preventDefault();
                
                const targetId = this.hash;
                const targetSection = $(targetId);
                if(!targetSection.length) return;
                
                const navbar = $('nav.navbar');
                const navbarHeight = navbar.length ? navbar.outerHeight() : 0;
                
                $('html, body').animate({
                    scrollTop: targetSection.offset().top - navbarHeight
                }, 800, 'easeInOutExpo');
                
                // Close mobile menu if open
                const navbarCollapse = $('.navbar-collapse');
                if (navbarCollapse.hasClass('show')) {
                    navbarCollapse.removeClass('show');
                }
                
                $('.navbar-nav li').removeClass('active');
                $(`a[href="${targetId}"]`).parent('li').addClass('active');
            }
        });
        
        // Better active section detection
        $(window).on('scroll', function() {
            const scrollPosition = $(this).scrollTop();
            const navbarHeight = $('nav.navbar').outerHeight();
            const buffer = 5;
            
            $('.navbar-nav li').removeClass('active');
            
            $('section').each(function() {
                const section = $(this);
                const sectionTop = section.offset().top - navbarHeight - buffer;
                const sectionBottom = sectionTop + section.outerHeight();
                
                if (scrollPosition >= sectionTop && scrollPosition < sectionBottom) {
                    const sectionId = section.attr('id');
                    $(`.navbar-nav li a[href="#${sectionId}"]`).parent().addClass('active');
                    return false;
                }
            });
        });
    }

    // 3. FIXED: Progress-bar with Intersection Observer
    function initializeProgressBars() {
        const progressBars = $(".progress-bar");

        if (progressBars.length) {
            const observer = new IntersectionObserver((entries) => {
                entries.forEach(entry => {
                    if (entry.isIntersecting) {
                        const $bar = $(entry.target);
                        const percentage = $bar.attr('aria-valuenow') || $bar.attr('data-percentage');
                        
                        if (percentage) {
                            // Animate the progress bar
                            $bar.css({
                                width: percentage + '%'
                            });
                            
                            // Add animation class
                            $bar.addClass('animated');
                        }
                        
                        observer.unobserve(entry.target);
                    }
                });
            }, {
                threshold: 0.1
            });
            
            progressBars.each(function() {
                $(this).css('width', '0%');
                observer.observe(this);
            });
        }
    }

    // 4. FIXED: Owl Carousel with proper error handling
    function initializeOwlCarousel() {
        // Check if Owl Carousel is loaded
        if (typeof $.fn.owlCarousel === 'function') {
            const $clientCarousel = $('#client');
            
            if ($clientCarousel.length) {
                $clientCarousel.owlCarousel({
                    items: 7,
                    loop: true,
                    smartSpeed: 1000,
                    autoplay: true,
                    dots: false,
                    autoplayHoverPause: true,
                    responsive: {
                        0: { items: 2 },
                        415: { items: 2 },
                        600: { items: 4 },
                        1199: { items: 4 },
                        1200: { items: 7 }
                    }
                });
            }
        } else {
            console.warn('Owl Carousel is not loaded. Please include the Owl Carousel script.');
        }
    }

    // 5. FIXED: Contact Form with enhanced validation
    function initializeContactForm() {
        const contactForm = $('form#contact-form');
        if (!contactForm.length) return;
        
        const submitButton = contactForm.find('button[type="submit"]');
        const originalButtonText = submitButton.text();
        
        // Initialize form status container
        if($('#form-status').length === 0) {
            contactForm.after('<div id="form-status" class="mt-3" style="display:none;"></div>');
        }
        const formStatus = $('#form-status');
        
        // Clear validation on input focus
        contactForm.find('input, textarea').on('focus', function() {
            $(this).removeClass('is-invalid');
            $(this).siblings('.invalid-feedback').remove();
        });
        
        // Enhanced form submission
        contactForm.on('submit', function(e) {
            e.preventDefault();
            
            // Clear previous validation
            contactForm.find('.invalid-feedback').remove();
            contactForm.find('.is-invalid').removeClass('is-invalid');
            formStatus.html('').hide();
            
            // Validate form
            let isValid = true;
            const requiredFields = contactForm.find('input[required], textarea[required]');
            
            requiredFields.each(function() {
                const field = $(this);
                const fieldValue = field.val().trim();
                
                if(!fieldValue) {
                    isValid = false;
                    field.addClass('is-invalid');
                    $('<div class="invalid-feedback">This field is required</div>').insertAfter(field);
                }
            });
            
            // Email validation
            const emailInput = contactForm.find('input[type="email"]');
            if(emailInput.length && emailInput.val().trim()) {
                const emailPattern = /^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$/;
                if(!emailPattern.test(emailInput.val().trim())) {
                    isValid = false;
                    emailInput.addClass('is-invalid');
                    $('<div class="invalid-feedback">Please enter a valid email address</div>').insertAfter(emailInput);
                }
            }
            
            if(!isValid) {
                showFormMessage('danger', 'Please fix the highlighted errors');
                return false;
            }
            
            // Submit form
            submitButton.prop('disabled', true).html('<i class="fa fa-spinner fa-spin"></i> Sending...');
            
            const formData = new FormData(contactForm[0]);
            
            $.ajax({
                url: contactForm.attr('action'),
                type: 'POST',
                data: formData,
                processData: false,
                contentType: false,
                success: function(response) {
                    showFormMessage('success', 'Thank you! Your message has been sent successfully.');
                    contactForm[0].reset();
                    
                    setTimeout(function() {
                        submitButton.prop('disabled', false).text(originalButtonText);
                    }, 2000);
                },
                error: function(xhr, status, error) {
                    let errorMessage = 'Sorry, there was a problem sending your message.';
                    
                    if(xhr.responseJSON && xhr.responseJSON.message) {
                        errorMessage += ' Error: ' + xhr.responseJSON.message;
                    }
                    
                    showFormMessage('danger', errorMessage);
                    submitButton.prop('disabled', false).text(originalButtonText);
                }
            });
        });
        
        function showFormMessage(type, message) {
            const iconClass = type === 'success' ? 'fa-check-circle' : 'fa-times-circle';
            formStatus.html(`
                <div class="alert alert-${type}">
                    <i class="fa ${iconClass}"></i> ${message}
                    <button type="button" class="close-alert">&times;</button>
                </div>
            `).fadeIn();
            
            startDismissTimer(formStatus);
        }
    }

    // 6. Initialize animations
    function initializeAnimations() {
        // Add page transition class
        $('body').addClass('page-transition');
        
        setTimeout(() => {
            $('body').addClass('loaded');
        }, 100);
        
        // Initialize scroll animations
        const animationObserver = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    entry.target.classList.add('animate-on-scroll');
                }
            });
        }, { threshold: 0.1 });
        
        $('.card-base, .section-heading, .portfolio-item').each(function() {
            animationObserver.observe(this);
        });
    }

    // Skills Section Enhanced Functionality
    // Counter Animation for Stats
    function animateCounters() {
        $('.stat-number').each(function() {
            const $this = $(this);
            const countTo = parseInt($this.attr('data-count'));
            
            $({ countNum: 0 }).animate({
                countNum: countTo
            }, {
                duration: 2000,
                easing: 'swing',
                step: function() {
                    $this.text(Math.floor(this.countNum));
                },
                complete: function() {
                    $this.text(this.countNum);
                }
            });
        });
    }
    
    // Skills Tab Switching
    $('.skill-tab').on('click', function() {
        const category = $(this).data('category');
        
        // Update active tab
        $('.skill-tab').removeClass('active');
        $(this).addClass('active');
        
        // Update active content
        $('.skill-category-content').removeClass('active');
        $('#' + category).addClass('active');
        
        // Animate progress bars after content is shown
        setTimeout(() => {
            animateProgressBars();
        }, 100);
    });
    
    // Progress Bar Animation
    function animateProgressBars() {
        $('.skill-progress-bar').each(function() {
            const width = $(this).data('width');
            $(this).css('width', '0%').animate({
                width: width + '%'
            }, 1500);
        });
    }
    
    // Intersection Observer for Skills Section
    const skillsObserver = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                // Animate counters
                animateCounters();
                
                // Animate progress bars
                setTimeout(() => {
                    animateProgressBars();
                }, 500);
                
                // Add animation classes to skill cards
                $('.skill-card').each(function(index) {
                    setTimeout(() => {
                        $(this).addClass('animate-in');
                    }, index * 100);
                });
                
                skillsObserver.unobserve(entry.target);
            }
        });
    }, {
        threshold: 0.2
    });
    
    // Observe skills section
    const skillsSection = document.querySelector('#skills');
    if (skillsSection) {
        skillsObserver.observe(skillsSection);
    }
    
    // Skill Card Hover Effects
    $('.skill-card').on('mouseenter', function() {
        $(this).find('.skill-progress-bar').addClass('pulse');
    }).on('mouseleave', function() {
        $(this).find('.skill-progress-bar').removeClass('pulse');
    });
    
    // Initialize progress bars for default active tab
    setTimeout(() => {
        animateProgressBars();
    }, 1000);
});

// Add pulse animation CSS dynamically
const pulseCSS = `
.skill-progress-bar.pulse::after {
    animation: shimmer 1s infinite;
}
`;

const style = document.createElement('style');
style.textContent = pulseCSS;
document.head.appendChild(style);

// Handle system theme changes
window.matchMedia('(prefers-color-scheme: dark)').addEventListener('change', function(e) {
    if (!localStorage.getItem('theme')) {
        const newTheme = e.matches ? 'dark' : 'light';
        document.documentElement.setAttribute('data-theme', newTheme);
        updateThemeIcons(newTheme);
    }
});

// Utility functions
function startDismissTimer(element) {
    const dismissTimeout = setTimeout(function() {
        element.fadeOut(500);
    }, 6000);
    
    element.data('dismissTimeout', dismissTimeout);
}

// Handle close button click for alerts
$(document).on('click', '.close-alert', function() {
    const alert = $(this).closest('.alert').parent();
    const timeout = alert.data('dismissTimeout');
    
    if (timeout) {
        clearTimeout(timeout);
    }
    
    alert.fadeOut(500);
    return false;
});

// Initialize theme before page renders
(function() {
    const currentTheme = localStorage.getItem('theme') || 
        (window.matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light');
    document.documentElement.setAttribute('data-theme', currentTheme);
})();

// Newsletter Form Handler
$(document).ready(function() {
    $('#newsletter-form').on('submit', function(e) {
        e.preventDefault();
        
        const email = $(this).find('input[type="email"]').val();
        const button = $(this).find('.newsletter-btn');
        const originalText = button.text();
        
        // Basic email validation
        if (!email || !email.includes('@')) {
            alert('Please enter a valid email address');
            return;
        }
        
        // Show loading state
        button.text('Subscribing...').prop('disabled', true);
        
        // Simulate API call (replace with your actual newsletter service)
        setTimeout(() => {
            button.text('Subscribed!').css('background', '#27ae60');
            $(this).find('input[type="email"]').val('');
            
            setTimeout(() => {
                button.text(originalText).prop('disabled', false).css('background', '');
            }, 3000);
        }, 1500);
    });
});

// Skills Redesigned Animation
$(document).ready(function() {
    
    // Animate progress bars when skills section comes into view
    function animateSkillBars() {
        $('.skill-progress-redesigned').each(function() {
            const progress = $(this).data('progress');
            $(this).css('width', progress + '%');
        });
    }
    
    // Intersection Observer for skills section
    const skillsObserver = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                setTimeout(animateSkillBars, 300);
                skillsObserver.unobserve(entry.target);
            }
        });
    }, {
        threshold: 0.2
    });
    
    // Observe skills section
    const skillsSection = document.querySelector('.skills-redesigned');
    if (skillsSection) {
        skillsObserver.observe(skillsSection);
    }
});
