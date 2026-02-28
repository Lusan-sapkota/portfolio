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
        initializeSkillsRedesigned();
        initializeSubdomainCards();
        initializeMobileInteractions();
        optimizeAnimations();
        handleResponsiveAnimations();

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
                
                // Close mobile menu if open - FIXED VERSION
                const navbarCollapse = $('.navbar-collapse');
                const navbarToggler = $('.navbar-toggler');
                
                if (navbarCollapse.hasClass('show')) {
                    // Use Bootstrap's collapse method for proper cleanup
                    navbarCollapse.collapse('hide');
                    
                    // Reset the toggler button state
                    navbarToggler.attr('aria-expanded', 'false');
                    navbarToggler.removeClass('collapsed').addClass('collapsed');
                }
                
                // Update active states
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
        const formWrapper = $('#contact-form-wrapper');
        const thankYouCard = $('#contact-thankyou');

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
                        if (response.status === 'success') {
                            // Populate thank-you card with sender's details
                            $('#thankyou-name').text(response.name || 'there');
                            $('#thankyou-email').text(response.email || 'your inbox');

                            // Swap form for thank-you card
                            formWrapper.fadeOut(250, function () {
                                thankYouCard.fadeIn(350);
                            });
                            contactForm[0].reset();
                        } else {
                            contactMessageDiv
                                .removeClass('alert-success alert-info')
                                .addClass('alert alert-' + (response.status === 'info' ? 'info' : 'danger'))
                                .text(response.message)
                                .show();
                            submitBtn.text(originalText).prop('disabled', false);
                            setTimeout(function () { contactMessageDiv.fadeOut(); }, 8000);
                        }
                    },
                    error: function () {
                        contactMessageDiv
                            .removeClass('alert-success alert-info')
                            .addClass('alert alert-danger')
                            .text('An error occurred while sending your message. Please try again.')
                            .show();
                        submitBtn.text(originalText).prop('disabled', false);
                        setTimeout(function () { contactMessageDiv.fadeOut(); }, 8000);
                    }
                });
            });

            // "Send another message" resets everything
            $('#contact-send-another').on('click', function () {
                thankYouCard.fadeOut(200, function () {
                    formWrapper.fadeIn(300);
                    contactForm[0].reset();
                    contactForm.find('.contact-btn').text('Submit').prop('disabled', false);
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

    // Enhanced Skills Progress Bar Animation for Redesigned Section
    function initializeSkillsRedesigned() {
        const skillsSection = document.querySelector('.skills-redesigned');
        if (!skillsSection) return;
        
        const observer = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    // Add animation class to trigger CSS animations
                    entry.target.classList.add('animate-in');
                    
                    // Animate all progress bars with staggered delay
                    const progressBars = entry.target.querySelectorAll('.skill-progress-redesigned');
                    progressBars.forEach((bar, index) => {
                        setTimeout(() => {
                            const percentage = bar.getAttribute('data-progress') || 
                                             bar.getAttribute('data-percentage') || 
                                             bar.getAttribute('aria-valuenow') || '0';
                            bar.style.width = percentage + '%';
                            bar.classList.add('animate');
                        }, index * 200); // Stagger animations
                    });
                    
                    observer.unobserve(entry.target);
                }
            });
        }, {
            threshold: 0.3,
            rootMargin: '0px 0px -100px 0px'
        });
        
        observer.observe(skillsSection);
    }
    
    // Enhanced Subdomain Cards Animation
    function initializeSubdomainCards() {
        const subdomainCards = document.querySelectorAll('.subdomain-card');
        if (subdomainCards.length === 0) return;
        
        const observer = new IntersectionObserver((entries) => {
            entries.forEach((entry, index) => {
                if (entry.isIntersecting) {
                    setTimeout(() => {
                        entry.target.style.opacity = '1';
                        entry.target.style.transform = 'translateY(0)';
                    }, index * 150); // Stagger card animations
                    
                    observer.unobserve(entry.target);
                }
            });
        }, {
            threshold: 0.2,
            rootMargin: '0px 0px -50px 0px'
        });
        
        // Initially hide cards for animation
        subdomainCards.forEach(card => {
            card.style.opacity = '0';
            card.style.transform = 'translateY(30px)';
            card.style.transition = 'all 0.8s cubic-bezier(0.4, 0, 0.2, 1)';
            observer.observe(card);
        });
    }
    
    // Touch-friendly interactions for mobile
    function initializeMobileInteractions() {
        const isMobile = window.innerWidth <= 768;
        const isTouch = 'ontouchstart' in window;
        
        if (isMobile || isTouch) {
            // Add touch feedback for subdomain cards
            const subdomainCards = document.querySelectorAll('.subdomain-card');
            subdomainCards.forEach(card => {
                card.addEventListener('touchstart', function() {
                    this.style.transform = 'translateY(-8px) scale(1.02)';
                });
                
                card.addEventListener('touchend', function() {
                    setTimeout(() => {
                        this.style.transform = '';
                    }, 150);
                });
            });
            
            // Add touch feedback for skill categories
            const skillCategories = document.querySelectorAll('.skill-category-redesigned');
            skillCategories.forEach(category => {
                category.addEventListener('touchstart', function() {
                    this.style.transform = 'translateY(-4px)';
                });
                
                category.addEventListener('touchend', function() {
                    setTimeout(() => {
                        this.style.transform = '';
                    }, 150);
                });
            });
        }
    }
    
    // Performance optimization for animations
    function optimizeAnimations() {
        // Pause animations when tab is hidden
        document.addEventListener('visibilitychange', function() {
            const body = document.body;
            if (document.hidden) {
                body.style.animationPlayState = 'paused';
            } else {
                body.style.animationPlayState = 'running';
            }
        });
        
        // Reduce animations on low-end devices
        if (navigator.hardwareConcurrency && navigator.hardwareConcurrency < 4) {
            document.documentElement.style.setProperty('--transition', '0.2s ease');
            document.documentElement.style.setProperty('--transition-fast', '0.1s ease');
        }
    }
    
    // Enhanced responsive behavior
    function handleResponsiveAnimations() {
        const mediaQuery = window.matchMedia('(max-width: 768px)');
        
        function handleMobileChange(e) {
            const subdomainCards = document.querySelectorAll('.subdomain-card');
            const skillCategories = document.querySelectorAll('.skill-category-redesigned');
            
            if (e.matches) {
                // Mobile optimizations
                subdomainCards.forEach(card => {
                    card.style.setProperty('--hover-transform', 'translateY(-10px) scale(1.02)');
                });
                
                skillCategories.forEach(category => {
                    category.style.setProperty('--hover-transform', 'translateY(-4px)');
                });
            } else {
                // Desktop optimizations
                subdomainCards.forEach(card => {
                    card.style.removeProperty('--hover-transform');
                });
                
                skillCategories.forEach(category => {
                    category.style.removeProperty('--hover-transform');
                });
            }
        }
        
        mediaQuery.addListener(handleMobileChange);
        handleMobileChange(mediaQuery);
    }
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

