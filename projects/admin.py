from django.contrib import admin
from .models import Category, Technology, Project, ProjectImage

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ('name',)

@admin.register(Technology)
class TechnologyAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'icon')
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ('name',)

class ProjectImageInline(admin.TabularInline):
    model = ProjectImage
    extra = 1

@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'completion_date', 'featured', 'order')
    list_filter = ('category', 'technologies', 'featured')
    prepopulated_fields = {'slug': ('title',)}
    search_fields = ('title', 'summary', 'description')
    date_hierarchy = 'completion_date'
    filter_horizontal = ('technologies',)
    inlines = [ProjectImageInline]
    fieldsets = (
        ('Project Information', {
            'fields': ('title', 'slug', 'summary', 'description', 'thumbnail')
        }),
        ('Classification', {
            'fields': ('category', 'technologies')
        }),
        ('Links', {
            'fields': ('github_link', 'live_link')
        }),
        ('Display Settings', {
            'fields': ('featured', 'completion_date', 'order')
        }),
    )