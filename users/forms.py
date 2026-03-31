from django import forms
from django.contrib.auth.models import User
from .models import Profile



class UserEditForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email')

class ProfileEditForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('photo',)




#LOGIN FORM
class LoginForm(forms.Form):
    username =forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)


#REGISTRATION FORM
class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(label='Password' , widget=forms.PasswordInput)
    password2 = forms.CharField(label='Confirm Password', widget=forms.PasswordInput)
    class Meta:
        model = User
        fields = ('username' , 'email', 'first_name')

    def check_password(self):
        if self.cleaned_data['password']!= self.cleaned_data['password2']:
            raise forms.ValidationError('Passwords does not matched.')
        return self.cleaned_data['password2']
    
    def clean_username(self):
        username = self.cleaned_data.get('username')

        if User.objects.filter(username=username).exists():
            raise forms.ValidationError("Username is already taken")

        return username
    

