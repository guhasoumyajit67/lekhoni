from django.contrib import admin
from .models import Category, Tag, Poem, Comment, Like


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'created_at']
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ['name', 'description']


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'created_at']
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ['name']


@admin.register(Poem)
class PoemAdmin(admin.ModelAdmin):
    list_display = ['title', 'category', 'author', 'is_published', 'is_featured', 'views', 'published_at']
    list_filter = ['category', 'tags', 'is_published', 'is_featured', 'created_at']
    search_fields = ['title', 'content', 'pen_note', 'author__username']
    prepopulated_fields = {'slug': ('title',)}
    readonly_fields = ['views', 'created_at', 'updated_at']
    filter_horizontal = ['tags']

    fieldsets = (
        ('Title & Content', {
            'fields': ('title', 'slug', 'content', 'english_translation', 'author')
        }),
        ('Category & Tags', {
            'fields': ('category', 'tags')
        }),
        ('Lekhoni\'s Note', {
            'fields': ('pen_note',)
        }),
        ('Media', {
            'fields': ('featured_image', 'audio_file')
        }),
        ('Publication', {
            'fields': ('is_published', 'is_featured', 'published_at')
        }),
        ('SEO', {
            'fields': ('meta_description', 'meta_keywords')
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