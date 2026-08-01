// ============================================
// home.js - Lekhoni Homepage JavaScript
// ============================================

document.addEventListener('DOMContentLoaded', function() {
    
    // --------------------------------------------
    // 1. Handle "See More" or specific homepage interactions
    // --------------------------------------------
    console.log("Homepage loaded successfully.");

    // --------------------------------------------
    // 2. Hover Lift Animation Enhancement
    // --------------------------------------------
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
    // 3. Fix Bengali Numerals on the Homepage
    // --------------------------------------------
    function updateHomeBengaliNumbers() {
        document.querySelectorAll('.like-count, .view-count, .comment-count, .poem-count').forEach(function(el) {
            const text = el.textContent.trim();
            if (/^\d+$/.test(text)) {
                el.style.fontFamily = "'Noto Serif Bengali', 'Hind Siliguri', sans-serif";
                el.style.fontFeatureSettings = "'tnum'";
            }
        });
    }
    updateHomeBengaliNumbers();

    // --------------------------------------------
    // 4. REMOVED SEARCH JS - Handled natively by HTML onclick
    // --------------------------------------------
    console.log("✅ Search handled natively by HTML.");
});