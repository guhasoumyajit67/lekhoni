from django.test import TestCase
from django.contrib.auth import get_user_model
from ..forms import CustomUserCreationForm, ProfileUpdateForm

User = get_user_model()


class CustomUserCreationFormTest(TestCase):
    """Test custom user creation form"""

    def test_valid_data(self):
        """Test form with valid data"""
        form = CustomUserCreationForm(data={
            'username': 'newuser',
            'email': 'new@example.com',
            'first_name': 'Test',
            'last_name': 'User',
            'password1': 'StrongPass123',
            'password2': 'StrongPass123',
        })
        self.assertTrue(form.is_valid())

    def test_invalid_data(self):
        """Test form with invalid data"""
        form = CustomUserCreationForm(data={
            'username': 'newuser',
            'email': 'invalid-email',
            'password1': 'StrongPass123',
            'password2': 'DifferentPass',
        })
        self.assertFalse(form.is_valid())

    def test_duplicate_username(self):
        """Test form with duplicate username"""
        User.objects.create_user(username='existinguser', password='pass123')
        form = CustomUserCreationForm(data={
            'username': 'existinguser',
            'email': 'new@example.com',
            'password1': 'StrongPass123',
            'password2': 'StrongPass123',
        })
        self.assertFalse(form.is_valid())


class ProfileUpdateFormTest(TestCase):
    """Test profile update form"""

    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='pass123'
        )

    def test_valid_data(self):
        """Test form with valid data"""
        form = ProfileUpdateForm(data={
            'username': 'testuser',
            'email': 'newemail@example.com',
            'first_name': 'Updated',
            'last_name': 'User',
        }, instance=self.user)
        self.assertTrue(form.is_valid())

    def test_duplicate_username(self):
        """Test form with duplicate username"""
        User.objects.create_user(username='otheruser', password='pass123')
        form = ProfileUpdateForm(data={
            'username': 'otheruser',
            'email': 'test@example.com',
            'first_name': 'Test',
            'last_name': 'User',
        }, instance=self.user)
        self.assertFalse(form.is_valid())

    def test_duplicate_email(self):
        """Test form with duplicate email"""
        User.objects.create_user(
            username='otheruser',
            email='other@example.com',
            password='pass123'
        )
        form = ProfileUpdateForm(data={
            'username': 'testuser',
            'email': 'other@example.com',
            'first_name': 'Test',
            'last_name': 'User',
        }, instance=self.user)
        self.assertFalse(form.is_valid())