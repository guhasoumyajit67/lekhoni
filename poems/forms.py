from django import forms
from .models import Poem, Comment


class PoemForm(forms.ModelForm):
    class Meta:
        model = Poem
        fields = [
            'title', 'content', 'category'
        ]
        labels = {
            'title': 'শিরোনাম',
            'content': 'কবিতা',
            'category': 'বিভাগ',
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



class CommentEditForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']
        labels = {
            'content': 'মন্তব্য সম্পাদনা',
        }
        widgets = {
            'content': forms.Textarea(attrs={
                'class': 'form-control', 
                'rows': 3,
                'placeholder': 'আপনার মন্তব্য সম্পাদনা করুন...'
            }),
        }