from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render
from django.http import JsonResponse
from django.db import models
from .models import Poem, Category, Comment, Like  # ← Removed Tag
from .forms import PoemForm, CommentForm


class HomeView(ListView):
    """Home page showing latest published poems"""
    model = Poem
    template_name = 'home.html'
    context_object_name = 'poems'
    paginate_by = 6

    def get_queryset(self):
        return Poem.objects.filter(is_published=True).order_by('-published_at')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Featured poem
        context['featured_poem'] = Poem.objects.filter(is_published=True, is_featured=True).first()
        if not context['featured_poem']:
            context['featured_poem'] = Poem.objects.filter(is_published=True).order_by('-published_at').first()
        # Categories for sidebar
        context['categories'] = Category.objects.all()
        # Random poem for "Poem of the Day"
        context['random_poem'] = Poem.objects.filter(is_published=True).order_by('?').first()
        return context


class PoemListView(ListView):
    """List all published poems"""
    model = Poem
    template_name = 'poems/poem_list.html'
    context_object_name = 'poems'
    paginate_by = 9

    def get_queryset(self):
        return Poem.objects.filter(is_published=True).order_by('-published_at')


class PoemDetailView(DetailView):
    """Detailed view of a single poem"""
    model = Poem
    template_name = 'poems/poem_detail.html'
    context_object_name = 'poem'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        poem = self.get_object()
        poem.increment_views()
        
        context['comments'] = poem.comments.filter(is_approved=True)
        context['form'] = CommentForm()
        context['related_poems'] = Poem.objects.filter(
            category=poem.category,
            is_published=True
        ).exclude(id=poem.id)[:4]
        context['likes_count'] = poem.likes.count()
        context['user_liked'] = False
        if self.request.user.is_authenticated:
            context['user_liked'] = poem.likes.filter(user=self.request.user).exists()
        return context

    def post(self, request, *args, **kwargs):
        """Handle comment submission"""
        self.object = self.get_object()
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.poem = self.object
            comment.author = request.user
            comment.save()
            messages.success(request, 'আপনার মন্তব্য সফলভাবে যোগ হয়েছে!')
            return redirect('poem_detail', slug=self.object.slug)
        context = self.get_context_data(**kwargs)
        context['form'] = form
        return render(request, self.template_name, context)

    

class CreatePoemView(LoginRequiredMixin, CreateView):
    """Create a new poem"""
    model = Poem
    form_class = PoemForm
    template_name = 'poems/create_poem.html'
    success_url = reverse_lazy('my_poems')

    def form_valid(self, form):
        form.instance.author = self.request.user
        messages.success(self.request, 'আপনার কবিতা সফলভাবে প্রকাশিত হয়েছে!')
        return super().form_valid(form)


class UpdatePoemView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    """Update an existing poem"""
    model = Poem
    form_class = PoemForm
    template_name = 'poems/create_poem.html'
    success_url = reverse_lazy('my_poems')

    def form_valid(self, form):
        messages.success(self.request, 'আপনার কবিতা সফলভাবে আপডেট হয়েছে!')
        return super().form_valid(form)

    def test_func(self):
        poem = self.get_object()
        return self.request.user == poem.author


class DeletePoemView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    """Delete a poem"""
    model = Poem
    template_name = 'poems/confirm_delete.html'
    success_url = reverse_lazy('my_poems')

    def delete(self, request, *args, **kwargs):
        messages.success(request, 'আপনার কবিতা সফলভাবে ডিলিট হয়েছে!')
        return super().delete(request, *args, **kwargs)

    def test_func(self):
        poem = self.get_object()
        return self.request.user == poem.author


# My Poems
class MyPoemsView(LoginRequiredMixin, ListView):
    """List poems written by the logged-in user"""
    model = Poem
    template_name = 'poems/my_poems.html'
    context_object_name = 'poems'
    paginate_by = 9

    def get_queryset(self):
        return Poem.objects.filter(author=self.request.user).order_by('-created_at')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        poems = self.get_queryset()
        context['total_poems'] = poems.count()
        context['total_views'] = sum(poem.views for poem in poems)
        return context


class CategoryListView(ListView):
    """List all categories"""
    model = Category
    template_name = 'poems/category_list.html'
    context_object_name = 'categories'
    ordering = ['name']


class CategoryDetailView(ListView):
    """List poems in a specific category"""
    template_name = 'poems/category_detail.html'
    context_object_name = 'poems'
    paginate_by = 9

    def get_queryset(self):
        self.category = get_object_or_404(Category, slug=self.kwargs['slug'])
        return Poem.objects.filter(category=self.category, is_published=True).order_by('-published_at')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category'] = self.category
        context['category_poem_count'] = self.get_queryset().count()
        return context


class SearchView(ListView):
    """Search poems"""
    template_name = 'poems/search_results.html'
    context_object_name = 'poems'
    paginate_by = 9

    def get_queryset(self):
        query = self.request.GET.get('q', '').strip()
        if query:
            return Poem.objects.filter(
                models.Q(title__icontains=query) |
                models.Q(content__icontains=query) |
                models.Q(category__name__icontains=query) |
                models.Q(author__username__icontains=query),
                is_published=True
            ).distinct().order_by('-published_at')
        return Poem.objects.none()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['query'] = self.request.GET.get('q', '').strip()
        context['result_count'] = self.get_queryset().count()
        return context


class AboutView(ListView):
    """About page with statistics"""
    template_name = 'poems/about.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['total_poems'] = Poem.objects.filter(is_published=True).count()
        context['total_categories'] = Category.objects.count()
        context['total_authors'] = Poem.objects.filter(is_published=True).values('author').distinct().count()
        context['latest_poems'] = Poem.objects.filter(is_published=True).order_by('-published_at')[:5]
        context['popular_poems'] = Poem.objects.filter(is_published=True).order_by('-views')[:5]
        return context