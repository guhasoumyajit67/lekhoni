from django import forms
from .models import Poem, Comment


class PoemForm(forms.ModelForm):
    class Meta:
        model = Poem
        fields = [
            'title', 'content', 'english_translation', 'category',
            'tags', 'featured_image', 'audio_file', 'pen_note',
            'is_published', 'is_featured', 'meta_description'
        ]
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'কবিতার শিরোনাম'}),
            'content': forms.Textarea(attrs={'class': 'form-control', 'rows': 12, 'placeholder': 'আপনার কবিতা লিখুন...'}),
            'english_translation': forms.Textarea(attrs={'class': 'form-control', 'rows': 5, 'placeholder': 'ইংরেজি অনুবাদ (ঐচ্ছিক)'}),
            'category': forms.Select(attrs={'class': 'form-select'}),
            'tags': forms.SelectMultiple(attrs={'class': 'form-select', 'size': 5}),
            'pen_note': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'লেখনীর কথা - এই কবিতা লেখার অনুপ্রেরণা...'}),
            'meta_description': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'SEO বিবরণ (সর্বোচ্চ ১৬০ অক্ষর)'}),
        }


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'আপনার মন্তব্য লিখুন...'}),
        }