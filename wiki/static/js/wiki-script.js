document.addEventListener('DOMContentLoaded', function() {
    // Dark mode toggle
    const themeToggle = document.getElementById('wiki-theme-toggle');
    
    if (themeToggle) {
        const moonIcon = themeToggle.querySelector('.fa-moon');
        const sunIcon = themeToggle.querySelector('.fa-sun');
        
        // Check for saved theme preference from main site
        const currentTheme = localStorage.getItem('theme') || 
            (window.matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light');
        
        // Apply theme based on main site preference
        if (currentTheme === 'dark') {
            document.documentElement.setAttribute('data-theme', 'dark');
            moonIcon.classList.add('d-none');
            sunIcon.classList.remove('d-none');
        }
        
        // Toggle dark mode using the main site's approach
        themeToggle.addEventListener('click', function() {
            const isDarkMode = document.documentElement.getAttribute('data-theme') === 'dark';
            
            // Toggle theme
            if (isDarkMode) {
                document.documentElement.setAttribute('data-theme', 'light');
                localStorage.setItem('theme', 'light');
                sunIcon.classList.add('d-none');
                moonIcon.classList.remove('d-none');
            } else {
                document.documentElement.setAttribute('data-theme', 'dark');
                localStorage.setItem('theme', 'dark');
                moonIcon.classList.add('d-none');
                sunIcon.classList.remove('d-none');
            }
        });
    }
    
    // Category collapse icons
    document.querySelectorAll('.wiki-category-header, .wiki-subcategory-header').forEach(header => {
        const icon = header.querySelector('i.fas');
        const collapseId = header.getAttribute('href');
        const collapseElement = document.querySelector(collapseId);
        
        if (icon && collapseElement) {
            // Set aria-expanded attribute
            header.setAttribute('aria-expanded', 'false');
            
            // Add Bootstrap collapse event listener
            collapseElement.addEventListener('show.bs.collapse', () => {
                header.setAttribute('aria-expanded', 'true');
                icon.classList.replace('fa-chevron-right', 'fa-chevron-down');
            });
            
            collapseElement.addEventListener('hide.bs.collapse', () => {
                header.setAttribute('aria-expanded', 'false');
                icon.classList.replace('fa-chevron-down', 'fa-chevron-right');
            });
            
            // Mark active item based on current page
            const currentPath = window.location.pathname;
            collapseElement.querySelectorAll('.list-group-item').forEach(item => {
                if (item.getAttribute('href') === currentPath) {
                    item.classList.add('active');
                    header.classList.add('active');
                    
                    // Automatically expand the category containing the active item
                    const bsCollapse = new bootstrap.Collapse(collapseElement, {
                        toggle: false
                    });
                    bsCollapse.show();
                }
            });
        }
    });
});