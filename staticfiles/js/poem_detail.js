// ============================================
// poem_detail.js - Lekhoni Poem Detail Page
// ============================================

// ============================================
// BENGALI NUMERAL CONVERTER
// ============================================
function toBengaliNumber(value) {
    const bengaliDigits = {
        '0': '০', '1': '১', '2': '২', '3': '৩', '4': '৪',
        '5': '৫', '6': '৬', '7': '৭', '8': '৮', '9': '৯'
    };
    
    // Convert to string and handle potential null/undefined
    let strValue = String(value || '0');
    
    // Remove any non-digit characters (like commas, spaces, etc.)
    strValue = strValue.replace(/[^\d]/g, '');
    
    // If empty after cleaning, return '০'
    if (strValue === '') {
        return '০';
    }
    
    // Replace each digit with Bengali numeral
    return strValue.replace(/\d/g, function(digit) {
        return bengaliDigits[digit] || digit;
    });
}

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

    setTimeout(function() {
        toast.style.animation = 'slideOut 0.3s ease';
        setTimeout(function() {
            toast.remove();
        }, 300);
    }, 3000);
}

// ============================================
// UPDATE BENGALI NUMBERS ON PAGE LOAD
// ============================================
function updateAllBengaliNumbers() {
    // Update like counts
    document.querySelectorAll('.like-count').forEach(function(element) {
        const currentText = element.textContent.trim();
        // Only convert if it's a number
        if (/^\d+$/.test(currentText)) {
            element.textContent = toBengaliNumber(currentText);
            // Apply consistent style
            element.style.fontFamily = "'Noto Serif Bengali', 'Hind Siliguri', sans-serif";
            element.style.fontFeatureSettings = "'tnum'";
            element.style.fontWeight = "600";
        }
    });
    
    // Update view counts
    document.querySelectorAll('.view-count, .views-count').forEach(function(element) {
        const currentText = element.textContent.trim();
        if (/^\d+$/.test(currentText)) {
            element.textContent = toBengaliNumber(currentText);
            // Apply consistent style
            element.style.fontFamily = "'Noto Serif Bengali', 'Hind Siliguri', sans-serif";
            element.style.fontFeatureSettings = "'tnum'";
            element.style.fontWeight = "600";
        }
    });
    
    // Update comment counts
    document.querySelectorAll('.comment-count, .comments-count, #commentCountDisplay, #commentCount').forEach(function(element) {
        const currentText = element.textContent.trim();
        if (/^\d+$/.test(currentText)) {
            element.textContent = toBengaliNumber(currentText);
            // Apply consistent style
            element.style.fontFamily = "'Noto Serif Bengali', 'Hind Siliguri', sans-serif";
            element.style.fontFeatureSettings = "'tnum'";
            element.style.fontWeight = "600";
        }
    });
}

// ============================================
// FIX: Ensure like count stays in Bengali
// ============================================
function updateLikeCount(element, count) {
    // Directly set the text content to Bengali numerals
    element.textContent = toBengaliNumber(count);
    // Apply consistent style
    element.style.fontFamily = "'Noto Serif Bengali', 'Hind Siliguri', sans-serif";
    element.style.fontFeatureSettings = "'tnum'";
    element.style.fontWeight = "600";
    
    // Also update any other elements that might display the same count
    document.querySelectorAll('.like-count, #likeCount, .like-counter').forEach(function(el) {
        if (el !== element) {
            el.textContent = toBengaliNumber(count);
            el.style.fontFamily = "'Noto Serif Bengali', 'Hind Siliguri', sans-serif";
            el.style.fontFeatureSettings = "'tnum'";
            el.style.fontWeight = "600";
        }
    });
}

