from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView
from .models import Project, Category, Technology

class ProjectListView(ListView):
    model = Project
    template_name = 'projects/project_list.html'
    context_object_name = 'projects'
    paginate_by = 9
    
    def get_queryset(self):
        queryset = Project.objects.all()
        
        # Filter by category if provided
        category_slug = self.kwargs.get('category_slug')
        if category_slug:
            category = get_object_or_404(Category, slug=category_slug)
            queryset = queryset.filter(category=category)
        
        # Filter by technology if provided
        technology_slug = self.kwargs.get('technology_slug')
        if technology_slug:
            technology = get_object_or_404(Technology, slug=technology_slug)
            queryset = queryset.filter(technologies=technology)
        
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        context['technologies'] = Technology.objects.all()
        
        # Add active filters
        category_slug = self.kwargs.get('category_slug')
        if category_slug:
            context['active_category'] = get_object_or_404(Category, slug=category_slug)
        
        technology_slug = self.kwargs.get('technology_slug')
        if technology_slug:
            context['active_technology'] = get_object_or_404(Technology, slug=technology_slug)
        
        return context

class ProjectDetailView(DetailView):
    model = Project
    template_name = 'projects/project_detail.html'
    context_object_name = 'project'
    slug_url_kwarg = 'slug'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        project = self.get_object()
        
        # Get related projects (same category)
        related_projects = Project.objects.filter(category=project.category).exclude(id=project.id)[:3]
        context['related_projects'] = related_projects
        
        return context