from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    """
    Custom User model extending Django's AbstractUser.
    Add custom fields here as needed.
    """
    
    # Optional: Add custom fields for future use
    # bio = models.TextField(max_length=500, blank=True)
    # profile_picture = models.ImageField(upload_to='profiles/', blank=True, null=True)
    # website = models.URLField(blank=True)
    # phone_number = models.CharField(max_length=15, blank=True)
    # location = models.CharField(max_length=100, blank=True)
    # date_of_birth = models.DateField(blank=True, null=True)
    
    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'
        ordering = ['username']

    def __str__(self):
        return self.username
    
    def get_full_name(self):
        """Return the full name of the user."""
        if self.first_name and self.last_name:
            return f"{self.first_name} {self.last_name}"
        return self.username
    
    @property
    def poem_count(self):
        """Return the number of poems written by the user."""
        return self.poems.filter(is_published=True).count()
    
    @property
    def total_views(self):
        """Return the total views of all poems by the user."""
        return sum(poem.views for poem in self.poems.all())