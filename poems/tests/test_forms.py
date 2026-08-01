from django.test import TestCase
from django.contrib.auth import get_user_model
from poems.models import Poem, Category, Comment
from poems.forms import PoemForm, CommentForm, CommentEditForm

User = get_user_model()


class PoemFormTest(TestCase):
    """Test the PoemForm"""

    def setUp(self):
        """Create a test user and category"""
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        self.category = Category.objects.create(
            name='Romantic',
            slug='romantic'
        )

    def test_poem_form_valid_data(self):
        """Test PoemForm with valid data"""
        form = PoemForm(data={
            'title': 'My Test Poem',
            'content': 'This is a test poem content.',
            'category': self.category.id,
        })
        self.assertTrue(form.is_valid())

    def test_poem_form_missing_title(self):
        """Test PoemForm with missing title"""
        form = PoemForm(data={
            'content': 'This is a test poem content.',
            'category': self.category.id,
        })
        self.assertFalse(form.is_valid())
        self.assertIn('title', form.errors)

    def test_poem_form_missing_content(self):
        """Test PoemForm with missing content"""
        form = PoemForm(data={
            'title': 'My Test Poem',
            'category': self.category.id,
        })
        self.assertFalse(form.is_valid())
        self.assertIn('content', form.errors)

    def test_poem_form_missing_category(self):
        """Test PoemForm with missing category"""
        form = PoemForm(data={
            'title': 'My Test Poem',
            'content': 'This is a test poem content.',
        })
        # ✅ FIXED: Category is optional (null=True, blank=True), so form IS valid
        self.assertTrue(form.is_valid())
        # Ensure category is not in errors (since it's optional)
        self.assertNotIn('category', form.errors)

    def test_poem_form_widgets(self):
        """Test PoemForm widgets have correct CSS classes"""
        form = PoemForm()
        self.assertEqual(form.fields['title'].widget.attrs.get('class'), 'form-control')
        self.assertEqual(form.fields['content'].widget.attrs.get('class'), 'form-control')
        self.assertEqual(form.fields['category'].widget.attrs.get('class'), 'form-select')


class CommentFormTest(TestCase):
    """Test the CommentForm"""

    def test_comment_form_valid_data(self):
        """Test CommentForm with valid data"""
        form = CommentForm(data={
            'content': 'This is a test comment.',
        })
        self.assertTrue(form.is_valid())

    def test_comment_form_empty_content(self):
        """Test CommentForm with empty content"""
        form = CommentForm(data={
            'content': '',
        })
        self.assertFalse(form.is_valid())
        self.assertIn('content', form.errors)

    def test_comment_form_widgets(self):
        """Test CommentForm widgets have correct CSS classes"""
        form = CommentForm()
        self.assertEqual(form.fields['content'].widget.attrs.get('class'), 'form-control')
        self.assertEqual(form.fields['content'].widget.attrs.get('rows'), 3)


class CommentEditFormTest(TestCase):
    """Test the CommentEditForm"""

    def test_comment_edit_form_valid_data(self):
        """Test CommentEditForm with valid data"""
        form = CommentEditForm(data={
            'content': 'This is an edited comment.',
        })
        self.assertTrue(form.is_valid())

    def test_comment_edit_form_empty_content(self):
        """Test CommentEditForm with empty content"""
        form = CommentEditForm(data={
            'content': '',
        })
        self.assertFalse(form.is_valid())
        self.assertIn('content', form.errors)

    def test_comment_edit_form_widgets(self):
        """Test CommentEditForm widgets have correct CSS classes"""
        form = CommentEditForm()
        self.assertEqual(form.fields['content'].widget.attrs.get('class'), 'form-control')
        self.assertEqual(form.fields['content'].widget.attrs.get('rows'), 3)