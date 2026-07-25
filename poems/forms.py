from django import forms
from .models import Poem, Comment


class PoemForm(forms.ModelForm):
    class Meta:
        model = Poem
        fields = [
            'title', 'content', 'category', 
            'featured_image', 'audio_file'
        ]
        labels = {
            'title': 'শিরোনাম',
            'content': 'কবিতা',
            'category': 'ক্যাটাগরি',
            'featured_image': 'প্রচ্ছদ ছবি',
            'audio_file': 'অডিও ফাইল',
        }
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control', 
                'placeholder': 'কবিতার শিরোনাম'
            }),
            'content': forms.Textarea(attrs={
                'class': 'form-control', 
                'rows': 12, 
                'placeholder': 'আপনার কবিতা লিখুন...'
            }),
            'category': forms.Select(attrs={
                'class': 'form-select'
            }),
            'featured_image': forms.FileInput(attrs={
                'class': 'form-control'
            }),
            'audio_file': forms.FileInput(attrs={
                'class': 'form-control'
            }),
        }


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']
        labels = {
            'content': 'মন্তব্য',
        }
        widgets = {
            'content': forms.Textarea(attrs={
                'class': 'form-control', 
                'rows': 3, 
                'placeholder': 'আপনার মন্তব্য লিখুন...'
            }),
        }