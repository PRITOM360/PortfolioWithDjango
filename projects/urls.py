from django.urls import path
from . import views

app_name = 'projects'

urlpatterns = [
    path('', views.ProjectListView.as_view(), name='project_list'),
    path('category/<slug:category_slug>/', views.ProjectListView.as_view(), name='project_category'),
    path('technology/<slug:technology_slug>/', views.ProjectListView.as_view(), name='project_technology'),
    path('<slug:slug>/', views.ProjectDetailView.as_view(), name='project_detail'),
]