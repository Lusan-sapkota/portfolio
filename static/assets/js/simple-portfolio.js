// Modern Portfolio JavaScript - Enhanced Navigation & Interactions

class SimplePortfolio {
    constructor() {
        this.sections = [];
        this.currentSection = '';
        this.init();
    }

    init() {
        this.setupSubdomainCards();
        this.setupScrollEffects();
        this.setupSmoothScrolling();
        this.setupNavigationHighlighting(); // Now properly defined
        this.setupThemeToggle();
        this.setupPortfolioFilter();
        this.initSections();
        this.setupSkillsAnimation();
        this.setupMobileNavigation(); // Added mobile nav fix
    }

    // Initialize sections for navigation
    initSections() {
        this.sections = [
            'subdomains', 'about', 'education', 'skills', 
            'experience', 'profiles', 'portfolio', 'contact'
        ];
    }

    // FIXED: Properly define setupNavigationHighlighting
    setupNavigationHighlighting() {
        const navLinks = document.querySelectorAll('.smooth-menu');
        
        // Update active navigation on scroll
        window.addEventListener('scroll', () => {
            this.updateActiveNavigation();
        });
        
        // Set up click handlers for navigation links
        navLinks.forEach(link => {
            link.addEventListener('click', (e) => {
                // Remove active class from all links
                navLinks.forEach(l => l.classList.remove('active'));
                // Add active class to clicked link
                link.classList.add('active');
            });
        });
    }

    // FIXED: Mobile Navigation Setup
    setupMobileNavigation() {
        const navbarToggler = document.querySelector('.navbar-toggler');
        const navbarCollapse = document.querySelector('.navbar-collapse');
        
        if (navbarToggler && navbarCollapse) {
            navbarToggler.addEventListener('click', () => {
                navbarCollapse.classList.toggle('show');
                navbarToggler.classList.toggle('collapsed');
            });
            
            // Close mobile menu when clicking on nav links
            const navLinks = document.querySelectorAll('.nav-link');
            navLinks.forEach(link => {
                link.addEventListener('click', () => {
                    navbarCollapse.classList.remove('show');
                    navbarToggler.classList.add('collapsed');
                });
            });
        }
    }

    // Subdomain Cards
    setupSubdomainCards() {
        const cards = document.querySelectorAll('.subdomain-card');
        
        cards.forEach(card => {
            card.addEventListener('click', (e) => {
                const subdomain = card.dataset.subdomain;
                if (subdomain) {
                    this.navigateToSubdomain(subdomain);
                }
            });
        });

        // Handle subdomain buttons
        const buttons = document.querySelectorAll('.subdomain-btn');
        buttons.forEach(btn => {
            btn.addEventListener('click', (e) => {
                e.preventDefault();
                e.stopPropagation();
                const subdomain = btn.dataset.subdomain;
                if (subdomain) {
                    this.navigateToSubdomain(subdomain);
                }
            });
        });
    }

    // Enhanced Scroll Effects
    setupScrollEffects() {
        const navbar = document.querySelector('.navbar');
        let lastScrollTop = 0;

        window.addEventListener('scroll', () => {
            const scrollTop = window.pageYOffset || document.documentElement.scrollTop;
            
            // Add scrolled class
            if (scrollTop > 50) {
                navbar.classList.add('scrolled');
            } else {
                navbar.classList.remove('scrolled');
            }

            // Hide/show navbar on scroll
            if (scrollTop > lastScrollTop && scrollTop > 100) {
                navbar.classList.add('nav-hidden');
            } else {
                navbar.classList.remove('nav-hidden');
            }
            lastScrollTop = scrollTop;
        });
    }

