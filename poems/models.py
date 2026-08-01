from django.db import models
from django.conf import settings
from django.utils import timezone
from django.urls import reverse
from django.utils.text import slugify


class Category(models.Model):
    """Poetry category model"""
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True, blank=True)
    description = models.TextField(blank=True)
    icon = models.CharField(max_length=50, blank=True)

    class Meta:
        verbose_name_plural = "Categories"
        ordering = ['name']

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('category_detail', args=[self.slug])

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class Poem(models.Model):
    """Main Poem model"""
    
    # Core fields
    title = models.CharField(max_length=255)
    slug = models.SlugField(unique=True, max_length=255, blank=True)
    content = models.TextField()
    
    # Author
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='poems'
    )
    
    # Category
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='poems'
    )
    
    # Publication (auto-published)
    is_published = models.BooleanField(default=True)
    is_featured = models.BooleanField(default=False)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    published_at = models.DateTimeField(default=timezone.now)
    
    # Analytics
    views = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['-published_at']
        indexes = [
            models.Index(fields=['-published_at']),
            models.Index(fields=['author']),
            models.Index(fields=['category']),
        ]

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('poem_detail', args=[self.slug])

    def save(self, *args, **kwargs):
        # Auto-generate unique slug
        if not self.slug:
            base_slug = slugify(self.title)
            slug = base_slug
            counter = 1
            # Keep checking until we find a unique slug
            while Poem.objects.filter(slug=slug).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            self.slug = slug
        
        # Auto-publish all poems
        self.is_published = True
        
        super().save(*args, **kwargs)

    def increment_views(self):
        self.views += 1
        self.save(update_fields=['views'])


class Comment(models.Model):
    """Comment model for poems"""
    poem = models.ForeignKey(Poem, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='comments'
    )
    content = models.TextField()
    is_approved = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['created_at']

    def __str__(self):
        return f"Comment by {self.author.username} on {self.poem.title}"


class Like(models.Model):
    """Like model for poems"""
    poem = models.ForeignKey(Poem, on_delete=models.CASCADE, related_name='likes')
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='likes'
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('poem', 'user')

    def __str__(self):
        return f"{self.user.username} likes {self.poem.title}"