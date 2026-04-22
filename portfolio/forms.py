"""portfolio/forms.py"""
from django import forms
from django.contrib.auth.forms import PasswordChangeForm
from .models import Profile, Skill, Project, Experience, Certification


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        exclude = ['user']
        widgets = {
            'bio': forms.Textarea(attrs={'rows': 4}),
            'tagline': forms.TextInput(attrs={'placeholder': 'your tagline here'}),
            'location': forms.TextInput(attrs={'placeholder': 'City, Country'}),
            'github': forms.URLInput(attrs={'placeholder': 'https://github.com/username'}),
            'linkedin': forms.URLInput(attrs={'placeholder': 'https://linkedin.com/in/username'}),
            'twitter': forms.URLInput(attrs={'placeholder': 'https://twitter.com/username'}),
            'website': forms.URLInput(attrs={'placeholder': 'https://yoursite.dev'}),
        }


class SkillForm(forms.ModelForm):
    class Meta:
        model = Skill
        exclude = ['user']
        widgets = {
            'proficiency': forms.NumberInput(attrs={'min': 0, 'max': 100, 'placeholder': '85'}),
            'icon_class': forms.TextInput(attrs={'placeholder': 'devicon-python-plain'}),
        }


class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        exclude = ['user']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
            'date': forms.DateInput(attrs={'type': 'date'}),
            'tech_used': forms.TextInput(attrs={'placeholder': 'Python, Django, PostgreSQL'}),
            'github_link': forms.URLInput(attrs={'placeholder': 'https://github.com/...'}),
            'live_link': forms.URLInput(attrs={'placeholder': 'https://...'}),
        }


class ExperienceForm(forms.ModelForm):
    class Meta:
        model = Experience
        exclude = ['user']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
            'start_date': forms.DateInput(attrs={'type': 'date'}),
            'end_date': forms.DateInput(attrs={'type': 'date'}),
        }


class CertificationForm(forms.ModelForm):
    class Meta:
        model = Certification
        exclude = ['user']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
            'expiry_date': forms.DateInput(attrs={'type': 'date'}),
            'credential_url': forms.URLInput(attrs={'placeholder': 'https://verify.credly.com/...'}),
        }


UserPasswordChangeForm = PasswordChangeForm