// Enhanced Mobile Skills Animation - Add this function
function initializeMobileSkillBars() {
    // Check if we're on a mobile device
    const isMobile = window.innerWidth <= 768 || /Android|iPhone|iPad|iPod|BlackBerry|IEMobile|Opera Mini/i.test(navigator.userAgent);
    
    if (isMobile) {
        // Force show all skill bars immediately on mobile
        const progressBars = document.querySelectorAll('.skill-progress-redesigned');
        progressBars.forEach((bar, index) => {
            const percentage = bar.getAttribute('data-progress') || 
                             bar.getAttribute('data-percentage') || 
                             bar.getAttribute('aria-valuenow') || '75'; // Default to 75% if no data
            
            // Set width immediately for mobile
            setTimeout(() => {
                bar.style.width = percentage + '%';
                bar.style.opacity = '1';
                bar.classList.add('mobile-animated');
            }, index * 100); // Stagger slightly for visual appeal
        });
    }
}

// Call on page load and resize
document.addEventListener('DOMContentLoaded', function() {
    initializeMobileSkillBars();
    
    // Re-initialize on window resize
    let resizeTimer;
    window.addEventListener('resize', function() {
        clearTimeout(resizeTimer);
        resizeTimer = setTimeout(initializeMobileSkillBars, 250);
    });
});
