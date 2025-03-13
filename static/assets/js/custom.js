$(document).ready(function(){
	"use strict";

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
		
		 // Enhanced smooth scrolling (replaces old smooth-menu code)
        $('a[href^="#"]').on('click', function(event) {
            event.preventDefault();
            
            // Get the target section
            const targetId = $(this).attr('href');
            if(targetId === '#') return;
            
            const targetSection = $(targetId);
            if(!targetSection.length) return;
            
            // Calculate offset for navbar
            const navbar = $('nav.navbar');
            const navbarHeight = navbar.length ? navbar.outerHeight() : 0;
            
            // Smoothly scroll to target with offset
            $('html, body').animate({
                scrollTop: targetSection.offset().top - navbarHeight
            }, 1200, 'easeInOutExpo');
            
            // Close mobile menu if open
            const navbarCollapse = $('.navbar-collapse');
            if (navbarCollapse.hasClass('in')) {
                navbarCollapse.removeClass('in');
            }
        });
        
        // Active menu handling during scroll
        $(window).on('scroll', function() {
            const scrollPosition = $(window).scrollTop();
            const navbarHeight = $('nav.navbar').outerHeight();
            
            $('section').each(function() {
                const section = $(this);
                const sectionTop = section.offset().top - navbarHeight - 20;
                const sectionHeight = section.outerHeight();
                const sectionId = section.attr('id');
                
                if(scrollPosition >= sectionTop && scrollPosition < sectionTop + sectionHeight) {
                    $('.navbar-nav li').removeClass('active');
                    $(`.navbar-nav li a[href="#${sectionId}"]`).parent().addClass('active');
                }
            });
        });
        
        // Set 100vh height for sections
        function setSectionHeights() {
            const vh = $(window).height();
            const navbar = $('nav.navbar');
            const navbarHeight = navbar.length ? navbar.outerHeight() : 0;
            
            $('section').each(function() {
                $(this).css('min-height', vh);
                
                // Add extra padding to first section for navbar
                if($(this).attr('id') === 'welcome-hero') {
                    $(this).css('padding-top', navbarHeight);
                }
            });
        }
        
        // Initialize section heights
        setSectionHeights();
        $(window).on('resize', setSectionHeights);

		$('body').scrollspy({
			target:'.navbar-collapse',
			offset:0
		});

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

});
