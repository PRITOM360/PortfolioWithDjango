from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify
from ckeditor.fields import RichTextField

class Category(models.Model):
    """Model for blog categories"""
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True, blank=True)
    
    class Meta:
        verbose_name = "Blog Category"
        verbose_name_plural = "Blog Categories"
        ordering = ['name']
    
    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

class Tag(models.Model):
    """Model for blog tags"""
    name = models.CharField(max_length=50)
    slug = models.SlugField(unique=True, blank=True)
    
    class Meta:
        verbose_name = "Tag"
        verbose_name_plural = "Tags"
        ordering = ['name']
    
    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

class Post(models.Model):
    """Model for blog posts"""
    STATUS_CHOICES = (
        ('draft', 'Draft'),
        ('published', 'Published'),
    )
    
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, blank=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='blog_posts')
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, related_name='posts')
    tags = models.ManyToManyField(Tag, blank=True, related_name='posts')
    
    featured_image = models.ImageField(upload_to='blog/', blank=True)
    summary = models.TextField(max_length=300)
    content = RichTextField()
    
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='draft')
    featured = models.BooleanField(default=False)
    
    published_date = models.DateTimeField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-published_date', '-created_at']
        verbose_name = "Post"
        verbose_name_plural = "Posts"
    
    def __str__(self):
        return self.title
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

class Comment(models.Model):
    """Model for blog comments"""
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    name = models.CharField(max_length=100)
    email = models.EmailField()
    website = models.URLField(blank=True)
    content = models.TextField()
    
    is_approved = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = "Comment"
        verbose_name_plural = "Comments"
    
    def __str__(self):
        return f"Comment by {self.name} on {self.post.title}"