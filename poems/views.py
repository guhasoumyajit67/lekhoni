from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render
from django.http import JsonResponse
from django.db import models
from django.utils import timezone
from datetime import timedelta
from .models import Poem, Category, Comment, Like
from .forms import PoemForm, CommentForm, CommentEditForm
from django.views import View
from django.core.paginator import Paginator


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
        
        # Categories sorted by poem count, with "অন্যান্য" last
        categories = []
        other_category = None
        
        for category in Category.objects.all():
            poem_count = Poem.objects.filter(category=category, is_published=True).count()
            category.poem_count = poem_count
            if category.name == 'অন্যান্য':
                other_category = category
            else:
                categories.append(category)
        
        categories.sort(key=lambda x: x.poem_count, reverse=True)
        
        if other_category:
            categories.append(other_category)
        
        context['categories'] = categories
        
        # ============================================
        # POEM OF THE DAY (Most popular in last 24 hours)
        # ============================================
        twenty_four_hours_ago = timezone.now() - timedelta(hours=24)
        context['poem_of_the_day'] = Poem.objects.filter(
            is_published=True,
            published_at__gte=twenty_four_hours_ago
        ).order_by('-views').first()
        
        # If no poem in last 24 hours, fallback to latest published
        if not context['poem_of_the_day']:
            context['poem_of_the_day'] = Poem.objects.filter(is_published=True).order_by('-published_at').first()
        
        # ============================================
        # MOST POPULAR POEMS IN LAST 7 DAYS
        # ============================================
        seven_days_ago = timezone.now() - timedelta(days=7)
        context['popular_poems'] = Poem.objects.filter(
            is_published=True,
            published_at__gte=seven_days_ago
        ).order_by('-views')[:3]
        
        return context


class PoemListView(ListView):
    """List all published poems"""
    model = Poem
    template_name = 'poems/poem_list.html'
    context_object_name = 'poems'
    paginate_by = 9

    def get_queryset(self):
        return Poem.objects.filter(is_published=True).order_by('-published_at')


class LoadMorePoemsView(View):
    """API endpoint to fetch next batch of poems via AJAX"""
    
    def get(self, request, *args, **kwargs):
        page = request.GET.get('page', 2)  # Start from page 2
        
        all_poems = Poem.objects.filter(is_published=True).order_by('-published_at')
        paginator = Paginator(all_poems, 9)
        
        try:
            poems = paginator.page(page)
        except:
            return JsonResponse({'html': '', 'has_next': False})
        
        # Render the partial template (just the cards)
        from django.template.loader import render_to_string
        html = render_to_string('partials/_poem_card.html', {'poems': poems})
        
        return JsonResponse({
            'html': html,
            'has_next': poems.has_next()
        })


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
            comment.is_approved = True
            comment.save()
            
            # Return JSON response for AJAX requests
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({
                    'success': True,
                    'comment_id': comment.id,
                    'message': 'আপনার মন্তব্য সফলভাবে যোগ হয়েছে!'
                })
            
            messages.success(request, 'আপনার মন্তব্য সফলভাবে যোগ হয়েছে!')
            return redirect('poem_detail', slug=self.object.slug)
        
        # If form is invalid and AJAX request
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({
                'success': False,
                'errors': form.errors,
                'message': 'মন্তব্য যুক্ত করতে সমস্যা হয়েছে।'
            }, status=400)
        
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


class MyPoemsLoadMoreView(View):
    """API endpoint to fetch next batch of user's poems via AJAX"""
    
    def get(self, request, *args, **kwargs):
        page = request.GET.get('page', 2)
        
        all_poems = Poem.objects.filter(author=request.user).order_by('-created_at')
        paginator = Paginator(all_poems, 9)
        
        try:
            poems = paginator.page(page)
        except:
            return JsonResponse({'html': '', 'has_next': False})
        
        from django.template.loader import render_to_string
        html = render_to_string('partials/_my_poem_card.html', {'poems': poems})
        
        return JsonResponse({
            'html': html,
            'has_next': poems.has_next()
        })


