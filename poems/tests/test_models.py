from django.test import TestCase
from django.contrib.auth import get_user_model
from django.utils import timezone
from poems.models import Category, Poem, Comment, Like

User = get_user_model()


class CategoryModelTest(TestCase):
    """Test the Category model"""

    def setUp(self):
        self.category = Category.objects.create(
            name='Romantic',
            description='Romantic poetry category',
            icon='fa-heart'
        )

    def test_category_creation(self):
        """Test category is created successfully"""
        self.assertEqual(self.category.name, 'Romantic')
        self.assertEqual(self.category.description, 'Romantic poetry category')
        self.assertEqual(self.category.icon, 'fa-heart')
        self.assertTrue(self.category.slug)

    def test_category_str_method(self):
        """Test __str__ method returns category name"""
        self.assertEqual(str(self.category), 'Romantic')

    def test_category_slug_auto_generated(self):
        """Test slug is auto-generated from name"""
        self.assertEqual(self.category.slug, 'romantic')

    def test_category_get_absolute_url(self):
        """Test get_absolute_url returns correct URL"""
        url = self.category.get_absolute_url()
        self.assertEqual(url, '/category/romantic/')


class PoemModelTest(TestCase):
    """Test the Poem model"""

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
            content='This is a test poem content.',
            author=self.user,
            category=self.category
        )

    def test_poem_creation(self):
        """Test poem is created successfully"""
        self.assertEqual(self.poem.title, 'Test Poem')
        self.assertEqual(self.poem.content, 'This is a test poem content.')
        self.assertEqual(self.poem.author, self.user)
        self.assertEqual(self.poem.category, self.category)
        self.assertTrue(self.poem.is_published)
        self.assertEqual(self.poem.views, 0)

    def test_poem_str_method(self):
        """Test __str__ method returns poem title"""
        self.assertEqual(str(self.poem), 'Test Poem')

    def test_poem_slug_auto_generated(self):
        """Test slug is auto-generated from title"""
        self.assertTrue(self.poem.slug)
        self.assertEqual(self.poem.slug, 'test-poem')

    def test_poem_slug_unique_with_counter(self):
        """Test duplicate titles get unique slugs with counter"""
        poem2 = Poem.objects.create(
            title='Test Poem',
            content='Another test poem.',
            author=self.user
        )
        self.assertNotEqual(self.poem.slug, poem2.slug)
        self.assertEqual(poem2.slug, 'test-poem-1')

    def test_poem_auto_published(self):
        """Test poems are auto-published"""
        self.assertTrue(self.poem.is_published)

    def test_poem_increment_views(self):
        """Test increment_views method"""
        initial_views = self.poem.views
        self.poem.increment_views()
        self.poem.refresh_from_db()
        self.assertEqual(self.poem.views, initial_views + 1)

    def test_poem_get_absolute_url(self):
        """Test get_absolute_url returns correct URL"""
        url = self.poem.get_absolute_url()
        self.assertEqual(url, f'/poem/{self.poem.slug}/')

    def test_poem_ordering(self):
        """Test poems are ordered by published_at descending"""
        poem2 = Poem.objects.create(
            title='Newer Poem',
            content='Newer content',
            author=self.user
        )
        poems = Poem.objects.all()
        self.assertEqual(poems[0], poem2)  # Newer poem should come first


class CommentModelTest(TestCase):
    """Test the Comment model"""

    def setUp(self):
        self.user = User.objects.create_user(
            username='commenter',
            password='testpass123'
        )
        self.poem = Poem.objects.create(
            title='Test Poem',
            content='Test content',
            author=self.user
        )
        self.comment = Comment.objects.create(
            poem=self.poem,
            author=self.user,
            content='This is a test comment.'
        )

    def test_comment_creation(self):
        """Test comment is created successfully"""
        self.assertEqual(self.comment.poem, self.poem)
        self.assertEqual(self.comment.author, self.user)
        self.assertEqual(self.comment.content, 'This is a test comment.')
        self.assertFalse(self.comment.is_approved)

    def test_comment_str_method(self):
        """Test __str__ method returns comment info"""
        expected = f"Comment by {self.user.username} on {self.poem.title}"
        self.assertEqual(str(self.comment), expected)

    def test_comment_ordering(self):
        """Test comments are ordered by created_at ascending"""
        comment2 = Comment.objects.create(
            poem=self.poem,
            author=self.user,
            content='Another comment'
        )
        comments = Comment.objects.all()
        self.assertEqual(comments[0], self.comment)  # Older comment first


class LikeModelTest(TestCase):
    """Test the Like model"""

    def setUp(self):
        self.user = User.objects.create_user(
            username='liker',
            password='testpass123'
        )
        self.poem = Poem.objects.create(
            title='Test Poem',
            content='Test content',
            author=self.user
        )
        self.like = Like.objects.create(
            poem=self.poem,
            user=self.user
        )

    def test_like_creation(self):
        """Test like is created successfully"""
        self.assertEqual(self.like.poem, self.poem)
        self.assertEqual(self.like.user, self.user)

    def test_like_str_method(self):
        """Test __str__ method returns like info"""
        expected = f"{self.user.username} likes {self.poem.title}"
        self.assertEqual(str(self.like), expected)

    def test_like_unique_constraint(self):
        """Test user cannot like the same poem twice"""
        with self.assertRaises(Exception):
            Like.objects.create(
                poem=self.poem,
                user=self.user
            )