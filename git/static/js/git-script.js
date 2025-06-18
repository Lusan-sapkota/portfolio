/*==================================
Git Section - Interactive Features
Lusan Sapkota Portfolio
==================================== */

document.addEventListener('DOMContentLoaded', function() {
    // Navbar scroll effect
    const navbar = document.querySelector('.navbar');
    let lastScrollTop = 0;
    
    function handleNavbarScroll() {
        const scrollTop = window.pageYOffset || document.documentElement.scrollTop;
        
        // Add/remove scrolled class based on scroll position
        if (scrollTop > 50) {
            navbar.classList.add('scrolled');
        } else {
            navbar.classList.remove('scrolled');
        }
        
        // Hide/show navbar on scroll (optional - uncomment if needed)
        // if (scrollTop > lastScrollTop && scrollTop > 100) {
        //     navbar.style.transform = 'translateY(-100%)';
        // } else {
        //     navbar.style.transform = 'translateY(0)';
        // }
        
        lastScrollTop = scrollTop <= 0 ? 0 : scrollTop;
    }
    
    // Throttled scroll listener for better performance
    let ticking = false;
    function requestTick() {
        if (!ticking) {
            requestAnimationFrame(handleNavbarScroll);
            ticking = true;
            setTimeout(() => ticking = false, 16); // ~60fps
        }
    }
    
    window.addEventListener('scroll', requestTick);
    
    // Cache DOM elements
    const navToggle = document.getElementById('navToggle');
    const filterSidebar = document.getElementById('filterSidebar');
    const searchInput = document.getElementById('searchInput');
    const searchClear = document.getElementById('searchClear');
    const projectsGrid = document.getElementById('projectsGrid');
    const loadingState = document.getElementById('loadingState');
    const resultsCount = document.getElementById('resultsCount');
    const sortSelect = document.getElementById('sortBy');
    const viewButtons = document.querySelectorAll('.view-btn');
    const filterInputs = document.querySelectorAll('input[name="category"], input[name="type"], input[name="status"]');
    const filterResetBtn = document.getElementById('filterReset');
    const clearFiltersBtn = document.getElementById('clearFilters');
    const themeToggle = document.getElementById('themeToggle');
    const themeIcon = document.getElementById('themeIcon');
    
    // State management
    let currentFilters = {
        category: '',
        type: '',
        status: '',
        search: '',
        sort: 'featured'
    };
    
    let debounceTimer;
    let isLoading = false;
    
    // Initialize
    initializeFilters();
    setupEventListeners();
    initializeDarkMode();
    
    function initializeFilters() {
        // Get current filters from URL
        const urlParams = new URLSearchParams(window.location.search);
        currentFilters.category = urlParams.get('category') || '';
        currentFilters.type = urlParams.get('type') || '';
        currentFilters.status = urlParams.get('status') || '';
        currentFilters.search = urlParams.get('q') || '';
        
        // Set input values
        if (searchInput) searchInput.value = currentFilters.search;
        
        // Set filter checkboxes
        filterInputs.forEach(input => {
            const filterType = input.name;
            const filterValue = input.value;
            
            if (currentFilters[filterType] === filterValue) {
                input.checked = true;
                input.closest('.filter-item').classList.add('active');
            }
        });
        
        // Show/hide search clear button
        toggleSearchClear();
    }
    
    function setupEventListeners() {
        // Navigation toggle
        if (navToggle) {
            navToggle.addEventListener('click', toggleSidebar);
        }
        
        // Search functionality
        if (searchInput) {
            searchInput.addEventListener('input', handleSearchInput);
            searchInput.addEventListener('keypress', function(e) {
                if (e.key === 'Enter') {
                    e.preventDefault();
                    applyFilters();
                }
            });
        }
        
        if (searchClear) {
            searchClear.addEventListener('click', clearSearch);
        }
        
        // Filter inputs
        filterInputs.forEach(input => {
            input.addEventListener('change', handleFilterChange);
        });
        
        // Sort functionality
        if (sortSelect) {
            sortSelect.addEventListener('change', handleSortChange);
        }
        
        // View toggle
        viewButtons.forEach(btn => {
            btn.addEventListener('click', () => toggleView(btn.dataset.view));
        });
        
        // Reset filters
        if (filterResetBtn) {
            filterResetBtn.addEventListener('click', resetAllFilters);
        }
        
        if (clearFiltersBtn) {
            clearFiltersBtn.addEventListener('click', resetAllFilters);
        }
        
        // Filter tag removal
        document.addEventListener('click', function(e) {
            if (e.target.matches('.filter-tag i')) {
                const filterType = e.target.dataset.filter;
                removeFilter(filterType);
            }
        });
        
        // Close sidebar on outside click (mobile)
        document.addEventListener('click', function(e) {
            if (window.innerWidth <= 768 && 
                filterSidebar && 
                filterSidebar.classList.contains('show') &&
                !filterSidebar.contains(e.target) &&
                !navToggle.contains(e.target)) {
                closeSidebar();
            }
        });
        
        // Responsive sidebar handling
        window.addEventListener('resize', handleResize);
        
        // Dark mode toggle
        if (themeToggle) {
            themeToggle.addEventListener('click', function() {
                const currentTheme = document.documentElement.getAttribute('data-theme');
                const newTheme = currentTheme === 'dark' ? 'light' : 'dark';
                
                document.documentElement.setAttribute('data-theme', newTheme);
                localStorage.setItem('theme', newTheme);
                updateThemeIcon(newTheme);
            });
        }
    }
    
    function toggleSidebar() {
        if (!filterSidebar) return;
        
        navToggle.classList.toggle('active');
        
        if (window.innerWidth <= 768) {
            filterSidebar.classList.toggle('show');
        } else {
            filterSidebar.classList.toggle('hidden');
        }
    }
    
    function closeSidebar() {
        if (!filterSidebar) return;
        
        navToggle.classList.remove('active');
        
        if (window.innerWidth <= 768) {
            filterSidebar.classList.remove('show');
        } else {
            filterSidebar.classList.add('hidden');
        }
    }
    
    function handleResize() {
        if (window.innerWidth > 768 && filterSidebar) {
            filterSidebar.classList.remove('show');
            if (navToggle.classList.contains('active')) {
                filterSidebar.classList.remove('hidden');
            }
        }
    }
    
    function handleSearchInput(e) {
        clearTimeout(debounceTimer);
        
        const searchTerm = e.target.value.trim();
        currentFilters.search = searchTerm;
        
        toggleSearchClear();
        
        // Debounce search to avoid too many API calls
        debounceTimer = setTimeout(() => {
            applyFilters();
        }, 300);
    }
    
    function clearSearch() {
        if (searchInput) {
            searchInput.value = '';
            currentFilters.search = '';
            toggleSearchClear();
            applyFilters();
        }
    }
    
    function toggleSearchClear() {
        if (!searchClear) return;
        
        if (currentFilters.search) {
            searchClear.style.display = 'block';
        } else {
            searchClear.style.display = 'none';
        }
    }
    
    function handleFilterChange(e) {
        const filterType = e.target.name;
        const filterValue = e.target.value;
        const filterItem = e.target.closest('.filter-item');
        
        // Update active states
        document.querySelectorAll(`input[name="${filterType}"]`).forEach(input => {
            input.closest('.filter-item').classList.remove('active');
        });
        
        if (e.target.checked) {
            filterItem.classList.add('active');
            currentFilters[filterType] = filterValue;
        } else {
            currentFilters[filterType] = '';
        }
        
        applyFilters();
    }
    
    function handleSortChange(e) {
        currentFilters.sort = e.target.value;
        sortProjects();
    }
    
    function removeFilter(filterType) {
        if (filterType === 'search') {
            clearSearch();
            return;
        }
        
        currentFilters[filterType] = '';
        
        // Update radio buttons
        const radioInput = document.querySelector(`input[name="${filterType}"][value=""]`);
        if (radioInput) {
            radioInput.checked = true;
            
            // Update active states
            document.querySelectorAll(`input[name="${filterType}"]`).forEach(input => {
                input.closest('.filter-item').classList.remove('active');
            });
            
            radioInput.closest('.filter-item').classList.add('active');
        }
        
        applyFilters();
    }
    
    function resetAllFilters() {
        // Reset all filters
        currentFilters = {
            category: '',
            type: '',
            status: '',
            search: '',
            sort: 'featured'
        };
        
        // Reset UI
        if (searchInput) searchInput.value = '';
        if (sortSelect) sortSelect.value = 'featured';
        
        // Reset filter inputs
        filterInputs.forEach(input => {
            input.closest('.filter-item').classList.remove('active');
            if (input.value === '') {
                input.checked = true;
                input.closest('.filter-item').classList.add('active');
            } else {
                input.checked = false;
            }
        });
        
        toggleSearchClear();
        applyFilters();
    }
    
    function applyFilters() {
        if (isLoading) return;
        
        isLoading = true;
        showLoading();
        
        // Build query parameters
        const params = new URLSearchParams();
        
        if (currentFilters.category) params.set('category', currentFilters.category);
        if (currentFilters.type) params.set('type', currentFilters.type);
        if (currentFilters.status) params.set('status', currentFilters.status);
        if (currentFilters.search) params.set('q', currentFilters.search);
        
        // Make API request
        fetch(`/git/api/projects?${params.toString()}`)
            .then(response => response.json())
            .then(projects => {
                renderProjects(projects);
                updateResultsCount(projects.length);
                updateURL(params);
                isLoading = false;
                hideLoading();
            })
            .catch(error => {
                console.error('Error fetching projects:', error);
                showError();
                isLoading = false;
                hideLoading();
            });
    }
    
    function renderProjects(projects) {
        if (!projectsGrid) return;
        
        if (projects.length === 0) {
            projectsGrid.innerHTML = `
                <div class="no-projects">
                    <div class="no-projects-icon">
                        <i class="fas fa-search"></i>
                    </div>
                    <h3>No projects found</h3>
                    <p>Try adjusting your filters or search terms.</p>
                    <button class="btn btn-primary" onclick="resetAllFilters()">
                        <i class="fas fa-undo"></i>
                        Clear All Filters
                    </button>
                </div>
            `;
            return;
        }
        
        // Sort projects
        const sortedProjects = sortProjectsArray(projects, currentFilters.sort);
        
        projectsGrid.innerHTML = sortedProjects.map(project => createProjectCard(project)).join('');
        
        // Add animations
        animateProjectCards();
    }
    
    function createProjectCard(project) {
        const technologies = project.technologies || [];
        const displayTechs = technologies.slice(0, 4);
        const moreTechsCount = technologies.length - 4;
        
        return `
            <div class="project-card ${project.is_featured ? 'featured' : ''}" data-project-id="${project.id}">
                ${project.is_featured ? `
                    <div class="featured-badge">
                        <i class="fas fa-star"></i>
                        Featured
                    </div>
                ` : ''}
                
                <div class="project-header">
                    ${project.image_url ? `
                        <div class="project-image">
                            <img src="${project.image_url}" alt="${project.title}" loading="lazy">
                            <div class="project-overlay">
                                <div class="project-actions">
                                    ${project.github_url ? `
                                        <a href="${project.github_url}" target="_blank" class="action-btn" title="View Source">
                                            <i class="fab fa-github"></i>
                                        </a>
                                    ` : ''}
                                    ${project.live_url ? `
                                        <a href="${project.live_url}" target="_blank" class="action-btn" title="Live Demo">
                                            <i class="fas fa-external-link-alt"></i>
                                        </a>
                                    ` : ''}
                                    <a href="/git/project/${project.id}" class="action-btn" title="View Details">
                                        <i class="fas fa-info-circle"></i>
                                    </a>
                                </div>
                            </div>
                        </div>
                    ` : ''}
                </div>
                
                <div class="project-content">
                    <div class="project-meta">
                        ${project.category ? `
                            <span class="project-category">
                                <i class="fas fa-folder"></i>
                                ${project.category}
                            </span>
                        ` : ''}
                        
                        <div class="project-status">
                            <span class="status-badge status-${project.status}">
                                ${getStatusIcon(project.status)}
                                ${project.status.charAt(0).toUpperCase() + project.status.slice(1)}
                            </span>
                        </div>
                    </div>
                    
                    <h3 class="project-title">
                        <a href="/git/project/${project.id}">${project.title}</a>
                    </h3>
                    
                    <p class="project-description">${truncateText(project.description, 120)}</p>
                    
                    <div class="project-technologies">
                        ${displayTechs.map(tech => `<span class="tech-tag">${tech.trim()}</span>`).join('')}
                        ${moreTechsCount > 0 ? `<span class="tech-more">+${moreTechsCount} more</span>` : ''}
                    </div>
                    
                    <div class="project-footer">
                        <div class="project-stats">
                            <div class="stat-item">
                                <i class="${project.is_opensource ? 'fab fa-osi' : 'fas fa-briefcase'}"></i>
                                <span>${project.is_opensource ? 'Open Source' : 'Commercial'}</span>
                            </div>
                            
                            ${project.stars > 0 ? `
                                <div class="stat-item">
                                    <i class="fas fa-star"></i>
                                    <span>${project.stars}</span>
                                </div>
                            ` : ''}
                        </div>
                        
                        <div class="project-links">
                            ${project.github_url ? `
                                <a href="${project.github_url}" target="_blank" class="btn btn-sm btn-outline">
                                    <i class="fab fa-github"></i>
                                    Code
                                </a>
                            ` : ''}
                            
                            ${project.live_url ? `
                                <a href="${project.live_url}" target="_blank" class="btn btn-sm btn-primary">
                                    <i class="fas fa-external-link-alt"></i>
                                    Demo
                                </a>
                            ` : ''}
                        </div>
                    </div>
                </div>
            </div>
        `;
    }
    
    function getStatusIcon(status) {
        switch (status) {
            case 'completed':
                return '<i class="fas fa-check-circle"></i>';
            case 'in-progress':
                return '<i class="fas fa-spinner fa-spin"></i>';
            case 'maintenance':
                return '<i class="fas fa-tools"></i>';
            default:
                return '<i class="fas fa-circle"></i>';
        }
    }
    
    function truncateText(text, maxLength) {
        if (!text) return '';
        if (text.length <= maxLength) return text;
        return text.substr(0, maxLength) + '...';
    }
    
    function sortProjects() {
        const projectCards = Array.from(projectsGrid.children);
        const sortedCards = sortProjectsArray(projectCards, currentFilters.sort);
        
        // Clear and re-append sorted cards
        projectsGrid.innerHTML = '';
        sortedCards.forEach(card => projectsGrid.appendChild(card));
        
        animateProjectCards();
    }
    
    function sortProjectsArray(items, sortBy) {
        const itemsCopy = [...items];
        
        switch (sortBy) {
            case 'featured':
                return itemsCopy.sort((a, b) => {
                    const aFeatured = a.is_featured || a.classList?.contains('featured');
                    const bFeatured = b.is_featured || b.classList?.contains('featured');
                    if (aFeatured && !bFeatured) return -1;
                    if (!aFeatured && bFeatured) return 1;
                    return 0;
                });
                
            case 'newest':
                return itemsCopy.sort((a, b) => {
                    const aDate = new Date(a.created_at || 0);
                    const bDate = new Date(b.created_at || 0);
                    return bDate - aDate;
                });
                
            case 'oldest':
                return itemsCopy.sort((a, b) => {
                    const aDate = new Date(a.created_at || 0);
                    const bDate = new Date(b.created_at || 0);
                    return aDate - bDate;
                });
                
            case 'stars':
                return itemsCopy.sort((a, b) => {
                    const aStars = a.stars || 0;
                    const bStars = b.stars || 0;
                    return bStars - aStars;
                });
                
            case 'name':
                return itemsCopy.sort((a, b) => {
                    const aName = a.title || a.querySelector('.project-title')?.textContent || '';
                    const bName = b.title || b.querySelector('.project-title')?.textContent || '';
                    return aName.localeCompare(bName);
                });
                
            default:
                return itemsCopy;
        }
    }
    
    function toggleView(view) {
        viewButtons.forEach(btn => btn.classList.remove('active'));
        document.querySelector(`[data-view="${view}"]`).classList.add('active');
        
        if (projectsGrid) {
            projectsGrid.className = `projects-grid ${view === 'list' ? 'list-view' : ''}`;
        }
    }
    
    function updateResultsCount(count) {
        if (resultsCount) {
            resultsCount.textContent = count;
        }
    }
    
    function updateURL(params) {
        const newURL = `${window.location.pathname}${params.toString() ? '?' + params.toString() : ''}`;
        window.history.pushState({}, '', newURL);
    }
    
    function showLoading() {
        if (loadingState) {
            loadingState.style.display = 'block';
        }
        if (projectsGrid) {
            projectsGrid.style.opacity = '0.5';
        }
    }
    
    function hideLoading() {
        if (loadingState) {
            loadingState.style.display = 'none';
        }
        if (projectsGrid) {
            projectsGrid.style.opacity = '1';
        }
    }
    
    function showError() {
        if (projectsGrid) {
            projectsGrid.innerHTML = `
                <div class="no-projects">
                    <div class="no-projects-icon">
                        <i class="fas fa-exclamation-triangle"></i>
                    </div>
                    <h3>Error loading projects</h3>
                    <p>Please try again later or contact support if the problem persists.</p>
                    <button class="btn btn-primary" onclick="location.reload()">
                        <i class="fas fa-redo"></i>
                        Retry
                    </button>
                </div>
            `;
        }
    }
    
    function animateProjectCards() {
        const cards = projectsGrid.querySelectorAll('.project-card');
        
        cards.forEach((card, index) => {
            card.style.opacity = '0';
            card.style.transform = 'translateY(20px)';
            
            setTimeout(() => {
                card.style.transition = 'opacity 0.3s ease, transform 0.3s ease';
                card.style.opacity = '1';
                card.style.transform = 'translateY(0)';
            }, index * 50);
        });
    }
    
    // Dark mode toggle
    function initializeDarkMode() {
        const currentTheme = localStorage.getItem('theme') || 'light';
        
        // Set initial theme
        document.documentElement.setAttribute('data-theme', currentTheme);
        updateThemeIcon(currentTheme);
        
        function updateThemeIcon(theme) {
            if (themeIcon) {
                if (theme === 'dark') {
                    themeIcon.className = 'fas fa-sun';
                    themeToggle.title = 'Switch to Light Mode';
                } else {
                    themeIcon.className = 'fas fa-moon';
                    themeToggle.title = 'Switch to Dark Mode';
                }
            }
        }
    }
    
    // Expose functions for global access
    window.resetAllFilters = resetAllFilters;
    window.removeFilter = removeFilter;
    
    // Initialize animations on page load
    setTimeout(animateProjectCards, 100);
});