class CategoryListView(ListView):
    """List all categories with 'অন্যান্য' last"""
    model = Category
    template_name = 'poems/category_list.html'
    context_object_name = 'categories'
    
    def get_queryset(self):
        categories = []
        other_category = None
        
        for category in Category.objects.all():
            poem_count = Poem.objects.filter(category=category, is_published=True).count()
            category.poem_count = poem_count
            if category.name == 'অন্যান্য':
                other_category = category
            else:
                categories.append(category)
        
        categories.sort(key=lambda x: x.poem_count, reverse=True)
        
        if other_category:
            categories.append(other_category)
        
        return categories


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


class CategoryLoadMorePoemsView(View):
    """API endpoint to fetch next batch of poems for a specific category via AJAX"""
    
    def get(self, request, slug, *args, **kwargs):
        page = request.GET.get('page', 2)
        category = get_object_or_404(Category, slug=slug)
        
        all_poems = Poem.objects.filter(category=category, is_published=True).order_by('-published_at')
        paginator = Paginator(all_poems, 9)
        
        try:
            poems = paginator.page(page)
        except:
            return JsonResponse({'html': '', 'has_next': False})
        
        from django.template.loader import render_to_string
        html = render_to_string('partials/_poem_card.html', {'poems': poems})
        
        return JsonResponse({
            'html': html,
            'has_next': poems.has_next()
        })
    

class SearchView(ListView):
    """Search poems"""
    template_name = 'poems/search.html'
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


class SearchLoadMoreView(View):
    """API endpoint to fetch next batch of search results via AJAX"""
    
    def get(self, request, *args, **kwargs):
        page = request.GET.get('page', 2)
        query = request.GET.get('q', '').strip()
        
        if not query:
            return JsonResponse({'html': '', 'has_next': False})
        
        all_poems = Poem.objects.filter(
            models.Q(title__icontains=query) |
            models.Q(content__icontains=query) |
            models.Q(category__name__icontains=query) |
            models.Q(author__username__icontains=query),
            is_published=True
        ).distinct().order_by('-published_at')
        
        paginator = Paginator(all_poems, 9)
        
        try:
            poems = paginator.page(page)
        except:
            return JsonResponse({'html': '', 'has_next': False})
        
        from django.template.loader import render_to_string
        html = render_to_string('partials/_poem_card.html', {'poems': poems})
        
        return JsonResponse({
            'html': html,
            'has_next': poems.has_next()
        })

    

class ToggleLikeView(LoginRequiredMixin, View):
    """Toggle like on a poem (AJAX)"""
    
    def post(self, request, slug):
        poem = get_object_or_404(Poem, slug=slug)
        like, created = Like.objects.get_or_create(
            poem=poem,
            user=request.user
        )
        if not created:
            like.delete()
            liked = False
        else:
            liked = True
        
        return JsonResponse({
            'liked': liked,
            'likes_count': poem.likes.count()
        })


class CommentEditView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    """Edit a comment"""
    model = Comment
    form_class = CommentEditForm
    template_name = 'poems/comment_edit.html'
    
    def get_success_url(self):
        return self.object.poem.get_absolute_url()
    
    def form_valid(self, form):
        messages.success(self.request, 'আপনার মন্তব্য সফলভাবে আপডেট হয়েছে!')
        return super().form_valid(form)
    
    def test_func(self):
        comment = self.get_object()
        return self.request.user == comment.author


class CommentDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    """Delete a comment"""
    model = Comment
    template_name = 'poems/comment_confirm_delete.html'
    
    def get_success_url(self):
        return self.object.poem.get_absolute_url()
    
    def delete(self, request, *args, **kwargs):
        messages.success(request, 'আপনার মন্তব্য সফলভাবে মুছে ফেলা হয়েছে!')
        return super().delete(request, *args, **kwargs)
    
    def test_func(self):
        comment = self.get_object()
        return self.request.user == comment.author


class AboutView(TemplateView):
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