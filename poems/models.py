from django.db import models
from django.conf import settings
from django.utils import timezone
from django.urls import reverse
from django.utils.text import slugify


class Category(models.Model):
    """Poetry category model"""
    name = models.CharField(max_length=100, help_text="Category name in Bengali")
    slug = models.SlugField(unique=True, blank=True, help_text="URL-friendly version")
    description = models.TextField(blank=True, help_text="Brief category description")
    icon = models.CharField(max_length=50, blank=True, help_text="Font Awesome icon class")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = "Categories"
        ordering = ['name']

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('poems:category_detail', args=[self.slug])

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class Tag(models.Model):
    """Poetry tag model"""
    name = models.CharField(max_length=50, help_text="Tag name in Bengali")
    slug = models.SlugField(unique=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('poems:tag_detail', args=[self.slug])

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class Poem(models.Model):
    """Main Poem model"""
    
    # Core fields
    title = models.CharField(max_length=255, help_text="Poem title in Bengali")
    slug = models.SlugField(unique=True, max_length=255, blank=True)
    content = models.TextField(help_text="The poem content")
    english_translation = models.TextField(blank=True, help_text="Optional English translation")
    
    # Author
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='poems'
    )
    
    # Category & Tags
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='poems'
    )
    tags = models.ManyToManyField(Tag, blank=True, related_name='poems')
    
    # "Lekhoni's Note" - Writer's inspiration
    pen_note = models.TextField(
        blank=True,
        help_text="লেখনীর কথা - Your inspiration behind this poem"
    )
    
    # Media (future use)
    featured_image = models.ImageField(
        upload_to='poem_images/',
        blank=True,
        null=True,
        help_text="Cover image for the poem"
    )
    audio_file = models.FileField(
        upload_to='poem_audio/',
        blank=True,
        null=True,
        help_text="Audio recitation (MP3 format)"
    )
    
    # Publication status
    is_published = models.BooleanField(default=False, help_text="Publish this poem")
    is_featured = models.BooleanField(default=False, help_text="Feature on homepage")
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    published_at = models.DateTimeField(default=timezone.now)
    
    # SEO
    meta_description = models.CharField(max_length=160, blank=True)
    meta_keywords = models.CharField(max_length=255, blank=True)
    
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
        return reverse('poems:poem_detail', args=[self.slug])

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        if self.is_published and not self.published_at:
            self.published_at = timezone.now()
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