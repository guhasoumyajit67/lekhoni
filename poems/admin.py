from django.contrib import admin
from .models import Category, Poem, Comment, Like  # ← Remove 'Tag' from import


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ['name', 'description']


@admin.register(Poem)
class PoemAdmin(admin.ModelAdmin):
    list_display = ['title', 'category', 'author', 'views', 'published_at']
    list_filter = ['category', 'created_at']
    search_fields = ['title', 'content', 'author__username']
    prepopulated_fields = {'slug': ('title',)}
    readonly_fields = ['views', 'created_at', 'updated_at']

    fieldsets = (
        ('Title & Content', {
            'fields': ('title', 'slug', 'content', 'author')
        }),
        ('Category', {
            'fields': ('category',)
        }),
        ('Media', {
            'fields': ('featured_image', 'audio_file')
        }),
        ('Publication', {
            'fields': ('is_published', 'is_featured', 'published_at')
        }),
        ('Analytics', {
            'fields': ('views', 'created_at', 'updated_at')
        }),
    )


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['author', 'poem', 'is_approved', 'created_at']
    list_filter = ['is_approved', 'created_at']
    list_editable = ['is_approved']
    search_fields = ['author__username', 'content']


@admin.register(Like)
class LikeAdmin(admin.ModelAdmin):
    list_display = ['user', 'poem', 'created_at']
    list_filter = ['created_at']
    search_fields = ['user__username', 'poem__title']