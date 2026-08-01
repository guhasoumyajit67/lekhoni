// ============================================
// লেখনী - Main JavaScript (Site-wide)
// ============================================

document.addEventListener('DOMContentLoaded', function() {
    
    // --------------------------------------------
    // Auto-dismiss alerts after 5 seconds
    // --------------------------------------------
    const alerts = document.querySelectorAll('.alert');
    alerts.forEach(function(alert) {
        setTimeout(function() {
            const closeBtn = alert.querySelector('.btn-close');
            if (closeBtn) {
                closeBtn.click();
            }
        }, 5000);
    });

    // --------------------------------------------
    // Active navigation link highlighting
    // --------------------------------------------
    const currentPath = window.location.pathname;
    document.querySelectorAll('.navbar-nav .nav-link').forEach(function(link) {
        const href = link.getAttribute('href');
        if (href && href !== '#' && currentPath === href) {
            link.classList.add('active');
            link.setAttribute('aria-current', 'page');
        }
    });
});