// ============================================
// my_poems.js - Infinite Scroll for My Poems Dashboard
// ============================================

document.addEventListener('DOMContentLoaded', function() {
    const loadMoreBtn = document.getElementById('load-more-btn');
    const loadMoreWrapper = document.getElementById('load-more-wrapper');
    const poemContainer = document.getElementById('poem-container');
    
    // Track which page we are currently on
    let currentPage = 2;

    // If the button doesn't exist on this page, stop the script
    if (!loadMoreBtn) return;

    loadMoreBtn.addEventListener('click', function() {
        // Disable button and show loading spinner
        loadMoreBtn.disabled = true;
        loadMoreBtn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> লোড হচ্ছে...';

        // Fetch the next batch of poems from the My Poems API endpoint
        fetch(`/my-poems/load-more/?page=${currentPage}`)
        .then(response => response.json())
        .then(data => {
            if (data.html) {
                // Append the new poems to the bottom of the container
                poemContainer.insertAdjacentHTML('beforeend', data.html);
                currentPage++; // Increment page counter for next click
            }
            
            if (data.has_next) {
                // If there are more poems, re-enable the button
                loadMoreBtn.disabled = false;
                loadMoreBtn.innerHTML = '<i class="fas fa-plus-circle me-2"></i> আরও লোড করুন';
            } else {
                // If no more poems, replace button with a message
                loadMoreWrapper.innerHTML = '<p class="text-muted">সব কবিতা লোড করা হয়েছে!</p>';
            }
        })
        .catch(error => {
            console.error('Error loading poems:', error);
            loadMoreBtn.disabled = false;
            loadMoreBtn.innerHTML = '<i class="fas fa-plus-circle me-2"></i> আরও লোড করুন';
            alert('লোড করতে সমস্যা হয়েছে। আবার চেষ্টা করুন।');
        });
    });
});