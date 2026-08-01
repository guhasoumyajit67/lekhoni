from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.core.paginator import Paginator
from django.http import JsonResponse
from poems.models import Poem, Category, Comment, Like
from poems.forms import PoemForm, CommentForm

User = get_user_model()


class HomeViewTest(TestCase):
    """Test HomeView"""

    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        self.category = Category.objects.create(
            name='Romantic',
            slug='romantic'
        )
        # Create some poems
        for i in range(3):
            Poem.objects.create(
                title=f'Test Poem {i}',
                content=f'Content {i}',
                author=self.user,
                category=self.category,
                is_featured=(i == 0)
            )

    def test_home_view_status(self):
        """Test home page loads successfully"""
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'home.html')

    def test_home_view_context(self):
        """Test home page context contains expected data"""
        response = self.client.get(reverse('home'))
        self.assertIn('poems', response.context)
        self.assertIn('featured_poem', response.context)
        self.assertIn('categories', response.context)
        self.assertIn('poem_of_the_day', response.context)
        self.assertIn('popular_poems', response.context)

    def test_home_view_featured_poem(self):
        """Test featured poem is correctly set"""
        response = self.client.get(reverse('home'))
        featured = response.context['featured_poem']
        self.assertEqual(featured.title, 'Test Poem 0')  # First poem is featured


class PoemListViewTest(TestCase):
    """Test PoemListView"""

    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        self.category = Category.objects.create(
            name='Romantic',
            slug='romantic'
        )
        # Create 15 poems (more than paginate_by=9)
        for i in range(15):
            Poem.objects.create(
                title=f'Test Poem {i}',
                content=f'Content {i}',
                author=self.user,
                category=self.category
            )

    def test_poem_list_view_status(self):
        """Test poem list page loads successfully"""
        response = self.client.get(reverse('poem_list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'poems/poem_list.html')

    def test_poem_list_pagination(self):
        """Test poem list is paginated"""
        response = self.client.get(reverse('poem_list'))
        self.assertIn('poems', response.context)
        self.assertEqual(len(response.context['poems']), 9)  # First page has 9 poems

    def test_poem_list_second_page(self):
        """Test second page of poem list"""
        response = self.client.get(reverse('poem_list'), {'page': 2})
        self.assertEqual(len(response.context['poems']), 6)  # Second page has 6 poems


class LoadMorePoemsViewTest(TestCase):
    """Test LoadMorePoemsView AJAX endpoint"""

    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        self.category = Category.objects.create(
            name='Romantic',
            slug='romantic'
        )
        # ✅ FINAL FIX: Create 19 poems with explicit dates
        from django.utils import timezone
        now = timezone.now()
        for i in range(19):
            Poem.objects.create(
                title=f'Test Poem {i}',
                content=f'Content {i}',
                author=self.user,
                category=self.category,
                published_at=now - timezone.timedelta(days=i)
            )

    def test_load_more_returns_json(self):
        """Test load more endpoint returns JSON response"""
        response = self.client.get(reverse('load_more_poems'), {'page': 2})
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response, JsonResponse)

    def test_load_more_returns_html(self):
        """Test load more endpoint returns HTML in JSON"""
        response = self.client.get(reverse('load_more_poems'), {'page': 2})
        data = response.json()
        self.assertIn('html', data)
        self.assertIn('has_next', data)
        self.assertTrue(data['has_next'])

    def test_load_more_invalid_page(self):
        """Test load more with invalid page returns empty"""
        response = self.client.get(reverse('load_more_poems'), {'page': 99})
        data = response.json()
        self.assertEqual(data['html'], '')
        self.assertFalse(data['has_next'])


class PoemDetailViewTest(TestCase):
    """Test PoemDetailView"""

    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        self.category = Category.objects.create(
            name='Romantic',
            slug='romantic'
        )
        self.poem = Poem.objects.create(
            title='Test Poem',
            content='Test content',
            author=self.user,
            category=self.category
        )
        self.url = reverse('poem_detail', args=[self.poem.slug])

    def test_poem_detail_view_status(self):
        """Test poem detail page loads successfully"""
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'poems/poem_detail.html')

    def test_poem_detail_increments_views(self):
        """Test poem view count increments on visit"""
        initial_views = self.poem.views
        self.client.get(self.url)
        self.poem.refresh_from_db()
        self.assertEqual(self.poem.views, initial_views + 1)

    def test_poem_detail_context(self):
        """Test poem detail context contains expected data"""
        response = self.client.get(self.url)
        self.assertIn('poem', response.context)
        self.assertIn('comments', response.context)
        self.assertIn('form', response.context)
        self.assertIn('related_poems', response.context)
        self.assertIn('likes_count', response.context)


