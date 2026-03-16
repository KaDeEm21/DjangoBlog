from django import forms
from django.contrib.auth import get_user_model
from django.core.validators import MinLengthValidator, RegexValidator

from .models import Comment, Post, Profile

User = get_user_model()

INPUT_CLASS = 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500'


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'image_url', 'content', 'category', 'tags']
        widgets = {
            'title': forms.TextInput(attrs={'class': INPUT_CLASS}),
            'image_url': forms.URLInput(attrs={'class': INPUT_CLASS, 'placeholder': 'https://...'}),
            'content': forms.Textarea(attrs={'class': INPUT_CLASS, 'rows': 10}),
            'category': forms.Select(attrs={'class': INPUT_CLASS}),
            'tags': forms.CheckboxSelectMultiple(attrs={'class': 'space-y-2'}),
        }

    def clean_content(self):
        content = self.cleaned_data['content']
        if len(content.strip()) < 50:
            raise forms.ValidationError('Treść musi mieć co najmniej 50 znaków')
        return content


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['name', 'email', 'content']
        widgets = {
            'name': forms.TextInput(attrs={'class': INPUT_CLASS}),
            'email': forms.EmailInput(attrs={'class': INPUT_CLASS}),
            'content': forms.Textarea(attrs={'class': INPUT_CLASS, 'rows': 4}),
        }

    def __init__(self, *args, **kwargs):
        self.post = kwargs.pop('post', None)
        super().__init__(*args, **kwargs)

    def clean_email(self):
        return self.cleaned_data['email'].strip().lower()

    def clean_content(self):
        content = self.cleaned_data['content']
        if len(content.strip()) < 5:
            raise forms.ValidationError('Komentarz musi mieć co najmniej 5 znaków')
        return content

    def clean(self):
        cleaned_data = super().clean()
        email = cleaned_data.get('email')
        if self.post and email and Comment.objects.filter(post=self.post, email=email).exists():
            self.add_error('email', 'Ten email już skomentował ten post')
        return cleaned_data


class RegistrationForm(forms.ModelForm):
    username = forms.CharField(
        max_length=150,
        widget=forms.TextInput(attrs={'class': INPUT_CLASS}),
        label='Nazwa użytkownika',
    )
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': INPUT_CLASS}))
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': INPUT_CLASS}),
        validators=[
            MinLengthValidator(8, 'Hasło musi mieć co najmniej 8 znaków'),
            RegexValidator(r'(?=.*[a-z])', 'Hasło musi zawierać co najmniej jedną małą literę'),
            RegexValidator(r'(?=.*[A-Z])', 'Hasło musi zawierać co najmniej jedną wielką literę'),
            RegexValidator(r'(?=.*\d)', 'Hasło musi zawierać co najmniej jedną cyfrę'),
        ],
        label='Hasło',
    )
    password_confirm = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': INPUT_CLASS}),
        label='Powtórz hasło',
    )

    class Meta:
        model = User
        fields = ['username', 'email']

    def clean_password_confirm(self):
        password = self.cleaned_data.get('password')
        password_confirm = self.cleaned_data.get('password_confirm')
        if password and password_confirm and password != password_confirm:
            raise forms.ValidationError('Hasła nie są takie same')
        return password_confirm

    def clean_email(self):
        email = self.cleaned_data['email'].strip().lower()
        if User.objects.filter(email__iexact=email).exists():
            raise forms.ValidationError('Email jest już zajęty')
        return email

    def clean_username(self):
        username = self.cleaned_data['username'].strip()
        if User.objects.filter(username__iexact=username).exists():
            raise forms.ValidationError('Nazwa użytkownika jest już zajęta')
        return username

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        user.set_password(self.cleaned_data['password'])
        if commit:
            user.save()
        return user


class LoginForm(forms.Form):
    username = forms.CharField(max_length=150, widget=forms.TextInput(attrs={'class': INPUT_CLASS}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': INPUT_CLASS}))


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['avatar', 'bio', 'website', 'location']
        widgets = {
            'avatar': forms.URLInput(attrs={'class': INPUT_CLASS, 'placeholder': 'https://...'}),
            'bio': forms.Textarea(attrs={'class': INPUT_CLASS, 'rows': 4}),
            'website': forms.URLInput(attrs={'class': INPUT_CLASS, 'placeholder': 'https://...'}),
            'location': forms.TextInput(attrs={'class': INPUT_CLASS}),
        }
