// Main JavaScript for Game Manager Web Interface

// Toast notification system
function showToast(message, type = 'info') {
    const toast = document.getElementById('toast');
    const toastBody = document.getElementById('toast-body');
    const toastHeader = toast.querySelector('.toast-header');
    
    // Set message
    toastBody.textContent = message;
    
    // Set icon and color based on type
    const icon = toastHeader.querySelector('i');
    icon.className = 'me-2';
    
    switch(type) {
        case 'success':
            icon.classList.add('bi', 'bi-check-circle', 'text-success');
            break;
        case 'error':
            icon.classList.add('bi', 'bi-exclamation-triangle', 'text-danger');
            break;
        case 'warning':
            icon.classList.add('bi', 'bi-exclamation-circle', 'text-warning');
            break;
        default:
            icon.classList.add('bi', 'bi-info-circle', 'text-primary');
    }
    
    // Show toast
    const bsToast = new bootstrap.Toast(toast, {
        autohide: true,
        delay: type === 'error' ? 5000 : 3000
    });
    bsToast.show();
}

// Galaxy sync function
function refreshGalaxy() {
    const syncBtn = document.querySelector('[onclick="refreshGalaxy()"]');
    const originalText = syncBtn.innerHTML;
    
    // Show loading state
    syncBtn.disabled = true;
    syncBtn.innerHTML = '<i class="bi bi-arrow-repeat spin"></i> Syncing...';
    
    // Add spinning animation
    const style = document.createElement('style');
    style.textContent = `
        .spin {
            animation: spin 1s linear infinite;
        }
        @keyframes spin {
            from { transform: rotate(0deg); }
            to { transform: rotate(360deg); }
        }
    `;
    document.head.appendChild(style);
    
    fetch('/api/refresh-galaxy', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        }
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            showToast(data.message, 'success');
            // Refresh the page after a short delay to show updated data
            setTimeout(() => {
                window.location.reload();
            }, 2000);
        } else {
            showToast(data.message, 'error');
        }
    })
    .catch(error => {
        showToast('Network error during sync: ' + error.message, 'error');
    })
    .finally(() => {
        // Restore button state
        syncBtn.disabled = false;
        syncBtn.innerHTML = originalText;
        document.head.removeChild(style);
    });
}

// Page loading animations
document.addEventListener('DOMContentLoaded', function() {
    // Add fade-in animation to main content
    const mainContent = document.querySelector('main');
    if (mainContent) {
        mainContent.classList.add('fade-in-up');
    }
    
    // Add staggered animation to cards
    const cards = document.querySelectorAll('.card');
    cards.forEach((card, index) => {
        card.style.animationDelay = `${index * 0.1}s`;
        card.classList.add('fade-in-up');
    });
    
    // Initialize tooltips if any
    const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });
});

// Navbar active link highlighting
document.addEventListener('DOMContentLoaded', function() {
    const currentPath = window.location.pathname;
    const navLinks = document.querySelectorAll('.navbar-nav .nav-link');
    
    navLinks.forEach(link => {
        if (link.getAttribute('href') === currentPath) {
            link.classList.add('active');
        }
    });
});

// Smooth scrolling for internal links
document.addEventListener('DOMContentLoaded', function() {
    const internalLinks = document.querySelectorAll('a[href^="#"]');
    
    internalLinks.forEach(link => {
        link.addEventListener('click', function(e) {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                target.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            }
        });
    });
});

// Enhanced card hover effects
document.addEventListener('DOMContentLoaded', function() {
    const cards = document.querySelectorAll('.card');
    
    cards.forEach(card => {
        card.addEventListener('mouseenter', function() {
            this.style.transform = 'translateY(-5px) scale(1.02)';
        });
        
        card.addEventListener('mouseleave', function() {
            this.style.transform = 'translateY(0) scale(1)';
        });
    });
});

// Progress bar animation
function animateProgressBar(progressBar, targetWidth) {
    let currentWidth = 0;
    const increment = targetWidth / 50; // 50 steps for smooth animation
    
    const timer = setInterval(() => {
        currentWidth += increment;
        if (currentWidth >= targetWidth) {
            currentWidth = targetWidth;
            clearInterval(timer);
        }
        progressBar.style.width = currentWidth + '%';
    }, 20);
}

