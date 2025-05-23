from django.contrib import admin
from .models import Category, Tag, Post, Comment

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ('name',)

@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ('name',)

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'category', 'status', 'featured', 'published_date')
    list_filter = ('status', 'category', 'featured', 'author')
    search_fields = ('title', 'summary', 'content')
    prepopulated_fields = {'slug': ('title',)}
    raw_id_fields = ('author',)
    date_hierarchy = 'published_date'
    filter_horizontal = ('tags',)
    fieldsets = (
        ('Post Information', {
            'fields': ('title', 'slug', 'author', 'category', 'tags')
        }),
        ('Content', {
            'fields': ('featured_image', 'summary', 'content')
        }),
        ('Publication', {
            'fields': ('status', 'featured', 'published_date')
        }),
    )

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('name', 'post', 'created_at', 'is_approved')
    list_filter = ('is_approved', 'created_at')
    search_fields = ('name', 'email', 'content')
    actions = ['approve_comments']
    
    def approve_comments(self, request, queryset):
        queryset.update(is_approved=True)
    approve_comments.short_description = "Approve selected comments"