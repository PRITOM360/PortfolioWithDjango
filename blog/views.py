from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView, FormView
from django.views.generic.detail import SingleObjectMixin
from django.urls import reverse
from django.contrib import messages
from django.utils import timezone
from django.db.models import Count

from .models import Post, Category, Tag, Comment
from .forms import CommentForm

class PostListView(ListView):
    model = Post
    template_name = 'blog/post_list.html'
    context_object_name = 'posts'
    paginate_by = 6
    
    def get_queryset(self):
        queryset = Post.objects.filter(status='published')
        
        # Filter by category if provided
        category_slug = self.kwargs.get('category_slug')
        if category_slug:
            category = get_object_or_404(Category, slug=category_slug)
            queryset = queryset.filter(category=category)
        
        # Filter by tag if provided
        tag_slug = self.kwargs.get('tag_slug')
        if tag_slug:
            tag = get_object_or_404(Tag, slug=tag_slug)
            queryset = queryset.filter(tags=tag)
        
        # Search query if provided
        search_query = self.request.GET.get('q')
        if search_query:
            queryset = queryset.filter(
                title__icontains=search_query
            ) | queryset.filter(
                summary__icontains=search_query
            ) | queryset.filter(
                content__icontains=search_query
            )
        
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.annotate(post_count=Count('posts'))
        context['tags'] = Tag.objects.annotate(post_count=Count('posts')).order_by('-post_count')[:20]
        
        # Featured posts
        context['featured_posts'] = Post.objects.filter(status='published', featured=True)[:3]
        
        # Add active filters
        category_slug = self.kwargs.get('category_slug')
        if category_slug:
            context['active_category'] = get_object_or_404(Category, slug=category_slug)
        
        tag_slug = self.kwargs.get('tag_slug')
        if tag_slug:
            context['active_tag'] = get_object_or_404(Tag, slug=tag_slug)
        
        # Search query
        search_query = self.request.GET.get('q')
        if search_query:
            context['search_query'] = search_query
        
        return context

class PostDetailView(DetailView):
    model = Post
    template_name = 'blog/post_detail.html'
    context_object_name = 'post'
    slug_url_kwarg = 'slug'
    
    def get_queryset(self):
        return Post.objects.filter(status='published')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        post = self.get_object()
        
        # Comment form
        context['comment_form'] = CommentForm()
        
        # Approved comments
        context['comments'] = post.comments.filter(is_approved=True)
        
        # Related posts (same category)
        related_posts = Post.objects.filter(
            category=post.category, 
            status='published'
        ).exclude(id=post.id)[:3]
        context['related_posts'] = related_posts
        
        # Recent posts
        context['recent_posts'] = Post.objects.filter(
            status='published'
        ).exclude(id=post.id)[:5]
        
        return context
    
    def post(self, request, *args, **kwargs):
        post = self.get_object()
        form = CommentForm(request.POST)
        
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.save()
            messages.success(request, "Your comment has been submitted and is awaiting approval.")
            return redirect('blog:post_detail', slug=post.slug)
        
        # If form is not valid, render the template with form errors
        context = self.get_context_data()
        context['comment_form'] = form
        return render(request, self.template_name, context)