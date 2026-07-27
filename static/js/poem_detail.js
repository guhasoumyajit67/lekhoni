// ============================================
// poem_detail.js - Lekhoni Poem Detail Page
// ============================================

// ============================================
// SHARE BUTTON - Copy Link to Clipboard
// ============================================
function copyShareLink() {
    const url = window.location.href;
    if (navigator.clipboard) {
        navigator.clipboard.writeText(url)
            .then(function() {
                showToast('লিংক কপি করা হয়েছে!', 'success');
            })
            .catch(function() {
                fallbackCopy(url);
            });
    } else {
        fallbackCopy(url);
    }
}

function fallbackCopy(text) {
    const tempInput = document.createElement('input');
    tempInput.value = text;
    document.body.appendChild(tempInput);
    tempInput.select();
    document.execCommand('copy');
    document.body.removeChild(tempInput);
    showToast('লিংক কপি করা হয়েছে!', 'success');
}

// ============================================
// TOAST NOTIFICATION
// ============================================
function showToast(message, type) {
    // Check if toast container exists
    let container = document.getElementById('toast-container');
    if (!container) {
        container = document.createElement('div');
        container.id = 'toast-container';
        container.style.position = 'fixed';
        container.style.bottom = '20px';
        container.style.right = '20px';
        container.style.zIndex = '9999';
        container.style.display = 'flex';
        container.style.flexDirection = 'column';
        container.style.gap = '10px';
        document.body.appendChild(container);
    }

    const toast = document.createElement('div');
    toast.style.padding = '12px 24px';
    toast.style.borderRadius = '8px';
    toast.style.color = 'white';
    toast.style.fontSize = '14px';
    toast.style.fontWeight = '500';
    toast.style.boxShadow = '0 4px 12px rgba(0,0,0,0.15)';
    toast.style.animation = 'slideIn 0.3s ease';
    toast.style.minWidth = '200px';
    toast.style.textAlign = 'center';

    if (type === 'success') {
        toast.style.background = '#2A7F7A';
    } else if (type === 'error') {
        toast.style.background = '#dc3545';
    } else {
        toast.style.background = '#1A1A1A';
    }

    toast.textContent = message;

    // Add slide-in animation
    const style = document.createElement('style');
    style.textContent = `
        @keyframes slideIn {
            from { transform: translateX(100%); opacity: 0; }
            to { transform: translateX(0); opacity: 1; }
        }
        @keyframes slideOut {
            from { transform: translateX(0); opacity: 1; }
            to { transform: translateX(100%); opacity: 0; }
        }
    `;
    document.head.appendChild(style);

    container.appendChild(toast);

    // Auto-remove after 3 seconds
    setTimeout(function() {
        toast.style.animation = 'slideOut 0.3s ease';
        setTimeout(function() {
            toast.remove();
        }, 300);
    }, 3000);
}

// ============================================
// MAIN INITIALIZATION
// ============================================
document.addEventListener('DOMContentLoaded', function() {

    // --------------------------------------------
    // Toggle Comments Section
    // --------------------------------------------
    const toggleBtn = document.getElementById('toggleCommentsBtn');
    const commentsSection = document.getElementById('commentsSection');
    
    if (toggleBtn && commentsSection) {
        toggleBtn.addEventListener('click', function() {
            if (commentsSection.style.display === 'none') {
                commentsSection.style.display = 'block';
                toggleBtn.style.background = '#2A7F7A';
                toggleBtn.style.color = 'white';
                toggleBtn.style.borderColor = '#2A7F7A';
            } else {
                commentsSection.style.display = 'none';
                toggleBtn.style.background = 'transparent';
                toggleBtn.style.color = '';
                toggleBtn.style.borderColor = '';
            }
        });
    }

    // --------------------------------------------
    // Share Button
    // --------------------------------------------
    const shareBtn = document.getElementById('shareBtn');
    if (shareBtn) {
        shareBtn.addEventListener('click', copyShareLink);
    }

    // --------------------------------------------
    // Like Button (AJAX)
    // --------------------------------------------
    const likeButtons = document.querySelectorAll('.like-btn');
    likeButtons.forEach(function(btn) {
        btn.addEventListener('click', function(e) {
            e.preventDefault();
            
            const slug = this.dataset.poemSlug;
            const heartIcon = this.querySelector('i');
            const likeCount = this.querySelector('.like-count');
            const csrfToken = this.dataset.csrf;
            
            if (!csrfToken) {
                console.error('CSRF token not found');
                showToast('লাইক করতে সমস্যা হয়েছে', 'error');
                return;
            }

            // Add loading state
            this.disabled = true;
            this.style.opacity = '0.7';

            fetch('/like/' + slug + '/', {
                method: 'POST',
                headers: {
                    'X-CSRFToken': csrfToken,
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({})
            })
            .then(function(response) {
                if (!response.ok) {
                    throw new Error('Network response was not ok');
                }
                return response.json();
            })
            .then(function(data) {
                if (data.liked) {
                    heartIcon.classList.add('text-danger');
                } else {
                    heartIcon.classList.remove('text-danger');
                }
                likeCount.textContent = data.likes_count;
                showToast(data.liked ? 'পছন্দ করেছেন!' : 'পছন্দ সরিয়েছেন!', 'success');
            })
            .catch(function(error) {
                console.error('Like error:', error);
                showToast('লাইক করতে সমস্যা হয়েছে। আবার চেষ্টা করুন।', 'error');
            })
            .finally(function() {
                // Remove loading state
                btn.disabled = false;
                btn.style.opacity = '1';
            });
        });
    });

    // --------------------------------------------
    // Comment Form - AJAX Submission
    // --------------------------------------------
    const commentForm = document.getElementById('commentForm');
    if (commentForm) {
        commentForm.addEventListener('submit', function(e) {
            e.preventDefault();
            
            const formData = new FormData(this);
            const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;
            const submitBtn = this.querySelector('button[type="submit"]');
            const commentInput = this.querySelector('textarea');
            
            // Show loading state
            submitBtn.disabled = true;
            submitBtn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> পাঠানো হচ্ছে...';
            
            fetch(window.location.href, {
                method: 'POST',
                headers: {
                    'X-CSRFToken': csrfToken,
                },
                body: formData
            })
            .then(function(response) {
                if (response.redirected) {
                    // If redirected, reload the page to show new comment
                    window.location.href = response.url;
                    return;
                }
                return response.text();
            })
            .then(function(data) {
                // Reload page to show new comment
                window.location.reload();
            })
            .catch(function(error) {
                console.error('Comment error:', error);
                showToast('মন্তব্য পাঠাতে সমস্যা হয়েছে।', 'error');
                submitBtn.disabled = false;
                submitBtn.innerHTML = '<i class="fas fa-paper-plane me-1"></i> মন্তব্য পাঠান';
            });
        });
    }
});