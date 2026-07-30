from django.urls import path
from . import views

urlpatterns = [
    # Home
    path('', views.HomeView.as_view(), name='home'),
    
    # Poems
    path('poems/', views.PoemListView.as_view(), name='poem_list'),
    
    # 🚨 ADD THIS LINE RIGHT HERE:
    path('poems/load-more/', views.LoadMorePoemsView.as_view(), name='load_more_poems'),
    
    path('poem/<slug:slug>/', views.PoemDetailView.as_view(), name='poem_detail'),
    path('create/', views.CreatePoemView.as_view(), name='create_poem'),
    path('update/<slug:slug>/', views.UpdatePoemView.as_view(), name='update_poem'),
    path('delete/<slug:slug>/', views.DeletePoemView.as_view(), name='delete_poem'),
    
    # Like
    path('like/<slug:slug>/', views.ToggleLikeView.as_view(), name='toggle_like'),
    
    # Comments
    path('comment/edit/<int:pk>/', views.CommentEditView.as_view(), name='comment_edit'),
    path('comment/delete/<int:pk>/', views.CommentDeleteView.as_view(), name='comment_delete'),
    
    # My Poems
    path('my-poems/', views.MyPoemsView.as_view(), name='my_poems'),
    
    # Categories
    path('categories/', views.CategoryListView.as_view(), name='category_list'),
    path('category/<slug:slug>/', views.CategoryDetailView.as_view(), name='category_detail'),
    
    # Search
    path('search/', views.SearchView.as_view(), name='search'),
    
    # About
    path('about/', views.AboutView.as_view(), name='about'),
]