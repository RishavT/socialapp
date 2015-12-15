from django import forms

class LoginForm(forms.Form):
    username = forms.CharField(label='Username', max_length=100)
    password = forms.CharField(max_length=32, widget=forms.PasswordInput)
    
class SignupForm(forms.Form):
    username = forms.CharField(label='Username', max_length=100)
    password1 = forms.CharField(label='password', max_length=32, widget=forms.PasswordInput)
    password2 = forms.CharField(label='repeat password', max_length=32, widget=forms.PasswordInput)
    
class StatusForm(forms.Form):
    data = forms.CharField(label='Enter your status', required=True)

class CommentForm(forms.Form):
    data = forms.CharField(label='Enter your comment', required=True)