// Initialize progress bars on page load
document.addEventListener('DOMContentLoaded', function() {
    const progressBars = document.querySelectorAll('.progress-bar');
    
    progressBars.forEach(bar => {
        const targetWidth = parseFloat(bar.style.width);
        bar.style.width = '0%';
        
        // Start animation after a short delay
        setTimeout(() => {
            animateProgressBar(bar, targetWidth);
        }, 500);
    });
});

// Enhanced button click effects
document.addEventListener('DOMContentLoaded', function() {
    const buttons = document.querySelectorAll('.btn');
    
    buttons.forEach(button => {
        button.addEventListener('click', function(e) {
            // Create ripple effect
            const ripple = document.createElement('span');
            const rect = this.getBoundingClientRect();
            const size = Math.max(rect.width, rect.height);
            const x = e.clientX - rect.left - size / 2;
            const y = e.clientY - rect.top - size / 2;
            
            ripple.style.cssText = `
                position: absolute;
                border-radius: 50%;
                background: rgba(255, 255, 255, 0.3);
                transform: scale(0);
                animation: ripple 0.6s linear;
                width: ${size}px;
                height: ${size}px;
                left: ${x}px;
                top: ${y}px;
                pointer-events: none;
            `;
            
            this.style.position = 'relative';
            this.style.overflow = 'hidden';
            this.appendChild(ripple);
            
            setTimeout(() => {
                ripple.remove();
            }, 600);
        });
    });
    
    // Add ripple animation CSS
    const style = document.createElement('style');
    style.textContent = `
        @keyframes ripple {
            to {
                transform: scale(4);
                opacity: 0;
            }
        }
    `;
    document.head.appendChild(style);
});

// Loading state management
function setLoadingState(element, isLoading) {
    if (isLoading) {
        element.disabled = true;
        element.dataset.originalText = element.innerHTML;
        element.innerHTML = '<i class="bi bi-arrow-repeat spin"></i> Loading...';
    } else {
        element.disabled = false;
        element.innerHTML = element.dataset.originalText || element.innerHTML;
    }
}

// Error handling for images
document.addEventListener('DOMContentLoaded', function() {
    const images = document.querySelectorAll('img');
    
    images.forEach(img => {
        img.addEventListener('error', function() {
            // Hide the image and show placeholder
            this.style.display = 'none';
            const placeholder = this.parentNode.querySelector('.game-image-placeholder');
            if (placeholder) {
                placeholder.style.display = 'flex';
            }
        });
        
        img.addEventListener('load', function() {
            // Show the image and hide placeholder
            this.style.display = 'block';
            const placeholder = this.parentNode.querySelector('.game-image-placeholder');
            if (placeholder) {
                placeholder.style.display = 'none';
            }
        });
    });
});

// Keyboard shortcuts
document.addEventListener('keydown', function(e) {
    // Ctrl/Cmd + R for refresh
    if ((e.ctrlKey || e.metaKey) && e.key === 'r' && e.shiftKey) {
        e.preventDefault();
        refreshGalaxy();
        return;
    }
    
    // / for search focus
    if (e.key === '/' && !e.ctrlKey && !e.metaKey && !e.altKey) {
        const searchInput = document.getElementById('search-input');
        if (searchInput && document.activeElement !== searchInput) {
            e.preventDefault();
            searchInput.focus();
        }
    }
    
    // Escape to clear search
    if (e.key === 'Escape') {
        const searchInput = document.getElementById('search-input');
        if (searchInput && document.activeElement === searchInput) {
            searchInput.blur();
        }
    }
});

// Console welcome message
console.log(`
🎮 Game Manager Web Interface
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Welcome to your gaming collection manager!

Keyboard shortcuts:
• Ctrl+Shift+R - Refresh from Galaxy
• / - Focus search (on search page)
• Esc - Clear search focus

Enjoy managing your games! 🎯
`);

// Analytics and usage tracking (privacy-friendly)
let sessionData = {
    startTime: Date.now(),
    pageViews: 0,
    gamesPickedThisSession: 0,
    searchesThisSession: 0
};

// Track page views
document.addEventListener('DOMContentLoaded', function() {
    sessionData.pageViews++;
});

// Update session data functions (for potential future features)
function trackGamePicked() {
    sessionData.gamesPickedThisSession++;
}

function trackSearch() {
    sessionData.searchesThisSession++;
}

// Cleanup function for when page is unloaded
window.addEventListener('beforeunload', function() {
    // Could be used for saving session data or cleanup
    console.log('Session summary:', sessionData);
}); 