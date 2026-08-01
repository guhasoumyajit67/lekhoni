// ============================================
// search.js - Infinite Scroll for Search Results
// ============================================

document.addEventListener('DOMContentLoaded', function() {
    const loadMoreBtn = document.getElementById('load-more-btn');
    const loadMoreWrapper = document.getElementById('load-more-wrapper');
    const poemContainer = document.getElementById('poem-container');
    
    if (!loadMoreBtn) return;

    // Get the current search query from the URL
    const urlParams = new URLSearchParams(window.location.search);
    const query = urlParams.get('q');
    
    let currentPage = 2;

    loadMoreBtn.addEventListener('click', function() {
        loadMoreBtn.disabled = true;
        loadMoreBtn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> লোড হচ্ছে...';

        // Fetch next page with the search query preserved
        fetch(`/search/load-more/?q=${query}&page=${currentPage}`)
        .then(response => response.json())
        .then(data => {
            if (data.html) {
                poemContainer.insertAdjacentHTML('beforeend', data.html);
                currentPage++;
            }
            
            if (data.has_next) {
                loadMoreBtn.disabled = false;
                loadMoreBtn.innerHTML = '<i class="fas fa-plus-circle me-2"></i> আরও লোড করুন';
            } else {
                loadMoreWrapper.innerHTML = '<p class="text-muted">সব কবিতা লোড করা হয়েছে!</p>';
            }
        })
        .catch(error => {
            console.error('Error loading search results:', error);
            loadMoreBtn.disabled = false;
            loadMoreBtn.innerHTML = '<i class="fas fa-plus-circle me-2"></i> আরও লোড করুন';
            alert('লোড করতে সমস্যা হয়েছে। আবার চেষ্টা করুন।');
        });
    });
});