    // Smooth Scrolling for Navigation Links
    setupSmoothScrolling() {
        const navLinks = document.querySelectorAll('.smooth-menu');
        
        navLinks.forEach(link => {
            link.addEventListener('click', (e) => {
                e.preventDefault();
                const targetId = link.getAttribute('href').substring(1);
                const targetSection = document.getElementById(targetId);
                
                if (targetSection) {
                    const navbarHeight = document.querySelector('.navbar').offsetHeight;
                    const targetPosition = targetSection.offsetTop - navbarHeight - 20;
                    
                    window.scrollTo({
                        top: targetPosition,
                        behavior: 'smooth'
                    });

                    // Close mobile menu if open
                    const navbarCollapse = document.querySelector('.navbar-collapse');
                    if (navbarCollapse && navbarCollapse.classList.contains('show')) {
                        navbarCollapse.classList.remove('show');
                        const toggler = document.querySelector('.navbar-toggler');
                        if (toggler) {
                            toggler.classList.add('collapsed');
                        }
                    }
                }
            });
        });
    }

    // Navigation Highlighting
    updateActiveNavigation() {
        const navLinks = document.querySelectorAll('.smooth-menu');
        const sections = document.querySelectorAll('section[id]');
        const scrollPosition = window.scrollY + 100;

        sections.forEach(section => {
            const sectionTop = section.offsetTop;
            const sectionHeight = section.offsetHeight;
            const sectionId = section.getAttribute('id');

            if (scrollPosition >= sectionTop && scrollPosition < sectionTop + sectionHeight) {
                // Remove active class from all nav links
                navLinks.forEach(link => link.classList.remove('active'));
                
                // Add active class to current section link
                const activeLink = document.querySelector(`.smooth-menu[href="#${sectionId}"]`);
                if (activeLink) {
                    activeLink.classList.add('active');
                }
                
                this.currentSection = sectionId;
            }
        });
    }

    // Theme Toggle
    setupThemeToggle() {
        const themeToggles = document.querySelectorAll('#theme-toggle, #mobile-theme-toggle');
        
        themeToggles.forEach(toggle => {
            toggle.addEventListener('click', (e) => {
                e.preventDefault();
                this.toggleTheme();
            });
        });

        // Load saved theme
        const savedTheme = localStorage.getItem('portfolio-theme') || 'light';
        this.setTheme(savedTheme);
    }

    toggleTheme() {
        const currentTheme = document.documentElement.getAttribute('data-theme') || 'light';
        const newTheme = currentTheme === 'light' ? 'dark' : 'light';
        
        // Add transition class for smooth animation
        document.body.classList.add('theme-transitioning');
        
        setTimeout(() => {
            this.setTheme(newTheme);
            setTimeout(() => {
                document.body.classList.remove('theme-transitioning');
            }, 300);
        }, 50);
    }

    setTheme(theme) {
        document.documentElement.setAttribute('data-theme', theme);
        localStorage.setItem('portfolio-theme', theme);
        
        // Update theme toggle icons
        const moonIcons = document.querySelectorAll('.fa-moon');
        const sunIcons = document.querySelectorAll('.fa-sun');
        
        if (theme === 'dark') {
            moonIcons.forEach(icon => {
                icon.style.display = 'none';
                icon.style.opacity = '0';
            });
            sunIcons.forEach(icon => {
                icon.style.display = 'inline-block';
                icon.style.opacity = '1';
            });
        } else {
            sunIcons.forEach(icon => {
                icon.style.display = 'none';
                icon.style.opacity = '0';
            });
            moonIcons.forEach(icon => {
                icon.style.display = 'inline-block';
                icon.style.opacity = '1';
            });
        }
        
        // Animate the toggle button
        const toggleButtons = document.querySelectorAll('#theme-toggle, #mobile-theme-toggle');
        toggleButtons.forEach(btn => {
            btn.style.transform = 'rotate(360deg)';
            setTimeout(() => {
                btn.style.transform = 'rotate(0deg)';
            }, 300);
        });
    }

    // Portfolio Filter
    setupPortfolioFilter() {
        const filterBtns = document.querySelectorAll('.filter-btn');
        const portfolioItems = document.querySelectorAll('.portfolio-item');
        
        filterBtns.forEach(btn => {
            btn.addEventListener('click', () => {
                // Remove active class from all buttons
                filterBtns.forEach(b => b.classList.remove('active'));
                // Add active class to clicked button
                btn.classList.add('active');
                
                const filter = btn.getAttribute('data-filter');
                
                portfolioItems.forEach(item => {
                    if (filter === 'all' || item.getAttribute('data-category') === filter) {
                        item.style.display = 'block';
                        item.style.animation = 'fadeInUp 0.5s ease-in-out';
                    } else {
                        item.style.display = 'none';
                    }
                });
            });
        });
    }

