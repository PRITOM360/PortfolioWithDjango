from django.urls import path
from . import views

app_name = 'blog'

urlpatterns = [
    path('', views.PostListView.as_view(), name='post_list'),
    path('category/<slug:category_slug>/', views.PostListView.as_view(), name='post_category'),
    path('tag/<slug:tag_slug>/', views.PostListView.as_view(), name='post_tag'),
    path('<slug:slug>/', views.PostDetailView.as_view(), name='post_detail'),
]