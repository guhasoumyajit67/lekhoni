from django.test import TestCase
from django.contrib.auth import get_user_model

User = get_user_model()


class CustomUserModelTest(TestCase):
    """Test the CustomUser model"""

    def setUp(self):
        """Create a test user"""
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123',
            first_name='Test',
            last_name='User'
        )

    def test_user_creation(self):
        """Test user is created successfully"""
        self.assertEqual(self.user.username, 'testuser')
        self.assertEqual(self.user.email, 'test@example.com')
        self.assertEqual(self.user.first_name, 'Test')
        self.assertEqual(self.user.last_name, 'User')
        self.assertTrue(self.user.check_password('testpass123'))
        self.assertTrue(self.user.is_active)

    def test_user_str_method(self):
        """Test __str__ method returns username"""
        self.assertEqual(str(self.user), 'testuser')

    def test_get_full_name(self):
        """Test get_full_name method"""
        self.assertEqual(self.user.get_full_name(), 'Test User')
        
        # Test without first/last name
        user2 = User.objects.create_user(
            username='user2',
            password='pass123'
        )
        self.assertEqual(user2.get_full_name(), 'user2')

    def test_poem_count_property(self):
        """Test poem_count property returns 0 initially"""
        self.assertEqual(self.user.poem_count, 0)

    def test_total_views_property(self):
        """Test total_views property returns 0 initially"""
        self.assertEqual(self.user.total_views, 0)