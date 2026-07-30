from django.urls import path
from . import views

urlpatterns = [
    # Home
    path('', views.HomeView.as_view(), name='home'),
    
    # Poems
    path('poems/', views.PoemListView.as_view(), name='poem_list'),
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
    path('my-poems/load-more/', views.MyPoemsLoadMoreView.as_view(), name='my_poems_load_more'),
    
    # Categories
    path('categories/', views.CategoryListView.as_view(), name='category_list'),
    path('category/<slug:slug>/', views.CategoryDetailView.as_view(), name='category_detail'),
    path('category/<slug:slug>/load-more/', views.CategoryLoadMorePoemsView.as_view(), name='category_load_more'),
    
    # Search
    path('search/', views.SearchView.as_view(), name='search'),
    
    # 🚨 ADD THIS MISSING LINE RIGHT HERE:
    path('search/load-more/', views.SearchLoadMoreView.as_view(), name='search_load_more'),
    
    # About
    path('about/', views.AboutView.as_view(), name='about'),
]