// ============================================
// MAIN INITIALIZATION
// ============================================
document.addEventListener('DOMContentLoaded', function() {

    // Update all Bengali numbers on page load
    updateAllBengaliNumbers();

    // --------------------------------------------
    // Share Button
    // --------------------------------------------
    const shareBtn = document.getElementById('shareBtn');
    if (shareBtn) {
        shareBtn.addEventListener('click', copyShareLink);
    }

    // --------------------------------------------
    // Like Button (AJAX) - FIXED VERSION
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

            // Get current count to preserve it if needed
            const currentCount = likeCount.textContent.trim();
            
            // Disable button to prevent double-click
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
                // Update heart icon
                if (data.liked) {
                    heartIcon.classList.add('text-danger');
                } else {
                    heartIcon.classList.remove('text-danger');
                }
                
                // CRITICAL FIX: Always use Bengali numerals
                let likesValue = data.likes_count;
                if (typeof likesValue === 'string') {
                    likesValue = parseInt(likesValue.replace(/[^\d]/g, '')) || 0;
                }
                
                // Update the like count with Bengali numeral and maintain style
                likeCount.textContent = toBengaliNumber(likesValue);
                // Ensure consistent style
                likeCount.style.fontFamily = "'Noto Serif Bengali', 'Hind Siliguri', sans-serif";
                likeCount.style.fontFeatureSettings = "'tnum'";
                likeCount.style.fontWeight = "600";
                
                // Also update any other like count displays on the page
                document.querySelectorAll('.like-count, #likeCount, .like-counter, [data-like-count]').forEach(function(el) {
                    if (el !== likeCount) {
                        el.textContent = toBengaliNumber(likesValue);
                        el.style.fontFamily = "'Noto Serif Bengali', 'Hind Siliguri', sans-serif";
                        el.style.fontFeatureSettings = "'tnum'";
                        el.style.fontWeight = "600";
                    }
                });
                
                showToast(data.liked ? 'পছন্দ করেছেন!' : 'পছন্দ সরিয়েছেন!', 'success');
            })
            .catch(function(error) {
                console.error('Like error:', error);
                // Restore the previous count if there's an error
                if (likeCount && currentCount) {
                    likeCount.textContent = currentCount;
                }
                showToast('লাইক করতে সমস্যা হয়েছে। আবার চেষ্টা করুন।', 'error');
            })
            .finally(function() {
                // Re-enable button
                btn.disabled = false;
                btn.style.opacity = '1';
            });
        });
    });

    // --------------------------------------------
    // Comment Form - AJAX Submission (No Reload)
    // --------------------------------------------
    const commentForm = document.getElementById('commentForm');
    if (commentForm) {
        commentForm.addEventListener('submit', function(e) {
            e.preventDefault();
            
            const formData = new FormData(this);
            const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;
            const submitBtn = this.querySelector('button[type="submit"]');
            const commentInput = this.querySelector('textarea');
            const commentsList = document.getElementById('commentsList');
            const commentCount = document.getElementById('commentCountDisplay');
            const commentCountBtn = document.getElementById('commentCount');
            
            // Validate comment
            const commentText = commentInput.value.trim();
            if (!commentText) {
                showToast('অনুগ্রহ করে মন্তব্য লিখুন।', 'error');
                return;
            }
            
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
                return response.text();
            })
            .then(function(html) {
                // Parse the response HTML
                const parser = new DOMParser();
                const doc = parser.parseFromString(html, 'text/html');
                
                // Update comments list
                const newCommentsList = doc.getElementById('commentsList');
                if (newCommentsList && commentsList) {
                    commentsList.innerHTML = newCommentsList.innerHTML;
                }
                
                // Update comment count
                const newCommentCount = doc.getElementById('commentCountDisplay');
                if (newCommentCount && commentCount) {
                    // Extract and convert the number to Bengali
                    const countText = newCommentCount.textContent.trim();
                    const countNumber = parseInt(countText.replace(/[^\d]/g, '')) || 0;
                    commentCount.textContent = toBengaliNumber(countNumber);
                    commentCount.style.fontFamily = "'Noto Serif Bengali', 'Hind Siliguri', sans-serif";
                    commentCount.style.fontFeatureSettings = "'tnum'";
                    commentCount.style.fontWeight = "600";
                    
                    if (commentCountBtn) {
                        commentCountBtn.textContent = toBengaliNumber(countNumber);
                        commentCountBtn.style.fontFamily = "'Noto Serif Bengali', 'Hind Siliguri', sans-serif";
                        commentCountBtn.style.fontFeatureSettings = "'tnum'";
                        commentCountBtn.style.fontWeight = "600";
                    }
                }
                
                // Clear the textarea
                commentInput.value = '';
                showToast('মন্তব্য সফলভাবে যোগ হয়েছে!', 'success');
            })
            .catch(function(error) {
                console.error('Comment error:', error);
                showToast('মন্তব্য পাঠাতে সমস্যা হয়েছে।', 'error');
            })
            .finally(function() {
                submitBtn.disabled = false;
                submitBtn.innerHTML = '<i class="fas fa-paper-plane me-1"></i> মন্তব্য পাঠান';
            });
        });
    }
});

// ============================================
// MutationObserver to watch for dynamic content
// ============================================
const observer = new MutationObserver(function(mutations) {
    mutations.forEach(function(mutation) {
        if (mutation.type === 'childList') {
            mutation.addedNodes.forEach(function(node) {
                if (node.nodeType === 1) {
                    // Check for any elements that might contain numbers
                    const numberElements = node.querySelectorAll('.like-count, .view-count, .views-count, .comment-count, .comments-count, #commentCountDisplay, #commentCount');
                    numberElements.forEach(function(el) {
                        const text = el.textContent.trim();
                        if (/^\d+$/.test(text)) {
                            el.textContent = toBengaliNumber(text);
                            el.style.fontFamily = "'Noto Serif Bengali', 'Hind Siliguri', sans-serif";
                            el.style.fontFeatureSettings = "'tnum'";
                            el.style.fontWeight = "600";
                        }
                    });
                    
                    // Also check the node itself
                    if (node.classList && (
                        node.classList.contains('like-count') || 
                        node.classList.contains('view-count') || 
                        node.classList.contains('views-count') || 
                        node.classList.contains('comment-count') || 
                        node.classList.contains('comments-count')
                    )) {
                        const text = node.textContent.trim();
                        if (/^\d+$/.test(text)) {
                            node.textContent = toBengaliNumber(text);
                            node.style.fontFamily = "'Noto Serif Bengali', 'Hind Siliguri', sans-serif";
                            node.style.fontFeatureSettings = "'tnum'";
                            node.style.fontWeight = "600";
                        }
                    }
                }
            });
        }
    });
});

// Start observing
observer.observe(document.body, {
    childList: true,
    subtree: true
});