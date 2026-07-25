from django.views.generic import CreateView, DetailView, UpdateView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import get_user_model
from django.contrib import messages

from .forms import CustomUserCreationForm, ProfileUpdateForm

User = get_user_model()


class SignUpView(CreateView):
    """
    User registration/signup view
    """
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'registration/signup.html'
    
    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, 'আপনার অ্যাকাউন্ট সফলভাবে তৈরি হয়েছে! এখন লগইন করুন।')
        return response


class ProfileView(LoginRequiredMixin, DetailView):
    """
    User profile view
    """
    model = User
    template_name = 'registration/profile.html'
    context_object_name = 'user'

    def get_object(self):
        return self.request.user


class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    """
    User profile update view
    """
    model = User
    form_class = ProfileUpdateForm
    template_name = 'registration/profile_update.html'
    success_url = reverse_lazy('accounts:profile')
    
    def get_object(self):
        return self.request.user
    
    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, 'আপনার প্রোফাইল সফলভাবে আপডেট হয়েছে!')
        return response