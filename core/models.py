from django.db import models
from django.core.validators import RegexValidator
from ckeditor.fields import RichTextField

class SiteSettings(models.Model):
    """Model to store site-wide settings"""
    site_title = models.CharField(max_length=100, default="My Portfolio")
    meta_description = models.TextField(max_length=160, blank=True)
    meta_keywords = models.CharField(max_length=255, blank=True)
    site_logo = models.ImageField(upload_to='site/', blank=True)
    favicon = models.ImageField(upload_to='site/', blank=True)
    
    # Social Media Links
    github = models.URLField(blank=True)
    linkedin = models.URLField(blank=True)
    twitter = models.URLField(blank=True)
    instagram = models.URLField(blank=True)
    facebook = models.URLField(blank=True)
    
    # Contact Information
    email = models.EmailField(blank=True)
    phone_regex = RegexValidator(
        regex=r'^\+?1?\d{9,15}$',
        message="Phone number must be entered in format: '+999999999'. Up to 15 digits allowed."
    )
    phone = models.CharField(validators=[phone_regex], max_length=17, blank=True)
    address = models.TextField(blank=True)
    
    # Resume/CV
    resume = models.FileField(upload_to='resume/', blank=True)
    
    # Footer
    footer_text = models.CharField(max_length=255, default="© 2025 All Rights Reserved")
    
    class Meta:
        verbose_name = "Site Settings"
        verbose_name_plural = "Site Settings"
    
    def __str__(self):
        return self.site_title
    
    def save(self, *args, **kwargs):
        """Make sure there's only one instance of SiteSettings"""
        if SiteSettings.objects.exists() and not self.pk:
            raise ValueError("There can only be one SiteSettings instance")
        return super().save(*args, **kwargs)

class About(models.Model):
    """Model to store About section information"""
    title = models.CharField(max_length=100, default="About Me")
    subtitle = models.CharField(max_length=200, blank=True)
    profile_image = models.ImageField(upload_to='about/')
    content = RichTextField()
    resume = models.FileField(upload_to='resume/', blank=True)
    
    # Professional information
    years_experience = models.PositiveIntegerField(default=0)
    clients_count = models.PositiveIntegerField(default=0)
    projects_count = models.PositiveIntegerField(default=0)
    
    class Meta:
        verbose_name = "About"
        verbose_name_plural = "About"
    
    def __str__(self):
        return self.title

class Education(models.Model):
    """Model to store education information"""
    degree = models.CharField(max_length=100)
    institution = models.CharField(max_length=100)
    location = models.CharField(max_length=100)
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)
    is_current = models.BooleanField(default=False)
    description = models.TextField(blank=True)
    order = models.PositiveIntegerField(default=0)
    
    class Meta:
        ordering = ['-end_date', '-is_current', 'order']
        verbose_name = "Education"
        verbose_name_plural = "Education"
    
    def __str__(self):
        return f"{self.degree} - {self.institution}"

class Experience(models.Model):
    """Model to store work experience"""
    position = models.CharField(max_length=100)
    company = models.CharField(max_length=100)
    location = models.CharField(max_length=100)
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)
    is_current = models.BooleanField(default=False)
    description = RichTextField()
    order = models.PositiveIntegerField(default=0)
    
    class Meta:
        ordering = ['-end_date', '-is_current', 'order']
        verbose_name = "Experience"
        verbose_name_plural = "Experience"
    
    def __str__(self):
        return f"{self.position} at {self.company}"

class Service(models.Model):
    """Model to store services offered"""
    title = models.CharField(max_length=100)
    icon = models.CharField(max_length=50, help_text="Font Awesome or other icon class")
    description = models.TextField()
    order = models.PositiveIntegerField(default=0)
    
    class Meta:
        ordering = ['order']
        verbose_name = "Service"
        verbose_name_plural = "Services"
    
    def __str__(self):
        return self.title

class Testimonial(models.Model):
    """Model to store client testimonials"""
    name = models.CharField(max_length=100)
    position = models.CharField(max_length=100)
    company = models.CharField(max_length=100, blank=True)
    image = models.ImageField(upload_to='testimonials/', blank=True)
    content = models.TextField()
    rating = models.PositiveIntegerField(default=5, choices=[(i, i) for i in range(1, 6)])
    order = models.PositiveIntegerField(default=0)
    
    class Meta:
        ordering = ['order']
        verbose_name = "Testimonial"
        verbose_name_plural = "Testimonials"
    
    def __str__(self):
        return f"Testimonial from {self.name}"

class Contact(models.Model):
    """Model to store contact form submissions"""
    name = models.CharField(max_length=100)
    email = models.EmailField()
    subject = models.CharField(max_length=200)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = "Contact"
        verbose_name_plural = "Contacts"
    
    def __str__(self):
        return f"Message from {self.name} - {self.subject}"

class Skill(models.Model):
    """Model to store skills"""
    CATEGORY_CHOICES = [
        ('programming', 'Programming Languages'),
        ('framework', 'Frameworks & Libraries'),
        ('database', 'Databases'),
        ('tool', 'Tools & Technologies'),
        ('language', 'Languages'),
        ('soft', 'Soft Skills'),
        ('other', 'Other'),
    ]
    
    name = models.CharField(max_length=100)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    level = models.PositiveIntegerField(default=80, help_text="Proficiency level (0-100)")
    icon = models.CharField(max_length=50, blank=True, help_text="Optional icon class")
    order = models.PositiveIntegerField(default=0)
    
    class Meta:
        ordering = ['category', 'order']
        verbose_name = "Skill"
        verbose_name_plural = "Skills"
    
    def __str__(self):
        return self.name