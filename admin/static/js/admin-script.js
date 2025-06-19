// Admin Dashboard JavaScript
$(document).ready(function() {
    // Initialize tooltips
    var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    var tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });
    
    // Initialize session timer
    initSessionTimer();
    
    // Auto-hide alerts after 5 seconds
    setTimeout(function() {
        $('.alert').fadeOut('slow');
    }, 5000);
    
    // Confirm delete actions
    $('.delete-confirm').on('click', function(e) {
        e.preventDefault();
        const message = $(this).data('confirm-message') || 'Are you sure you want to delete this item?';
        if (confirm(message)) {
            const form = $(this).closest('form');
            if (form.length) {
                form.submit();
            } else {
                window.location.href = $(this).attr('href');
            }
        }
    });
    
    // Handle AJAX form submissions
    $('.ajax-form').on('submit', function(e) {
        e.preventDefault();
        const form = $(this);
        const formData = new FormData(this);
        const url = form.attr('action');
        const method = form.attr('method') || 'POST';
        
        // Show loading state
        const submitBtn = form.find('button[type="submit"]');
        const originalText = submitBtn.html();
        submitBtn.prop('disabled', true).html('<i class="fas fa-spinner fa-spin"></i> Saving...');
        
        // Convert FormData to JSON for consistent handling
        const data = {};
        formData.forEach((value, key) => {
            if (key.endsWith('[]')) {
                // Handle array inputs
                const arrayKey = key.slice(0, -2);
                if (!data[arrayKey]) data[arrayKey] = [];
                data[arrayKey].push(value);
            } else if (form.find(`[name="${key}"][type="checkbox"]`).length) {
                // Handle checkboxes
                data[key] = form.find(`[name="${key}"]:checked`).length > 0;
            } else {
                data[key] = value;
            }
        });
        
        $.ajax({
            url: url,
            method: method,
            headers: {
                'Content-Type': 'application/json',
            },
            data: JSON.stringify(data),
            success: function(response) {
                if (response.status === 'success') {
                    markFormAsSaved(form); // Mark form as saved
                    showNotification('success', response.message || 'Operation completed successfully!');
                    // Redirect if specified
                    if (response.redirect) {
                        setTimeout(() => window.location.href = response.redirect, 1000);
                    }
                } else {
                    showNotification('error', response.message || 'An error occurred');
                }
            },
            error: function(xhr) {
                let message = 'An error occurred';
                if (xhr.responseJSON && xhr.responseJSON.message) {
                    message = xhr.responseJSON.message;
                }
                showNotification('error', message);
            },
            complete: function() {
                // Restore button state
                submitBtn.prop('disabled', false).html(originalText);
            }
        });
    });
    
    // Character counters for text inputs
    $('[data-max-length]').each(function() {
        const input = $(this);
        const maxLength = input.data('max-length');
        const counterId = input.attr('id') + 'Count';
        
        // Create counter element if it doesn't exist
        if (!$('#' + counterId).length) {
            input.after(`<small class="form-text text-muted"><span id="${counterId}">0</span>/${maxLength}</small>`);
        }
        
        // Update counter on input
        input.on('input', function() {
            const count = this.value.length;
            $('#' + counterId).text(count);
            
            // Change color based on limits
            if (count > maxLength) {
                $('#' + counterId).parent().removeClass('text-muted text-warning').addClass('text-danger');
            } else if (count > maxLength * 0.8) {
                $('#' + counterId).parent().removeClass('text-muted text-danger').addClass('text-warning');
            } else {
                $('#' + counterId).parent().removeClass('text-warning text-danger').addClass('text-muted');
            }
        });
        
        // Initial count
        input.trigger('input');
    });
    
    // Image preview functionality
    $('input[type="file"].image-preview').on('change', function() {
        const input = this;
        const previewId = $(input).data('preview');
        
        if (input.files && input.files[0]) {
            const reader = new FileReader();
            reader.onload = function(e) {
                $('#' + previewId).attr('src', e.target.result).show();
            };
            reader.readAsDataURL(input.files[0]);
        }
    });
    
    // URL validation for URL inputs
    $('input[type="url"]').on('blur', function() {
        const input = $(this);
        const value = input.val().trim();
        
        if (value && !isValidUrl(value)) {
            input.addClass('is-invalid');
            if (!input.next('.invalid-feedback').length) {
                input.after('<div class="invalid-feedback">Please enter a valid URL</div>');
            }
        } else {
            input.removeClass('is-invalid');
            input.next('.invalid-feedback').remove();
        }
    });
    
    // Search functionality
    $('.search-input').on('input', debounce(function() {
        const query = $(this).val().toLowerCase();
        const target = $(this).data('search-target');
        
        $(target).each(function() {
            const text = $(this).text().toLowerCase();
            $(this).toggle(text.includes(query));
        });
    }, 300));
    
    // Sortable tables
    if (typeof Sortable !== 'undefined') {
        $('.sortable tbody').each(function() {
            new Sortable(this, {
                handle: '.sort-handle',
                animation: 150,
                onEnd: function(evt) {
                    // Send new order to server
                    const items = [];
                    $(evt.to).find('tr').each(function(index) {
                        const id = $(this).data('id');
                        if (id) items.push({ id: id, order: index });
                    });
                    
                    if (items.length > 0) {
                        updateItemOrder(items);
                    }
                }
            });
        });
    }
});

