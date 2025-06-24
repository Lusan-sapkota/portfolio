// Define globally accessible functions
function updateThemeIcons(theme) {
    const moonIcons = document.querySelectorAll('.fa-moon');
    const sunIcons = document.querySelectorAll('.fa-sun');
    
    moonIcons.forEach(icon => icon.classList.toggle('d-none', theme === 'dark'));
    sunIcons.forEach(icon => icon.classList.toggle('d-none', theme === 'light'));
}

$(document).ready(function(){
    "use strict";

        // Initialize all components
        initializeDarkMode();
        initializeScrollEffects();
        initializeSmoothScrolling();
        initializeProgressBars();
        initializeOwlCarousel();
        initializeContactForm();
        initializeAnimations();

        // FIXED: Dark Mode Implementation
        function initializeDarkMode() {
            const currentTheme = document.documentElement.getAttribute('data-theme');
            
            // Set up theme toggle functionality
            $('#theme-toggle, #mobile-theme-toggle').on('click', function(e) {
                e.preventDefault();
                
                const current = document.documentElement.getAttribute('data-theme');
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

        // ... rest of your existing code remains unchanged ...

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
        
        // Better active section detection with improved logic
        $(window).on('scroll', function() {
            const scrollPosition = $(this).scrollTop();
            const windowHeight = $(window).height();
            const navbarHeight = $('nav.navbar').outerHeight() || 70;
            
            let activeSection = null;
            
            $('section[id]').each(function() {
                const section = $(this);
                const sectionTop = section.offset().top - navbarHeight - 50;
                const sectionBottom = sectionTop + section.outerHeight();
                const sectionId = section.attr('id');
                
                // Check if section is in viewport
                if (scrollPosition >= sectionTop && scrollPosition < sectionBottom) {
                    activeSection = sectionId;
                }
                
                // Special case for last section
                if (scrollPosition + windowHeight >= $(document).height() - 100) {
                    activeSection = $('section[id]:last').attr('id');
                }
            });
            
            // Update navbar active state
            if (activeSection) {
                $('.navbar-nav li').removeClass('active');
                $(`.navbar-nav li a[href="#${activeSection}"]`).parent().addClass('active');
            }
        });
        
        // Initial active section check on page load
        setTimeout(() => {
            $(window).trigger('scroll');
        }, 100);

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

    // 5. Contact Form Handling
    function initializeContactForm() {
        const contactForm = $('#contact-form');
        const contactMessageDiv = $('#contact-message');

        if (contactForm.length) {
            contactForm.on('submit', function (e) {
                e.preventDefault();

                const submitBtn = contactForm.find('.contact-btn');
                const originalText = submitBtn.text();
                const formData = new FormData(this);

                submitBtn.text('Sending...').prop('disabled', true);
                contactMessageDiv.hide();

                $.ajax({
                    url: contactForm.attr('action'),
                    type: 'POST',
                    data: formData,
                    processData: false,
                    contentType: false,
                    success: function (response) {
                        contactMessageDiv
                            .removeClass('alert-success alert-danger alert-info')
                            .addClass('alert alert-' + (response.status === 'error' ? 'danger' : response.status === 'info' ? 'info' : 'success'))
                            .text(response.message)
                            .show();

                        if (response.status === 'success') {
                            contactForm[0].reset();
                        }
                    },
                    error: function () {
                        contactMessageDiv
                            .removeClass('alert-success alert-info')
                            .addClass('alert alert-danger')
                            .text('An error occurred while sending your message. Please try again.')
                            .show();
                    },
                    complete: function () {
                        submitBtn.text(originalText).prop('disabled', false);
                        setTimeout(function () {
                            contactMessageDiv.fadeOut();
                        }, 8000);
                    }
                });
            });
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
