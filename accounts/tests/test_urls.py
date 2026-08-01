from django.test import TestCase
from django.urls import reverse, resolve


class AccountsUrlsTest(TestCase):
    """Test accounts app URLs"""

    def test_signup_url(self):
        """Test signup URL resolves correctly"""
        url = reverse('signup')
        self.assertEqual(url, '/accounts/signup/')
        self.assertEqual(resolve(url).view_name, 'signup')

    def test_login_url(self):
        """Test login URL resolves correctly"""
        url = reverse('login')
        self.assertEqual(url, '/accounts/login/')
        self.assertEqual(resolve(url).view_name, 'login')

    def test_profile_url(self):
        """Test profile URL resolves correctly"""
        # ✅ FIXED: Removed 'accounts:'
        url = reverse('profile')
        self.assertEqual(url, '/accounts/profile/')
        self.assertEqual(resolve(url).view_name, 'profile')

    def test_profile_update_url(self):
        """Test profile update URL resolves correctly"""
        # ✅ FIXED: Removed 'accounts:'
        url = reverse('profile_update')
        self.assertEqual(url, '/accounts/profile/update/')
        self.assertEqual(resolve(url).view_name, 'profile_update')

    def test_logout_url(self):
        """Test logout URL resolves correctly"""
        url = reverse('logout')
        self.assertEqual(url, '/accounts/logout/')
        self.assertEqual(resolve(url).view_name, 'logout')