// Utility functions
function showNotification(type, message, duration = 5000) {
    let alertClass, icon;
    
    switch(type) {
        case 'success':
            alertClass = 'alert-success';
            icon = 'fas fa-check-circle';
            break;
        case 'warning':
            alertClass = 'alert-warning';
            icon = 'fas fa-exclamation-triangle';
            break;
        case 'info':
            alertClass = 'alert-info';
            icon = 'fas fa-info-circle';
            break;
        case 'error':
        default:
            alertClass = 'alert-danger';
            icon = 'fas fa-exclamation-triangle';
            break;
    }
    
    const notification = $(`
        <div class="alert ${alertClass} alert-dismissible fade show notification-toast" role="alert" style="position: fixed; top: 20px; right: 20px; z-index: 9999; min-width: 300px;">
            <i class="${icon} me-2"></i>${message}
            <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
        </div>
    `);
    
    $('body').append(notification);
    
    // Auto-remove after duration
    setTimeout(() => {
        notification.fadeOut(() => notification.remove());
    }, duration);
}

function isValidUrl(string) {
    try {
        new URL(string);
        return true;
    } catch (_) {
        return false;
    }
}

function debounce(func, wait, immediate) {
    var timeout;
    return function() {
        var context = this, args = arguments;
        var later = function() {
            timeout = null;
            if (!immediate) func.apply(context, args);
        };
        var callNow = immediate && !timeout;
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
        if (callNow) func.apply(context, args);
    };
}

function updateItemOrder(items) {
    $.ajax({
        url: '/admin/api/update-order',
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        data: JSON.stringify({ items: items }),
        success: function(response) {
            if (response.status === 'success') {
                showNotification('success', 'Order updated successfully!');
            }
        },
        error: function() {
            showNotification('error', 'Failed to update order');
        }
    });
}

// Export functions for use in other scripts
window.AdminUtils = {
    showNotification: showNotification,
    isValidUrl: isValidUrl,
    debounce: debounce
};

// Session Timer Management
let sessionTimer = null;
let sessionTimeRemaining = 0;
let warningShown = false;
let lastActivityTime = Date.now();

function initSessionTimer() {
    // Check if session timer elements exist
    if (!$('#session-timer-compact').length) {
        return;
    }
    
    // Get initial session time
    fetchSessionTime();
    
    // Start the timer
    sessionTimer = setInterval(updateSessionTimer, 1000);
    
    // Bind extend session buttons
    $('#extend-session-btn-dropdown').on('click', extendSession);
    
    // Track user activity for save reminders
    trackUserActivity();
    
    // Warn before leaving if there are unsaved changes
    window.addEventListener('beforeunload', function(e) {
        if (hasUnsavedChanges()) {
            e.preventDefault();
            e.returnValue = '';
        }
    });
}