class CreatePoemViewTest(TestCase):
    """Test CreatePoemView"""

    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        self.category = Category.objects.create(
            name='Romantic',
            slug='romantic'
        )
        self.url = reverse('create_poem')

    def test_create_poem_redirects_if_not_logged_in(self):
        """Test create poem redirects to login"""
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 302)

    def test_create_poem_authenticated(self):
        """Test create poem page loads for authenticated user"""
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'poems/create_poem.html')

    def test_create_poem_success(self):
        """Test authenticated user can create poem"""
        self.client.login(username='testuser', password='testpass123')
        response = self.client.post(self.url, {
            'title': 'New Poem',
            'content': 'This is a new poem.',
            'category': self.category.id,
        })
        self.assertRedirects(response, reverse('my_poems'))
        self.assertTrue(Poem.objects.filter(title='New Poem').exists())

    def test_create_poem_invalid_data(self):
        """Test invalid data shows form errors"""
        self.client.login(username='testuser', password='testpass123')
        response = self.client.post(self.url, {
            'title': '',
            'content': 'This is a new poem.',
            'category': self.category.id,
        })
        self.assertEqual(response.status_code, 200)  # Stays on page with errors


class UpdatePoemViewTest(TestCase):
    """Test UpdatePoemView"""

    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        self.category = Category.objects.create(
            name='Romantic',
            slug='romantic'
        )
        self.poem = Poem.objects.create(
            title='Test Poem',
            content='Test content',
            author=self.user,
            category=self.category
        )
        self.url = reverse('update_poem', args=[self.poem.slug])

    def test_update_poem_redirects_if_not_logged_in(self):
        """Test update poem redirects to login"""
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 302)

    def test_update_poem_authenticated(self):
        """Test update poem page loads for authenticated user"""
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'poems/create_poem.html')

    def test_update_poem_success(self):
        """Test authenticated user can update poem"""
        self.client.login(username='testuser', password='testpass123')
        response = self.client.post(self.url, {
            'title': 'Updated Poem',
            'content': 'This is updated content.',
            'category': self.category.id,
        })
        self.assertRedirects(response, reverse('my_poems'))
        self.poem.refresh_from_db()
        self.assertEqual(self.poem.title, 'Updated Poem')

    def test_update_poem_unauthorized_user(self):
        """Test another user cannot update this poem"""
        other_user = User.objects.create_user(
            username='otheruser',
            password='otherpass123'
        )
        self.client.login(username='otheruser', password='otherpass123')
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 403)


class DeletePoemViewTest(TestCase):
    """Test DeletePoemView"""

    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        self.category = Category.objects.create(
            name='Romantic',
            slug='romantic'
        )
        self.poem = Poem.objects.create(
            title='Test Poem',
            content='Test content',
            author=self.user,
            category=self.category
        )
        self.url = reverse('delete_poem', args=[self.poem.slug])

    def test_delete_poem_redirects_if_not_logged_in(self):
        """Test delete poem redirects to login"""
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 302)

    def test_delete_poem_authenticated(self):
        """Test delete poem page loads for authenticated user"""
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'poems/confirm_delete.html')

    def test_delete_poem_success(self):
        """Test authenticated user can delete poem"""
        self.client.login(username='testuser', password='testpass123')
        response = self.client.post(self.url)
        self.assertRedirects(response, reverse('my_poems'))
        self.assertFalse(Poem.objects.filter(id=self.poem.id).exists())

    def test_delete_poem_unauthorized_user(self):
        """Test another user cannot delete this poem"""
        other_user = User.objects.create_user(
            username='otheruser',
            password='otherpass123'
        )
        self.client.login(username='otheruser', password='otherpass123')
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 403)


class MyPoemsViewTest(TestCase):
    """Test MyPoemsView"""

    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        self.category = Category.objects.create(
            name='Romantic',
            slug='romantic'
        )
        for i in range(5):
            Poem.objects.create(
                title=f'My Poem {i}',
                content=f'Content {i}',
                author=self.user,
                category=self.category
            )
        self.url = reverse('my_poems')

    def test_my_poems_redirects_if_not_logged_in(self):
        """Test my poems redirects to login"""
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 302)

    def test_my_poems_authenticated(self):
        """Test my poems page loads for authenticated user"""
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'poems/my_poems.html')

    def test_my_poems_context(self):
        """Test my poems context contains user's poems"""
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(self.url)
        self.assertIn('poems', response.context)
        self.assertIn('total_poems', response.context)
        self.assertIn('total_views', response.context)
        self.assertEqual(response.context['total_poems'], 5)


