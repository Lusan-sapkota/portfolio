$(document).ready(function(){
    "use strict";

    // Dark Mode Implementation
    function initializeDarkMode() {
        // Check for saved theme preference or use preferred color scheme
        const currentTheme = localStorage.getItem('theme') || 
            (window.matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light');
        
        // Apply the theme
        if (currentTheme === 'dark') {
            document.documentElement.setAttribute('data-theme', 'dark');
            $('.fa-moon').hide();
            $('.fa-sun').show();
        } else {
            document.documentElement.setAttribute('data-theme', 'light');
            $('.fa-sun').hide();
            $('.fa-moon').show();
        }
        
        // Set up theme toggle functionality
        $('#theme-toggle').on('click', function(e) {
            e.preventDefault();
            
            // Toggle theme
            if (document.documentElement.getAttribute('data-theme') === 'dark') {
                document.documentElement.setAttribute('data-theme', 'light');
                localStorage.setItem('theme', 'light');
                $('.fa-sun').hide();
                $('.fa-moon').show();
            } else {
                document.documentElement.setAttribute('data-theme', 'dark');
                localStorage.setItem('theme', 'dark');
                $('.fa-moon').hide();
                $('.fa-sun').show();
            }
        });
    }

    // Initialize dark mode
    initializeDarkMode();

    // 1. Scroll To Top 
        $(window).on('scroll',function () {
            if ($(this).scrollTop() > 600) {
                $('.return-to-top').fadeIn();
            } else {
                $('.return-to-top').fadeOut();
            }
        });
        $('.return-to-top').on('click',function(){
                $('html, body').animate({
                scrollTop: 0
            }, 1500);
            return false;
        });
    
    
    
    // 2. Smooth Scroll spy
        
        $('.header-area').sticky({
           topSpacing:0
        });
        
        // IMPROVED: Enhanced smooth scrolling with faster animation
        $('.smooth-menu a, a.smooth-menu, a[href^="#"]').on('click', function(event) {
            if(this.hash !== "") {
                event.preventDefault();
                
                // Get the target section
                const targetId = this.hash;
                const targetSection = $(targetId);
                if(!targetSection.length) return;
                
                // Calculate offset for navbar
                const navbar = $('nav.navbar');
                const navbarHeight = navbar.length ? navbar.outerHeight() : 0;
                
                // Smoothly scroll to target with offset - faster animation (800ms instead of 1200ms)
                $('html, body').animate({
                    scrollTop: targetSection.offset().top - navbarHeight
                }, 800, 'easeInOutExpo');
                
                // Close mobile menu if open
                const navbarCollapse = $('.navbar-collapse');
                if (navbarCollapse.hasClass('in')) {
                    navbarCollapse.removeClass('in');
                }
                
                // Update active state manually
                $('.navbar-nav li').removeClass('active');
                $(`a[href="${targetId}"]`).parent('li').addClass('active');
            }
        });
        
        // IMPROVED: Better active section detection with more precision
        $(window).on('scroll', function() {
            const scrollPosition = $(this).scrollTop();
            const navbarHeight = $('nav.navbar').outerHeight();
            
            // Use a small buffer to avoid multiple active sections
            const buffer = 5;
            
            // Reset active state
            $('.navbar-nav li').removeClass('active');
            
            // Find the current section and set as active
            $('section').each(function() {
                const section = $(this);
                const sectionTop = section.offset().top - navbarHeight - buffer;
                const sectionBottom = sectionTop + section.outerHeight();
                
                if (scrollPosition >= sectionTop && scrollPosition < sectionBottom) {
                    const sectionId = section.attr('id');
                    $(`.navbar-nav li a[href="#${sectionId}"]`).parent().addClass('active');
                    return false; // Break the loop once we found the active section
                }
            });
        });

        // Remove the conflicting scrollspy initialization
        // $('body').scrollspy({
        //	target:'.navbar-collapse',
        //	offset:0
        // });

    // 3. Progress-bar
    
        var dataToggleTooTip = $('[data-toggle="tooltip"]');
        var progressBar = $(".progress-bar");
        if (progressBar.length) {
            progressBar.appear(function () {
                dataToggleTooTip.tooltip({
                    trigger: 'manual'
                }).tooltip('show');
                progressBar.each(function () {
                    var each_bar_width = $(this).attr('aria-valuenow');
                    $(this).width(each_bar_width + '%');
                });
            });
        }
    
    // 4. owl carousel
    
        // i. client (carousel)
        
            $('#client').owlCarousel({
                items:7,
                loop:true,
                smartSpeed: 1000,
                autoplay:true,
                dots:false,
                autoplayHoverPause:true,
                responsive:{
                        0:{
                            items:2
                        },
                        415:{
                            items:2
                        },
                        600:{
                            items:4

                        },
                        1199:{
                            items:4
                        },
                        1200:{
                            items:7
                        }
                    }
                });
                
                
                $('.play').on('click',function(){
                    owl.trigger('play.owl.autoplay',[1000])
                })
                $('.stop').on('click',function(){
                    owl.trigger('stop.owl.autoplay')
                })


    // 5. welcome animation support

        $(window).load(function(){
            $(".header-text h2,.header-text p").removeClass("animated fadeInUp").css({'opacity':'0'});
            $(".header-text a").removeClass("animated fadeInDown").css({'opacity':'0'});
        });

        $(window).load(function(){
            $(".header-text h2,.header-text p").addClass("animated fadeInUp").css({'opacity':'0'});
            $(".header-text a").addClass("animated fadeInDown").css({'opacity':'0'});
        });

    // Form validation and submission handling
    $(document).ready(function() {
        const contactForm = $('form#contact-form');
        const submitButton = contactForm.find('button[type="submit"]');
        const originalButtonText = submitButton.text();
        
        // Initialize form status container with better styling
        if($('#form-status').length === 0) {
            contactForm.after('<div id="form-status" class="mt-3" style="display:none;"></div>');
        }
        const formStatus = $('#form-status');
        
        // Clear previous validation on input focus
        contactForm.find('input, textarea').on('focus', function() {
            $(this).removeClass('is-invalid');
            $(this).siblings('.invalid-feedback').remove();
        });
        
        contactForm.on('submit', function(e) {
            e.preventDefault();
            
            // Remove any previous validation messages
            contactForm.find('.invalid-feedback').remove();
            contactForm.find('.is-invalid').removeClass('is-invalid');
            formStatus.html('').hide();
            
            // Validate form
            let isValid = true;
            const requiredFields = contactForm.find('input[required], textarea[required]');
            
            // Check each required field
            requiredFields.each(function() {
                const field = $(this);
                const fieldValue = field.val().trim();
                
                if(!fieldValue) {
                    isValid = false;
                    field.addClass('is-invalid');
                    // Insert feedback directly after the input
                    $('<div class="invalid-feedback">This field is required</div>').insertAfter(field);
                }
            });
            
            // Validate email format with more comprehensive regex
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
                // Show validation summary with close button
                formStatus.html('<div class="alert alert-danger">' +
                    '<i class="fa fa-exclamation-circle"></i> Please fix the highlighted errors' +
                    '<button type="button" class="close-alert">&times;</button></div>').fadeIn();
                
                // Auto-dismiss after 8 seconds
                startDismissTimer(formStatus);
                
                // Scroll to the first error
                $('html, body').animate({
                    scrollTop: contactForm.find('.is-invalid').first().offset().top - 100
                }, 500);
                return false;
            }
            
            // Update button state and show loading indicator
            submitButton.prop('disabled', true).html('<i class="fa fa-spinner fa-spin"></i> Sending...');
            
            // Prepare form data correctly
            const formData = new FormData(contactForm[0]);
            
            // Submit form via AJAX with proper FormData
            $.ajax({
                url: contactForm.attr('action'),
                type: 'POST',
                data: formData,
                processData: false,
                contentType: false,
                success: function(response) {
                    // Success message with animation and close button
                    formStatus.html('<div class="alert alert-success">' + 
                        '<i class="fa fa-check-circle"></i> ' +
                        'Thank you! Your message has been sent successfully.' +
                        '<button type="button" class="close-alert">&times;</button></div>')
                        .hide().fadeIn();
                    
                    // Auto-dismiss after 6 seconds
                    startDismissTimer(formStatus);
                    
                    // Reset form
                    contactForm[0].reset();
                    
                    // Reset button after delay
                    setTimeout(function() {
                        submitButton.prop('disabled', false).text(originalButtonText);
                    }, 2000);
                },
                error: function(xhr, status, error) {
                    // Detailed error message with close button
                    let errorMessage = 'Sorry, there was a problem sending your message.';
                    
                    if(xhr.responseJSON && xhr.responseJSON.message) {
                        errorMessage += ' Error: ' + xhr.responseJSON.message;
                    }
                    
                    formStatus.html('<div class="alert alert-danger">' +
                        '<i class="fa fa-times-circle"></i> ' + errorMessage + 
                        '<button type="button" class="close-alert">&times;</button></div>').fadeIn();
                    
                    // Auto-dismiss after 8 seconds
                    startDismissTimer(formStatus);
                    
                    // Reset button
                    submitButton.prop('disabled', false).text(originalButtonText);
                }
            });
        });
        
        // Additional visual feedback - highlight fields while typing
        contactForm.find('input, textarea').on('input', function() {
            const field = $(this);
            if(field.val().trim()) {
                field.addClass('is-valid').removeClass('is-invalid');
            } else if(field.prop('required')) {
                field.removeClass('is-valid');
            }
        });
    });
    
    // 6. Handle theme based on system changes
    window.matchMedia('(prefers-color-scheme: dark)').addEventListener('change', function(e) {
        if (!localStorage.getItem('theme')) {
            // Only auto-switch if user hasn't manually set a preference
            if (e.matches) {
                document.documentElement.setAttribute('data-theme', 'dark');
                $('.fa-moon').hide();
                $('.fa-sun').show();
            } else {
                document.documentElement.setAttribute('data-theme', 'light');
                $('.fa-sun').hide();
                $('.fa-moon').show();
            }
        }
    });
});