function fetchSessionTime() {
    $.ajax({
        url: '/admin/api/session-status',
        method: 'GET',
        success: function(response) {
            if (response.status === 'active' || response.status === 'warning') {
                sessionTimeRemaining = response.time_remaining;
                lastActivityTime = Date.now();
                warningShown = false;
                updateSessionDisplay();
            } else if (response.status === 'expired') {
                handleSessionExpired();
            }
        },
        error: function(xhr) {
            console.error('Failed to fetch session status:', xhr.status);
            // If we get a 401/403, the session is likely expired
            if (xhr.status === 401 || xhr.status === 403) {
                handleSessionExpired();
            }
        }
    });
}

function updateSessionTimer() {
    if (sessionTimeRemaining <= 0) {
        handleSessionExpired();
        return;
    }
    
    sessionTimeRemaining--;
    updateSessionDisplay();
    
    // Show warning at 5 minutes
    if (sessionTimeRemaining <= 300 && !warningShown) {
        showSessionWarning();
        warningShown = true;
    }
    
    // Show save reminder for long inactive periods
    const inactiveTime = (Date.now() - lastActivityTime) / 1000;
    if (inactiveTime > 300 && hasUnsavedChanges()) { // 5 minutes of inactivity
        showSaveReminder();
        lastActivityTime = Date.now(); // Reset to avoid spam
    }
}

function updateSessionDisplay() {
    const timeStr = formatTime(sessionTimeRemaining);
    
    // Update compact display
    $('#session-timer-compact').text(timeStr);
    
    // Update dropdown display
    const $dropdownTimer = $('#session-timer-dropdown');
    $dropdownTimer.text(timeStr);
    
    // Update badge color based on time remaining
    $dropdownTimer.removeClass('bg-success bg-warning bg-danger');
    if (sessionTimeRemaining > 900) { // > 15 minutes
        $dropdownTimer.addClass('bg-success');
    } else if (sessionTimeRemaining > 300) { // > 5 minutes
        $dropdownTimer.addClass('bg-warning');
    } else {
        $dropdownTimer.addClass('bg-danger');
    }
    
    // Show/hide warning in dropdown
    if (sessionTimeRemaining <= 300) {
        $('#session-warning-dropdown').removeClass('d-none');
    } else {
        $('#session-warning-dropdown').addClass('d-none');
    }
}

function formatTime(seconds) {
    const minutes = Math.floor(seconds / 60);
    const remainingSeconds = seconds % 60;
    return `${minutes}:${remainingSeconds.toString().padStart(2, '0')}`;
}

function showSessionWarning() {
    showNotification(
        'warning',
        `<i class="fas fa-clock"></i> Session Warning: Your session will expire in ${formatTime(sessionTimeRemaining)}. <button type="button" class="btn btn-sm btn-outline-light ms-2" onclick="extendSession()">Extend Session</button>`,
        10000
    );
}

function showSaveReminder() {
    showNotification(
        'info',
        '<i class="fas fa-save"></i> Save Reminder: You have unsaved changes. Consider saving your work.',
        5000
    );
}

function extendSession() {
    $.ajax({
        url: '/admin/api/extend-session',
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        data: JSON.stringify({}),
        success: function(response) {
            if (response.status === 'success') {
                sessionTimeRemaining = response.time_remaining;
                warningShown = false;
                updateSessionDisplay();
                showNotification('success', 'Session extended successfully!', 3000);
            } else {
                showNotification('error', response.message || 'Failed to extend session');
            }
        },
        error: function() {
            showNotification('error', 'Failed to extend session');
        }
    });
}

function handleSessionExpired() {
    clearInterval(sessionTimer);
    
    // Show final warning
    showNotification(
        'error',
        '<i class="fas fa-exclamation-triangle"></i> Session Expired: You will be redirected to login.',
        3000
    );
    
    // Redirect to login after a short delay
    setTimeout(() => {
        window.location.href = '/admin/login?expired=1';
    }, 3000);
}

function trackUserActivity() {
    // Track various user activities
    $(document).on('click keypress scroll mousemove', function() {
        lastActivityTime = Date.now();
    });
    
    // Track form changes
    $(document).on('input change', 'input, textarea, select', function() {
        lastActivityTime = Date.now();
        markFormAsChanged($(this).closest('form'));
    });
}

function hasUnsavedChanges() {
    return $('.form-changed').length > 0;
}

function markFormAsChanged(form) {
    form.addClass('form-changed');
}

function markFormAsSaved(form) {
    form.removeClass('form-changed');
}