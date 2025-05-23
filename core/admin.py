from django.contrib import admin
from .models import (
    SiteSettings, About, Education, Experience, 
    Service, Testimonial, Contact, Skill
)

@admin.register(SiteSettings)
class SiteSettingsAdmin(admin.ModelAdmin):
    fieldsets = (
        ('Site Information', {
            'fields': ('site_title', 'meta_description', 'meta_keywords', 'site_logo', 'favicon')
        }),
        ('Social Media', {
            'fields': ('github', 'linkedin', 'twitter', 'instagram', 'facebook')
        }),
        ('Contact Information', {
            'fields': ('email', 'phone', 'address')
        }),
        ('Resume', {
            'fields': ('resume',)
        }),
        ('Footer', {
            'fields': ('footer_text',)
        }),
    )
    
    def has_add_permission(self, request):
        # Check if there's already an instance
        if SiteSettings.objects.exists():
            return False
        return super().has_add_permission(request)

@admin.register(About)
class AboutAdmin(admin.ModelAdmin):
    fieldsets = (
        ('About Information', {
            'fields': ('title', 'subtitle', 'profile_image', 'content', 'resume')
        }),
        ('Professional Stats', {
            'fields': ('years_experience', 'clients_count', 'projects_count')
        }),
    )
    
    def has_add_permission(self, request):
        # Check if there's already an instance
        if About.objects.exists():
            return False
        return super().has_add_permission(request)

@admin.register(Education)
class EducationAdmin(admin.ModelAdmin):
    list_display = ('degree', 'institution', 'start_date', 'end_date', 'is_current', 'order')
    list_filter = ('is_current',)
    search_fields = ('degree', 'institution')
    fieldsets = (
        ('Education Details', {
            'fields': ('degree', 'institution', 'location')
        }),
        ('Time Period', {
            'fields': ('start_date', 'end_date', 'is_current')
        }),
        ('Additional Information', {
            'fields': ('description', 'order')
        }),
    )

@admin.register(Experience)
class ExperienceAdmin(admin.ModelAdmin):
    list_display = ('position', 'company', 'start_date', 'end_date', 'is_current', 'order')
    list_filter = ('is_current',)
    search_fields = ('position', 'company')
    fieldsets = (
        ('Job Details', {
            'fields': ('position', 'company', 'location')
        }),
        ('Time Period', {
            'fields': ('start_date', 'end_date', 'is_current')
        }),
        ('Additional Information', {
            'fields': ('description', 'order')
        }),
    )

@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ('title', 'order')
    search_fields = ('title', 'description')
    fieldsets = (
        ('Service Details', {
            'fields': ('title', 'icon', 'description', 'order')
        }),
    )

@admin.register(Testimonial)
class TestimonialAdmin(admin.ModelAdmin):
    list_display = ('name', 'position', 'company', 'rating', 'order')
    list_filter = ('rating',)
    search_fields = ('name', 'company', 'content')
    fieldsets = (
        ('Client Information', {
            'fields': ('name', 'position', 'company', 'image')
        }),
        ('Testimonial Content', {
            'fields': ('content', 'rating', 'order')
        }),
    )

@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'subject', 'created_at', 'is_read')
    list_filter = ('is_read', 'created_at')
    search_fields = ('name', 'email', 'subject', 'message')
    readonly_fields = ('name', 'email', 'subject', 'message', 'created_at')
    fieldsets = (
        ('Contact Information', {
            'fields': ('name', 'email')
        }),
        ('Message', {
            'fields': ('subject', 'message', 'created_at')
        }),
        ('Status', {
            'fields': ('is_read',)
        }),
    )
    
    def has_add_permission(self, request):
        return False

@admin.register(Skill)
class SkillAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'level', 'order')
    list_filter = ('category',)
    search_fields = ('name',)
    fieldsets = (
        ('Skill Details', {
            'fields': ('name', 'category', 'level', 'icon', 'order')
        }),
    )