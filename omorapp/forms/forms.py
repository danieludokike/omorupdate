from django import forms

from ..models import UserContact, Comment


class LoginForm(forms.Form):
    """USER LOGIN FORM"""
    username = forms.CharField(max_length=50)
    password = forms.CharField(
        max_length=50,
        widget=forms.PasswordInput()
    )


class SignupForm(forms.Form):
    """USER REGISTRATION FORM"""
    username = forms.CharField(max_length=50)
    email = forms.EmailField(max_length=150)
    first_name = forms.CharField(max_length=50, required=False)
    last_name = forms.CharField(max_length=50, required=False)
    password = forms.CharField(
        max_length=50,
        widget=forms.PasswordInput()
    )
    password2 = forms.CharField(
        max_length=50,
        widget=forms.PasswordInput()
    )


class UserContactForm(forms.ModelForm):
    """ USER CONTACT FORM"""
    class Meta:
        model = UserContact
        fields = ('name', 'email', 'subject', 'message')

        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Your name'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Your email'}),
            'subject': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Your subject'}),
            'message': forms.Textarea(attrs={'class': 'form-control', 'rows': 5, 'placeholder': 'Enter your message'})
        }


class CommentForm(forms.ModelForm):
    """USER COMMENT FORM"""
    class Meta:
        model = Comment
        fields = ('write_up',)

