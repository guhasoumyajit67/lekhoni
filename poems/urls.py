from django.urls import path
from . import views

urlpatterns = [
    # Home
    path('', views.HomeView.as_view(), name='home'),
    
    # Poems
    path('poems/', views.PoemListView.as_view(), name='poem_list'),
    path('poem/<slug:slug>/', views.PoemDetailView.as_view(), name='poem_detail'),
    path('create/', views.CreatePoemView.as_view(), name='create_poem'),
    path('update/<slug:slug>/', views.UpdatePoemView.as_view(), name='update_poem'),
    path('delete/<slug:slug>/', views.DeletePoemView.as_view(), name='delete_poem'),
    
    # My Poems
    path('my-poems/', views.MyPoemsView.as_view(), name='my_poems'),
    
    # Categories
    path('categories/', views.CategoryListView.as_view(), name='category_list'),
    path('category/<slug:slug>/', views.CategoryDetailView.as_view(), name='category_detail'),
    
    # Tags
    path('tag/<slug:slug>/', views.TagDetailView.as_view(), name='tag_detail'),
    
    # Search
    path('search/', views.SearchView.as_view(), name='search'),
    
    # About
    path('about/', views.AboutView.as_view(), name='about'),
]