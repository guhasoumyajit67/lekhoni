from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model

User = get_user_model()


class SignUpViewTest(TestCase):
    """Test user registration"""

    def setUp(self):
        self.url = reverse('signup')
        self.valid_data = {
            'username': 'newuser',
            'email': 'new@example.com',
            'password1': 'StrongPass123',
            'password2': 'StrongPass123',
        }

    def test_signup_page_status(self):
        """Test signup page loads successfully"""
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'registration/signup.html')

    def test_signup_success(self):
        """Test user can sign up successfully"""
        response = self.client.post(self.url, self.valid_data)
        self.assertTrue(User.objects.filter(username='newuser').exists())
        self.assertRedirects(response, reverse('login'))

    def test_signup_invalid_data(self):
        """Test signup with invalid data"""
        invalid_data = self.valid_data.copy()
        invalid_data['password2'] = 'DifferentPass'
        response = self.client.post(self.url, invalid_data)
        self.assertFalse(User.objects.filter(username='newuser').exists())
        self.assertEqual(response.status_code, 200)

    def test_signup_duplicate_username(self):
        """Test cannot create user with duplicate username"""
        User.objects.create_user(username='existinguser', password='pass123')
        data = {
            'username': 'existinguser',
            'email': 'test@example.com',
            'password1': 'Pass123456',
            'password2': 'Pass123456',
        }
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, 200)


class LoginViewTest(TestCase):
    """Test user login"""

    def setUp(self):
        self.user = User.objects.create_user(
            username='loginuser',
            password='loginpass123'
        )
        self.login_url = reverse('login')
        # ✅ FIXED: Removed 'poems:'
        self.home_url = reverse('home')

    def test_login_page_status(self):
        """Test login page loads successfully"""
        response = self.client.get(self.login_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'registration/login.html')

    def test_login_success(self):
        """Test user can login successfully"""
        response = self.client.post(self.login_url, {
            'username': 'loginuser',
            'password': 'loginpass123'
        })
        self.assertRedirects(response, self.home_url)
        response = self.client.get(self.home_url)
        self.assertTrue(response.context['user'].is_authenticated)

    def test_login_invalid_username(self):
        """Test login with invalid username"""
        response = self.client.post(self.login_url, {
            'username': 'wronguser',
            'password': 'loginpass123'
        })
        self.assertEqual(response.status_code, 200)

    def test_login_invalid_password(self):
        """Test login with invalid password"""
        response = self.client.post(self.login_url, {
            'username': 'loginuser',
            'password': 'wrongpass'
        })
        self.assertEqual(response.status_code, 200)


class ProfileViewTest(TestCase):
    """Test user profile"""

    def setUp(self):
        self.user = User.objects.create_user(
            username='profileuser',
            email='profile@example.com',
            password='profilepass123'
        )
        # ✅ FIXED: Removed 'accounts:'
        self.profile_url = reverse('profile')
        self.login_url = reverse('login')

    def test_profile_redirects_if_not_logged_in(self):
        """Test profile page redirects to login if not authenticated"""
        response = self.client.get(self.profile_url)
        self.assertRedirects(response, f'{self.login_url}?next={self.profile_url}')

    def test_profile_page_authenticated(self):
        """Test profile page loads for authenticated user"""
        self.client.login(username='profileuser', password='profilepass123')
        response = self.client.get(self.profile_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'registration/profile.html')


class ProfileUpdateViewTest(TestCase):
    """Test profile update"""

    def setUp(self):
        self.user = User.objects.create_user(
            username='updateuser',
            password='updatepass123',
            email='old@example.com'
        )
        # ✅ FIXED: Removed 'accounts:'
        self.update_url = reverse('profile_update')
        self.login_url = reverse('login')

    def test_profile_update_redirects_if_not_logged_in(self):
        """Test update page redirects to login if not authenticated"""
        response = self.client.get(self.update_url)
        self.assertRedirects(response, f'{self.login_url}?next={self.update_url}')

    def test_profile_update_success(self):
        """Test user can update profile"""
        self.client.login(username='updateuser', password='updatepass123')
        response = self.client.post(self.update_url, {
            'username': 'updateuser',
            'email': 'newemail@example.com',
            'first_name': 'Updated',
            'last_name': 'User',
        })
        self.assertRedirects(response, reverse('profile'))
        self.user.refresh_from_db()
        self.assertEqual(self.user.email, 'newemail@example.com')
        self.assertEqual(self.user.first_name, 'Updated')


class LogoutViewTest(TestCase):
    """Test user logout"""

    def setUp(self):
        self.user = User.objects.create_user(
            username='logoutuser',
            password='logoutpass123'
        )
        self.logout_url = reverse('logout')
        # ✅ FIXED: Removed 'poems:'
        self.home_url = reverse('home')

    def test_logout_success(self):
        """Test user can logout successfully"""
        self.client.login(username='logoutuser', password='logoutpass123')
        response = self.client.post(self.logout_url)
        self.assertRedirects(response, self.home_url)
        response = self.client.get(self.home_url)
        self.assertFalse(response.context['user'].is_authenticated)