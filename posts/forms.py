from .models import Post
from django import forms


#class for creating a new post

class PostCreateForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('title', 'image','caption')
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'w-full px-3 py-2 border rounded-lg focus:ring-2 focus:ring-purple-400'
            }),
            'caption': forms.Textarea(attrs={
                'class': 'w-full px-3 py-2 border rounded-lg focus:ring-2 focus:ring-purple-400'
            }),
        }