// Function to start auto-dismiss timer
function startDismissTimer(element) {
    const dismissTimeout = setTimeout(function() {
        element.fadeOut(500);
    }, 6000); // 6 seconds before auto-dismiss
    
    // Store the timeout ID on the element so we can cancel if user manually closes
    element.data('dismissTimeout', dismissTimeout);
}

// Handle close button click for alerts
$(document).on('click', '.close-alert', function() {
    // Find the parent alert
    const alert = $(this).closest('.alert').parent();
    
    // Clear any existing timeout to prevent duplicated fadeouts
    const timeout = alert.data('dismissTimeout');
    if (timeout) {
        clearTimeout(timeout);
    }
    
    // Fade out the alert
    alert.fadeOut(500);
    
    // Prevent event bubbling
    return false;
});

// Handle validation summary dismiss in case it has one
$(document).on('click', '.alert', function() {
    const alert = $(this);
    const timeout = alert.data('dismissTimeout');
    if (timeout) {
        clearTimeout(timeout);
    }
    alert.fadeOut(500);
});

// Initialize dark mode on page load (outside document ready for faster execution)
(function() {
    // Set theme before page renders to prevent flashing
    const currentTheme = localStorage.getItem('theme') || 
        (window.matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light');
    if (currentTheme === 'dark') {
        document.documentElement.setAttribute('data-theme', 'dark');
    }
})();
