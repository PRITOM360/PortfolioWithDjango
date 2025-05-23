from django.db import models
from django.utils.text import slugify
from ckeditor.fields import RichTextField

class Category(models.Model):
    """Model for project categories"""
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True, blank=True)
    
    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories"
        ordering = ['name']
    
    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

class Technology(models.Model):
    """Model for technologies used in projects"""
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True, blank=True)
    icon = models.CharField(max_length=50, blank=True, help_text="Optional icon class")
    
    class Meta:
        verbose_name = "Technology"
        verbose_name_plural = "Technologies"
        ordering = ['name']
    
    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

class Project(models.Model):
    """Model for portfolio projects"""
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, blank=True)
    summary = models.TextField(max_length=300)
    description = RichTextField()
    thumbnail = models.ImageField(upload_to='projects/thumbnails/')
    
    # Project details
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, related_name='projects')
    technologies = models.ManyToManyField(Technology, related_name='projects')
    
    # Links
    github_link = models.URLField(blank=True)
    live_link = models.URLField(blank=True)
    
    # Gallery images
    featured = models.BooleanField(default=False)
    completion_date = models.DateField()
    order = models.PositiveIntegerField(default=0)
    
    # Meta information
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-completion_date', 'order']
        verbose_name = "Project"
        verbose_name_plural = "Projects"
    
    def __str__(self):
        return self.title
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

class ProjectImage(models.Model):
    """Model for project gallery images"""
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='projects/gallery/')
    caption = models.CharField(max_length=200, blank=True)
    order = models.PositiveIntegerField(default=0)
    
    class Meta:
        ordering = ['order']
        verbose_name = "Project Image"
        verbose_name_plural = "Project Images"
    
    def __str__(self):
        return f"Image for {self.project.title}"