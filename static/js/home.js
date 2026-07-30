// ============================================
// home.js - Lekhoni Homepage JavaScript
// ============================================

document.addEventListener('DOMContentLoaded', function() {
    
    // --------------------------------------------
    // 1. Handle "See More" or specific homepage interactions
    // --------------------------------------------
    // (If you don't have a 'See More' button, this is a placeholder for future features)
    console.log("Homepage loaded successfully.");

    // --------------------------------------------
    // 2. Hover Lift Animation Enhancement
    // --------------------------------------------
    // Add a smooth scale transition to all cards
    const cards = document.querySelectorAll('.hover-lift');
    cards.forEach(function(card) {
        card.addEventListener('mouseenter', function() {
            this.style.transform = 'translateY(-6px)';
            this.style.boxShadow = '0 8px 25px rgba(0,0,0,0.12)';
            this.style.transition = 'all 0.3s cubic-bezier(0.25, 0.46, 0.45, 0.94)';
        });
        
        card.addEventListener('mouseleave', function() {
            this.style.transform = 'translateY(0)';
            this.style.boxShadow = '0 .125rem .25rem rgba(0,0,0,.075)';
            this.style.transition = 'all 0.3s cubic-bezier(0.25, 0.46, 0.45, 0.94)';
        });
    });

    // --------------------------------------------
    // 3. Fix Bengali Numerals on the Homepage (Crucial!)
    // --------------------------------------------
    // The template uses |bengali_num, but sometimes AJAX or dynamic content 
    // might load with standard numbers. This ensures they look right.
    function updateHomeBengaliNumbers() {
        document.querySelectorAll('.like-count, .view-count, .comment-count, .poem-count').forEach(function(el) {
            // Only modify if it's just a plain number (not already converted)
            const text = el.textContent.trim();
            if (/^\d+$/.test(text)) {
                // We won't override Django's template tag here, but we ensure font consistency
                el.style.fontFamily = "'Noto Serif Bengali', 'Hind Siliguri', sans-serif";
                el.style.fontFeatureSettings = "'tnum'";
            }
        });
    }
    updateHomeBengaliNumbers();
});