from django.test import TestCase
from django.urls import reverse, resolve
from poems import views


class PoemsUrlsTest(TestCase):
    """Test poems app URLs"""

    def test_home_url(self):
        """Test home URL resolves correctly"""
        url = reverse('home')
        self.assertEqual(url, '/')
        self.assertEqual(resolve(url).view_name, 'home')
        self.assertEqual(resolve(url).func.view_class, views.HomeView)

    def test_poem_list_url(self):
        """Test poem list URL resolves correctly"""
        url = reverse('poem_list')
        self.assertEqual(url, '/poems/')
        self.assertEqual(resolve(url).view_name, 'poem_list')
        self.assertEqual(resolve(url).func.view_class, views.PoemListView)

    def test_load_more_poems_url(self):
        """Test load more poems URL resolves correctly"""
        url = reverse('load_more_poems')
        self.assertEqual(url, '/poems/load-more/')
        self.assertEqual(resolve(url).view_name, 'load_more_poems')
        self.assertEqual(resolve(url).func.view_class, views.LoadMorePoemsView)

    def test_poem_detail_url(self):
        """Test poem detail URL resolves correctly"""
        url = reverse('poem_detail', args=['test-slug'])
        self.assertEqual(url, '/poem/test-slug/')
        self.assertEqual(resolve(url).view_name, 'poem_detail')
        self.assertEqual(resolve(url).func.view_class, views.PoemDetailView)

    def test_create_poem_url(self):
        """Test create poem URL resolves correctly"""
        url = reverse('create_poem')
        self.assertEqual(url, '/create/')
        self.assertEqual(resolve(url).view_name, 'create_poem')
        self.assertEqual(resolve(url).func.view_class, views.CreatePoemView)

    def test_update_poem_url(self):
        """Test update poem URL resolves correctly"""
        url = reverse('update_poem', args=['test-slug'])
        self.assertEqual(url, '/update/test-slug/')
        self.assertEqual(resolve(url).view_name, 'update_poem')
        self.assertEqual(resolve(url).func.view_class, views.UpdatePoemView)

    def test_delete_poem_url(self):
        """Test delete poem URL resolves correctly"""
        url = reverse('delete_poem', args=['test-slug'])
        self.assertEqual(url, '/delete/test-slug/')
        self.assertEqual(resolve(url).view_name, 'delete_poem')
        self.assertEqual(resolve(url).func.view_class, views.DeletePoemView)

    def test_toggle_like_url(self):
        """Test toggle like URL resolves correctly"""
        url = reverse('toggle_like', args=['test-slug'])
        self.assertEqual(url, '/like/test-slug/')
        self.assertEqual(resolve(url).view_name, 'toggle_like')
        self.assertEqual(resolve(url).func.view_class, views.ToggleLikeView)

    def test_comment_edit_url(self):
        """Test comment edit URL resolves correctly"""
        url = reverse('comment_edit', args=[1])
        self.assertEqual(url, '/comment/edit/1/')
        self.assertEqual(resolve(url).view_name, 'comment_edit')
        self.assertEqual(resolve(url).func.view_class, views.CommentEditView)

    def test_comment_delete_url(self):
        """Test comment delete URL resolves correctly"""
        url = reverse('comment_delete', args=[1])
        self.assertEqual(url, '/comment/delete/1/')
        self.assertEqual(resolve(url).view_name, 'comment_delete')
        self.assertEqual(resolve(url).func.view_class, views.CommentDeleteView)

    def test_my_poems_url(self):
        """Test my poems URL resolves correctly"""
        url = reverse('my_poems')
        self.assertEqual(url, '/my-poems/')
        self.assertEqual(resolve(url).view_name, 'my_poems')
        self.assertEqual(resolve(url).func.view_class, views.MyPoemsView)

    def test_my_poems_load_more_url(self):
        """Test my poems load more URL resolves correctly"""
        url = reverse('my_poems_load_more')
        self.assertEqual(url, '/my-poems/load-more/')
        self.assertEqual(resolve(url).view_name, 'my_poems_load_more')
        self.assertEqual(resolve(url).func.view_class, views.MyPoemsLoadMoreView)

    def test_category_list_url(self):
        """Test category list URL resolves correctly"""
        url = reverse('category_list')
        self.assertEqual(url, '/categories/')
        self.assertEqual(resolve(url).view_name, 'category_list')
        self.assertEqual(resolve(url).func.view_class, views.CategoryListView)

    def test_category_detail_url(self):
        """Test category detail URL resolves correctly"""
        url = reverse('category_detail', args=['romantic'])
        self.assertEqual(url, '/category/romantic/')
        self.assertEqual(resolve(url).view_name, 'category_detail')
        self.assertEqual(resolve(url).func.view_class, views.CategoryDetailView)

    def test_category_load_more_url(self):
        """Test category load more URL resolves correctly"""
        url = reverse('category_load_more', args=['romantic'])
        self.assertEqual(url, '/category/romantic/load-more/')
        self.assertEqual(resolve(url).view_name, 'category_load_more')
        self.assertEqual(resolve(url).func.view_class, views.CategoryLoadMorePoemsView)

    def test_search_url(self):
        """Test search URL resolves correctly"""
        url = reverse('search')
        self.assertEqual(url, '/search/')
        self.assertEqual(resolve(url).view_name, 'search')
        self.assertEqual(resolve(url).func.view_class, views.SearchView)

    def test_search_load_more_url(self):
        """Test search load more URL resolves correctly"""
        url = reverse('search_load_more')
        self.assertEqual(url, '/search/load-more/')
        self.assertEqual(resolve(url).view_name, 'search_load_more')
        self.assertEqual(resolve(url).func.view_class, views.SearchLoadMoreView)

    def test_about_url(self):
        """Test about URL resolves correctly"""
        url = reverse('about')
        self.assertEqual(url, '/about/')
        self.assertEqual(resolve(url).view_name, 'about')
        self.assertEqual(resolve(url).func.view_class, views.AboutView)