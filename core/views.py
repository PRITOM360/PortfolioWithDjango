from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from django.views.generic import TemplateView, FormView

from .models import (
    About, Education, Experience, 
    Service, Testimonial, Skill
)
from .forms import ContactForm
from projects.models import Project, Category
from blog.models import Post

class HomeView(TemplateView):
    template_name = 'core/home.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['about'] = About.objects.first()
        context['services'] = Service.objects.all()[:6]
        context['testimonials'] = Testimonial.objects.all()[:6]
        context['projects'] = Project.objects.filter(featured=True)[:6]
        context['posts'] = Post.objects.filter(status='published')[:3]
        
        # Group skills by category
        skills = Skill.objects.all()
        skill_categories = {}
        for skill in skills:
            category = skill.get_category_display()
            if category not in skill_categories:
                skill_categories[category] = []
            skill_categories[category].append(skill)
        
        context['skill_categories'] = skill_categories
        return context

class AboutView(TemplateView):
    template_name = 'core/about.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['about'] = About.objects.first()
        context['education'] = Education.objects.all()
        context['experience'] = Experience.objects.all()
        return context

class ServicesView(TemplateView):
    template_name = 'core/services.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['services'] = Service.objects.all()
        return context

class SkillsView(TemplateView):
    template_name = 'core/skills.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Group skills by category
        skills = Skill.objects.all()
        skill_categories = {}
        for skill in skills:
            category = skill.get_category_display()
            if category not in skill_categories:
                skill_categories[category] = []
            skill_categories[category].append(skill)
        
        context['skill_categories'] = skill_categories
        return context

class TestimonialsView(TemplateView):
    template_name = 'core/testimonials.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['testimonials'] = Testimonial.objects.all()
        return context

class ContactView(FormView):
    template_name = 'core/contact.html'
    form_class = ContactForm
    success_url = '/contact/?sent=1'
    
    def form_valid(self, form):
        # Save the contact message
        form.save()
        
        # Send email notification
        name = form.cleaned_data['name']
        email = form.cleaned_data['email']
        subject = form.cleaned_data['subject']
        message = form.cleaned_data['message']
        
        email_subject = f"New Contact Form Submission: {subject}"
        email_message = f"Name: {name}\nEmail: {email}\n\nMessage:\n{message}"
        
        try:
            send_mail(
                email_subject,
                email_message,
                email,  # From email
                [settings.EMAIL_HOST_USER],  # To email
                fail_silently=False,
            )
        except Exception as e:
            # Just log the error but don't prevent form submission
            print(f"Email sending failed: {e}")
        
        messages.success(self.request, "Your message has been sent successfully. We'll get back to you soon!")
        return super().form_valid(form)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if 'sent' in self.request.GET:
            context['sent'] = True
        return context