from .models import Post
from django import forms


#class for creating a new post

class PostCreateForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('title', 'image','caption')