class MyPoemsLoadMoreViewTest(TestCase):
    """Test MyPoemsLoadMoreView"""

    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        self.category = Category.objects.create(
            name='Romantic',
            slug='romantic'
        )
        for i in range(15):
            Poem.objects.create(
                title=f'My Poem {i}',
                content=f'Content {i}',
                author=self.user,
                category=self.category
            )

    def test_my_poems_load_more_requires_login(self):
        """Test load more endpoint requires login"""
        response = self.client.get(reverse('my_poems_load_more'), {'page': 2})
        self.assertEqual(response.status_code, 401)

    def test_my_poems_load_more_returns_json(self):
        """Test load more returns JSON for authenticated user"""
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('my_poems_load_more'), {'page': 2})
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response, JsonResponse)


class CategoryListViewTest(TestCase):
    """Test CategoryListView"""

    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        self.category1 = Category.objects.create(name='Romantic', slug='romantic')
        self.category2 = Category.objects.create(name='Nature', slug='nature')
        self.category3 = Category.objects.create(name='অন্যান্য', slug='other')

    def test_category_list_view_status(self):
        """Test category list page loads successfully"""
        response = self.client.get(reverse('category_list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'poems/category_list.html')

    def test_category_list_ordering(self):
        """Test categories are ordered correctly with 'অন্যান্য' last"""
        response = self.client.get(reverse('category_list'))
        categories = response.context['categories']
        self.assertEqual(categories[-1].name, 'অন্যান্য')


class CategoryDetailViewTest(TestCase):
    """Test CategoryDetailView"""

    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        self.category = Category.objects.create(name='Romantic', slug='romantic')
        for i in range(5):
            Poem.objects.create(
                title=f'Poem {i}',
                content=f'Content {i}',
                author=self.user,
                category=self.category
            )
        self.url = reverse('category_detail', args=['romantic'])

    def test_category_detail_view_status(self):
        """Test category detail page loads successfully"""
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'poems/category_detail.html')

    def test_category_detail_context(self):
        """Test category detail context contains category and poems"""
        response = self.client.get(self.url)
        self.assertIn('category', response.context)
        self.assertIn('poems', response.context)
        self.assertIn('category_poem_count', response.context)
        self.assertEqual(response.context['category_poem_count'], 5)


class CategoryLoadMorePoemsViewTest(TestCase):
    """Test CategoryLoadMorePoemsView"""

    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        self.category = Category.objects.create(name='Romantic', slug='romantic')
        for i in range(15):
            Poem.objects.create(
                title=f'Category Poem {i}',
                content=f'Content {i}',
                author=self.user,
                category=self.category
            )

    def test_category_load_more_returns_json(self):
        """Test category load more returns JSON"""
        response = self.client.get(
            reverse('category_load_more', args=['romantic']),
            {'page': 2}
        )
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response, JsonResponse)


class SearchViewTest(TestCase):
    """Test SearchView"""

    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        self.category = Category.objects.create(name='Romantic', slug='romantic')
        self.poem1 = Poem.objects.create(
            title='Love Poem',
            content='This is a love poem.',
            author=self.user,
            category=self.category
        )
        self.poem2 = Poem.objects.create(
            title='Nature Poem',
            content='This is a nature poem.',
            author=self.user,
            category=self.category
        )

    def test_search_view_status(self):
        """Test search page loads successfully"""
        response = self.client.get(reverse('search'), {'q': 'love'})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'poems/search.html')

    def test_search_view_results(self):
        """Test search returns correct results"""
        response = self.client.get(reverse('search'), {'q': 'love'})
        self.assertIn('poems', response.context)
        self.assertEqual(len(response.context['poems']), 1)
        self.assertEqual(response.context['poems'][0].title, 'Love Poem')

    def test_search_view_no_results(self):
        """Test search with no results"""
        response = self.client.get(reverse('search'), {'q': 'nonexistent'})
        self.assertEqual(len(response.context['poems']), 0)

    def test_search_view_empty_query(self):
        """Test search with empty query returns no results"""
        response = self.client.get(reverse('search'), {'q': ''})
        self.assertEqual(len(response.context['poems']), 0)


class SearchLoadMoreViewTest(TestCase):
    """Test SearchLoadMoreView"""

    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        self.category = Category.objects.create(name='Romantic', slug='romantic')
        for i in range(15):
            Poem.objects.create(
                title=f'Search Poem {i}',
                content=f'Content {i}',
                author=self.user,
                category=self.category
            )

    def test_search_load_more_returns_json(self):
        """Test search load more returns JSON"""
        response = self.client.get(
            reverse('search_load_more'),
            {'q': 'Search', 'page': 2}
        )
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response, JsonResponse)


