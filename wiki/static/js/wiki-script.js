document.addEventListener('DOMContentLoaded', function() {
    // Ensure dropdown works on click only
    const dropdownToggle = document.getElementById('mainSiteDropdown');
    if (dropdownToggle) {
        // Remove any existing event listeners that might interfere
        dropdownToggle.addEventListener('click', function(e) {
            // Let Bootstrap handle the dropdown
            // Don't prevent default here
        });
        
        // Prevent accidental hover behavior
        const dropdown = dropdownToggle.closest('.dropdown');
        if (dropdown) {
            dropdown.addEventListener('mouseenter', function(e) {
                // Don't trigger dropdown on hover
                e.stopPropagation();
            });
            
            dropdown.addEventListener('mouseleave', function(e) {
                // Don't close dropdown on mouse leave
                e.stopPropagation();
            });
        }
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

// Function to set active navigation state
function setActiveNavigation() {
    const currentPath = window.location.pathname;
    const navLinks = document.querySelectorAll('.navbar-nav .nav-link');
    
    // Remove active class from all nav links
    navLinks.forEach(link => {
        link.classList.remove('active');
    });
    
    // Add active class based on current page
    if (currentPath.includes('/wiki')) {
        if (currentPath.includes('/search')) {
            // Search page
            const searchLink = document.querySelector('a[href*="search"]');
            if (searchLink) searchLink.classList.add('active');
        } else if (currentPath.includes('/random')) {
            // Random page
            const randomLink = document.querySelector('a[href*="random"]');
            if (randomLink) randomLink.classList.add('active');
        } else {
            // Wiki home or article page
            const wikiLink = document.querySelector('a[href*="wiki.index"]');
            if (wikiLink) wikiLink.classList.add('active');
        }
    }
}

// Functions for random page interactions
function bookmarkArticle(articleId) {
    // Add to bookmarks (could integrate with localStorage or backend)
    const bookmarks = JSON.parse(localStorage.getItem('wiki-bookmarks') || '[]');
    if (!bookmarks.includes(articleId)) {
        bookmarks.push(articleId);
        localStorage.setItem('wiki-bookmarks', JSON.stringify(bookmarks));
        showNotification('Article bookmarked!', 'success');
    } else {
        showNotification('Article already bookmarked!', 'info');
    }
}

function shareArticle(articleId, title) {
    // Share functionality
    if (navigator.share) {
        navigator.share({
            title: title,
            url: window.location.origin + `/wiki/article/${articleId}`
        });
    } else {
        // Fallback: copy to clipboard
        const url = window.location.origin + `/wiki/article/${articleId}`;
        navigator.clipboard.writeText(url).then(() => {
            showNotification('Article link copied to clipboard!', 'success');
        });
    }
}

function showNotification(message, type = 'info') {
    // Simple notification system
    const notification = document.createElement('div');
    notification.className = `alert alert-${type} notification`;
    notification.style.cssText = `
        position: fixed;
        top: 20px;
        right: 20px;
        z-index: 9999;
        max-width: 300px;
        border-radius: 12px;
        opacity: 0;
        transition: all 0.3s ease;
    `;
    notification.textContent = message;
    
    document.body.appendChild(notification);
    
    // Fade in
    setTimeout(() => {
        notification.style.opacity = '1';
        notification.style.transform = 'translateY(0)';
    }, 100);
    
    // Fade out and remove
    setTimeout(() => {
        notification.style.opacity = '0';
        notification.style.transform = 'translateY(-20px)';
        setTimeout(() => notification.remove(), 300);
    }, 3000);
}

function shareArticle() {
    if (navigator.share) {
        navigator.share({
            title: '{{ article.title|e }}',
            text: '{{ article.get_excerpt(100)|e }}',
            url: window.location.href
        });
    } else {
        copyLink();
    }
}

function shareOnTwitter() {
    const text = encodeURIComponent('{{ article.title|e }} - {{ article.get_excerpt(100)|e }}');
    const url = encodeURIComponent(window.location.href);
    window.open(`https://twitter.com/intent/tweet?text=${text}&url=${url}`, '_blank');
}

function shareOnFacebook() {
    const url = encodeURIComponent(window.location.href);
    window.open(`https://www.facebook.com/sharer/sharer.php?u=${url}`, '_blank');
}

function shareOnLinkedIn() {
    const url = encodeURIComponent(window.location.href);
    const title = encodeURIComponent('{{ article.title|e }}');
    const summary = encodeURIComponent('{{ article.get_excerpt(100)|e }}');
    window.open(`https://www.linkedin.com/sharing/share-offsite/?url=${url}&title=${title}&summary=${summary}`, '_blank');
}

function copyLink() {
    navigator.clipboard.writeText(window.location.href).then(() => {
        alert('Link copied to clipboard!');
    });
}

function bookmarkArticle() {
    alert('Bookmark feature coming soon!');
}