    // Skills Animation
    setupSkillsAnimation() {
        const observerOptions = {
            threshold: 0.1,
            rootMargin: '0px 0px -50px 0px'
        };

        const observer = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    this.animateSkillBars(entry.target);
                }
            });
        }, observerOptions);

        // Observe skills section
        const skillsSection = document.querySelector('#skills');
        if (skillsSection) {
            observer.observe(skillsSection);
        }
    }

    animateSkillBars(section) {
        const skillBars = section.querySelectorAll('.skill-bar');
        
        skillBars.forEach(bar => {
            const percentage = bar.getAttribute('data-percentage');
            if (percentage) {
                setTimeout(() => {
                    bar.style.width = percentage + '%';
                }, 200);
            }
        });
    }

    // Navigation to subdomains
    navigateToSubdomain(subdomain) {
        const config = window.subdomainConfig || {};
        const subdomainData = config[subdomain];
        
        let url;
        if (subdomainData && subdomainData.url) {
            url = subdomainData.url;
        } else {
            // Fallback URLs
            switch(subdomain) {
                case 'wiki':
                    url = 'https://wiki.lusansapkota.com.np';
                    break;
                case 'git':
                    url = 'https://git.lusansapkota.com.np';
                    break;
                case 'donation':
                    url = 'https://donation.lusansapkota.com.np';
                    break;
                case 'store':
                    url = 'https://store.lusansapkota.com.np';
                    break;
                default:
                    console.warn(`Unknown subdomain: ${subdomain}`);
                    return;
            }
        }
        
        // Open external links in new tab
        if (url.startsWith('http') || url.startsWith('//')) {
            window.open(url, '_blank');
        } else {
            window.location.href = url;
        }
    }
}

// Enhanced Subdomain Cards Animation
function initializeSubdomainAnimations() {
    const cards = document.querySelectorAll('.subdomain-card');
    
    // Intersection Observer for scroll animations
    const observer = new IntersectionObserver((entries) => {
        entries.forEach((entry, index) => {
            if (entry.isIntersecting) {
                setTimeout(() => {
                    entry.target.classList.add('in-view');
                }, index * 100); // Staggered animation
            }
        });
    }, {
        threshold: 0.1,
        rootMargin: '0px 0px -50px 0px'
    });
    
    cards.forEach(card => {
        observer.observe(card);
        
        // Add click ripple effect
        card.addEventListener('click', function(e) {
            const ripple = document.createElement('span');
            const rect = this.getBoundingClientRect();
            const size = Math.max(rect.width, rect.height);
            const x = e.clientX - rect.left - size / 2;
            const y = e.clientY - rect.top - size / 2;
            
            ripple.style.width = ripple.style.height = size + 'px';
            ripple.style.left = x + 'px';
            ripple.style.top = y + 'px';
            ripple.classList.add('ripple-effect');
            
            this.appendChild(ripple);
            
            setTimeout(() => {
                ripple.remove();
            }, 600);
        });
        
        // Add loading state simulation
        card.addEventListener('mousedown', function() {
            this.classList.add('loading');
        });
        
        card.addEventListener('mouseup', function() {
            setTimeout(() => {
                this.classList.remove('loading');
            }, 200);
        });
    });
}

// Global navigation functions for backward compatibility
function navigateToWiki() {
    if (window.portfolio) {
        window.portfolio.navigateToSubdomain('wiki');
    }
}

function navigateToGit() {
    if (window.portfolio) {
        window.portfolio.navigateToSubdomain('git');
    }
}

function navigateToDonation() {
    if (window.portfolio) {
        window.portfolio.navigateToSubdomain('donation');
    }
}

function navigateToStore() {
    if (window.portfolio) {
        window.portfolio.navigateToSubdomain('store');
    }
}

// Initialize when DOM is ready
document.addEventListener('DOMContentLoaded', () => {
    window.portfolio = new SimplePortfolio();
    initializeSubdomainAnimations();
});