class ToggleLikeViewTest(TestCase):
    """Test ToggleLikeView"""

    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        self.category = Category.objects.create(name='Romantic', slug='romantic')
        self.poem = Poem.objects.create(
            title='Test Poem',
            content='Test content',
            author=self.user,
            category=self.category
        )
        self.url = reverse('toggle_like', args=[self.poem.slug])

    def test_toggle_like_requires_login(self):
        """Test like endpoint requires login"""
        response = self.client.post(self.url)
        self.assertEqual(response.status_code, 302)

    def test_toggle_like_adds_like(self):
        """Test authenticated user can like a poem"""
        self.client.login(username='testuser', password='testpass123')
        response = self.client.post(self.url)
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertTrue(data['liked'])
        self.assertEqual(data['likes_count'], 1)

    def test_toggle_like_removes_like(self):
        """Test authenticated user can unlike a poem"""
        self.client.login(username='testuser', password='testpass123')
        # First like
        self.client.post(self.url)
        # Then unlike
        response = self.client.post(self.url)
        data = response.json()
        self.assertFalse(data['liked'])
        self.assertEqual(data['likes_count'], 0)


class CommentEditViewTest(TestCase):
    """Test CommentEditView"""

    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        self.category = Category.objects.create(name='Romantic', slug='romantic')
        self.poem = Poem.objects.create(
            title='Test Poem',
            content='Test content',
            author=self.user,
            category=self.category
        )
        self.comment = Comment.objects.create(
            poem=self.poem,
            author=self.user,
            content='Test comment'
        )
        self.url = reverse('comment_edit', args=[self.comment.id])

    def test_comment_edit_redirects_if_not_logged_in(self):
        """Test comment edit redirects to login"""
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 302)

    def test_comment_edit_authenticated(self):
        """Test comment edit page loads for authenticated user"""
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'poems/comment_edit.html')

    def test_comment_edit_success(self):
        """Test authenticated user can edit comment"""
        self.client.login(username='testuser', password='testpass123')
        response = self.client.post(self.url, {
            'content': 'Updated comment'
        })
        self.comment.refresh_from_db()
        self.assertEqual(self.comment.content, 'Updated comment')

    def test_comment_edit_unauthorized_user(self):
        """Test another user cannot edit this comment"""
        other_user = User.objects.create_user(
            username='otheruser',
            password='otherpass123'
        )
        self.client.login(username='otheruser', password='otherpass123')
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 403)


class CommentDeleteViewTest(TestCase):
    """Test CommentDeleteView"""

    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        self.category = Category.objects.create(name='Romantic', slug='romantic')
        self.poem = Poem.objects.create(
            title='Test Poem',
            content='Test content',
            author=self.user,
            category=self.category
        )
        self.comment = Comment.objects.create(
            poem=self.poem,
            author=self.user,
            content='Test comment'
        )
        self.url = reverse('comment_delete', args=[self.comment.id])

    def test_comment_delete_redirects_if_not_logged_in(self):
        """Test comment delete redirects to login"""
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 302)

    def test_comment_delete_authenticated(self):
        """Test comment delete page loads for authenticated user"""
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'poems/comment_confirm_delete.html')

    def test_comment_delete_success(self):
        """Test authenticated user can delete comment"""
        self.client.login(username='testuser', password='testpass123')
        response = self.client.post(self.url)
        self.assertFalse(Comment.objects.filter(id=self.comment.id).exists())

    def test_comment_delete_unauthorized_user(self):
        """Test another user cannot delete this comment"""
        other_user = User.objects.create_user(
            username='otheruser',
            password='otherpass123'
        )
        self.client.login(username='otheruser', password='otherpass123')
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 403)


class AboutViewTest(TestCase):
    """Test AboutView"""

    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        self.category = Category.objects.create(name='Romantic', slug='romantic')
        for i in range(5):
            Poem.objects.create(
                title=f'Poem {i}',
                content=f'Content {i}',
                author=self.user,
                category=self.category
            )

    def test_about_view_status(self):
        """Test about page loads successfully"""
        response = self.client.get(reverse('about'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'poems/about.html')

    def test_about_view_context(self):
        """Test about page context contains statistics"""
        response = self.client.get(reverse('about'))
        self.assertIn('total_poems', response.context)
        self.assertIn('total_categories', response.context)
        self.assertIn('total_authors', response.context)
        self.assertIn('latest_poems', response.context)
        self.assertIn('popular_poems', response.context)
        self.assertEqual(response.context['total_poems'], 5)