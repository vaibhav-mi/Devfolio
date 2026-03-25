"""portfolio/admin.py"""
from django.contrib import admin
from .models import Profile, Skill, Project, Experience, Certification


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'tagline', 'location']
    list_filter = ['location']
    search_fields = ['user__username', 'user__email', 'tagline']


@admin.register(Skill)
class SkillAdmin(admin.ModelAdmin):
    list_display = ['name', 'user', 'category', 'proficiency', 'level']
    list_filter = ['category', 'level']
    search_fields = ['name', 'user__username']


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ['title', 'user', 'status', 'featured', 'date']
    list_filter = ['status', 'featured']
    search_fields = ['title', 'user__username']


@admin.register(Experience)
class ExperienceAdmin(admin.ModelAdmin):
    list_display = ['role', 'company', 'user', 'start_date', 'end_date', 'is_current']
    list_filter = ['is_current']
    search_fields = ['role', 'company', 'user__username']


@admin.register(Certification)
class CertificationAdmin(admin.ModelAdmin):
    list_display = ['title', 'issuer', 'user', 'date', 'expiry_date']
    list_filter = ['issuer']
    search_fields = ['title', 'issuer', 'user__username', 'credential_id']
