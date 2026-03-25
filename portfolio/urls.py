"""portfolio/urls.py"""
from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

app_name = 'portfolio'

urlpatterns = [
    # Auth
    path('login/', auth_views.LoginView.as_view(template_name='portfolio/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),

    # Core pages
    path('', views.dashboard, name='home'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('profile/', views.profile_view, name='profile'),

    # Skills
    path('skills/', views.skill_list, name='skill_list'),
    path('skills/<int:pk>/edit/', views.skill_edit, name='skill_edit'),
    path('skills/<int:pk>/delete/', views.skill_delete, name='skill_delete'),

    # Projects
    path('projects/', views.project_list, name='project_list'),
    path('projects/<int:pk>/edit/', views.project_edit, name='project_edit'),
    path('projects/<int:pk>/delete/', views.project_delete, name='project_delete'),

    # Experience
    path('experience/', views.experience_list, name='experience_list'),
    path('experience/<int:pk>/edit/', views.experience_edit, name='experience_edit'),
    path('experience/<int:pk>/delete/', views.experience_delete, name='experience_delete'),

    # Certifications
    path('certifications/', views.certification_list, name='certification_list'),
    path('certifications/<int:pk>/edit/', views.certification_edit, name='certification_edit'),
    path('certifications/<int:pk>/delete/', views.certification_delete, name='certification_delete'),
]
