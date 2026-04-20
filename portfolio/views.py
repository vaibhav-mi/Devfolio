"""portfolio/views.py"""
import json
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import update_session_auth_hash
from django.contrib import messages
from django.db.models import Count
from django.core.serializers.json import DjangoJSONEncoder

from .models import Profile, Skill, Project, Experience, Certification
from .forms import (
    ProfileForm, SkillForm, ProjectForm,
    ExperienceForm, CertificationForm, UserPasswordChangeForm,
)
from django import forms as django_forms


def _get_form_fields_with_widget_types(form):
    """Enhance form fields with widget type information for templates."""
    form_fields_data = []
    for field in form:
        widget_type = field.field.widget.__class__.__name__
        is_select = isinstance(field.field.widget, django_forms.Select)
        form_fields_data.append({
            'field': field,
            'widget_type': widget_type,
            'is_select': is_select,
        })
    return form_fields_data


def _base_context(request, active_page):
    """Shared context injected into every page."""
    profile, _ = Profile.objects.get_or_create(user=request.user)
    return {
        'active_page': active_page,
        'profile': profile,
        'nav_counts': {
            'skills': request.user.skills.count(),
            'projects': request.user.projects.count(),
            'certifications': request.user.certifications.count(),
        }
    }


# ── Dashboard ──────────────────────────────────────────────────────────────────
@login_required
def dashboard(request):
    user = request.user
    ctx = _base_context(request, 'dashboard')

    ctx['counts'] = {
        'skills': user.skills.count(),
        'projects': user.projects.count(),
        'experiences': user.experiences.count(),
        'certifications': user.certifications.count(),
    }

    top8 = list(user.skills.order_by('-proficiency')[:8].values('name', 'proficiency', 'category'))
    ctx['radar_labels'] = json.dumps([s['name'] for s in top8])
    ctx['radar_values'] = json.dumps([s['proficiency'] for s in top8])

    cat_qs = (user.skills.values('category').annotate(count=Count('id')).order_by('category'))
    ctx['bar_labels'] = json.dumps([i['category'].capitalize() for i in cat_qs])
    ctx['bar_values'] = json.dumps([i['count'] for i in cat_qs])

    ctx['recent_projects'] = user.projects.order_by('-date')[:5]
    ctx['featured_projects'] = user.projects.filter(featured=True)[:3]

    skills_data = list(user.skills.values('name', 'category', 'proficiency', 'level'))
    projects_data = []
    for p in user.projects.all():
        projects_data.append({
            'id': p.pk,
            'title': p.title,
            'description': p.description,
            'tech': p.tech_list(),
            'status': p.status,
            'featured': p.featured,
            'github_link': p.github_link,
            'live_link': p.live_link,
            'thumbnail': p.thumbnail.url if p.thumbnail else '',
        })

    ctx['skills_json'] = json.dumps(skills_data, cls=DjangoJSONEncoder)
    ctx['projects_json'] = json.dumps(projects_data, cls=DjangoJSONEncoder)
    return render(request, 'portfolio/dashboard.html', ctx)


# ── Profile ────────────────────────────────────────────────────────────────────
@login_required
def profile_view(request):
    profile, _ = Profile.objects.get_or_create(user=request.user)
    ctx = _base_context(request, 'profile')
    ctx['profile_form'] = ProfileForm(instance=profile)
    ctx['password_form'] = UserPasswordChangeForm(user=request.user)
    ctx['open_modal'] = ''

    if request.method == 'POST':
        action = request.POST.get('action')
        if action == 'update_profile':
            form = ProfileForm(request.POST, request.FILES, instance=profile)
            if form.is_valid():
                form.save()
                messages.success(request, 'Profile updated successfully.')
                return redirect('portfolio:profile')
            ctx['profile_form'] = form
            messages.error(request, 'Please correct the errors below.')
        elif action == 'change_password':
            form = UserPasswordChangeForm(user=request.user, data=request.POST)
            if form.is_valid():
                form.save()
                update_session_auth_hash(request, form.user)
                messages.success(request, 'Password changed successfully.')
                return redirect('portfolio:profile')
            ctx['password_form'] = form
            ctx['open_modal'] = 'password'
            messages.error(request, 'Please correct the password errors.')

    return render(request, 'portfolio/profile.html', ctx)


# ── Skills ─────────────────────────────────────────────────────────────────────
@login_required
def skill_list(request):
    ctx = _base_context(request, 'skills')
    ctx['skills'] = request.user.skills.all()
    form = SkillForm()
    ctx['form_fields'] = _get_form_fields_with_widget_types(form)
    ctx['form'] = form
    ctx['open_modal'] = False

    if request.method == 'POST':
        form = SkillForm(request.POST)
        if form.is_valid():
            skill = form.save(commit=False)
            skill.user = request.user
            skill.save()
            messages.success(request, f"Skill '{skill.name}' added.")
            return redirect('portfolio:skill_list')
        ctx['form'] = form
        ctx['form_fields'] = _get_form_fields_with_widget_types(form)
        ctx['open_modal'] = True
        messages.error(request, 'Please fix the errors below.')

    return render(request, 'portfolio/skill_list.html', ctx)


@login_required
def skill_edit(request, pk):
    skill = get_object_or_404(Skill, pk=pk, user=request.user)
    ctx = _base_context(request, 'skills')
    ctx['form'] = SkillForm(instance=skill)
    ctx['form_fields'] = _get_form_fields_with_widget_types(ctx['form'])
    ctx['object'] = skill

    if request.method == 'POST':
        form = SkillForm(request.POST, instance=skill)
        if form.is_valid():
            form.save()
            messages.success(request, 'Skill updated.')
            return redirect('portfolio:skill_list')
        ctx['form'] = form
        ctx['form_fields'] = _get_form_fields_with_widget_types(form)

    return render(request, 'portfolio/skill_form.html', ctx)


@login_required
def skill_delete(request, pk):
    skill = get_object_or_404(Skill, pk=pk, user=request.user)
    ctx = _base_context(request, 'skills')
    ctx['object'] = skill
    ctx['object_type'] = 'Skill'
    ctx['cancel_url'] = 'portfolio:skill_list'

    if request.method == 'POST':
        skill.delete()
        messages.success(request, 'Skill deleted.')
        return redirect('portfolio:skill_list')

    return render(request, 'portfolio/confirm_delete.html', ctx)


# ── Projects ───────────────────────────────────────────────────────────────────
@login_required
def project_list(request):
    ctx = _base_context(request, 'projects')
    ctx['projects'] = request.user.projects.all()
    form = ProjectForm()
    ctx['form'] = form
    ctx['form_fields'] = _get_form_fields_with_widget_types(form)
    ctx['open_modal'] = False

    if request.method == 'POST':
        form = ProjectForm(request.POST, request.FILES)
        if form.is_valid():
            project = form.save(commit=False)
            project.user = request.user
            project.save()
            messages.success(request, f"Project '{project.title}' added.")
            return redirect('portfolio:project_list')
        ctx['form'] = form
        ctx['form_fields'] = _get_form_fields_with_widget_types(form)
        ctx['open_modal'] = True
        messages.error(request, 'Please fix the errors below.')

    return render(request, 'portfolio/project_list.html', ctx)


@login_required
def project_edit(request, pk):
    project = get_object_or_404(Project, pk=pk, user=request.user)
    ctx = _base_context(request, 'projects')
    ctx['form'] = ProjectForm(instance=project)
    ctx['form_fields'] = _get_form_fields_with_widget_types(ctx['form'])
    ctx['object'] = project

    if request.method == 'POST':
        form = ProjectForm(request.POST, request.FILES, instance=project)
        if form.is_valid():
            form.save()
            messages.success(request, 'Project updated.')
            return redirect('portfolio:project_list')
        ctx['form'] = form
        ctx['form_fields'] = _get_form_fields_with_widget_types(form)

    return render(request, 'portfolio/project_form.html', ctx)


@login_required
def project_delete(request, pk):
    project = get_object_or_404(Project, pk=pk, user=request.user)
    ctx = _base_context(request, 'projects')
    ctx['object'] = project
    ctx['object_type'] = 'Project'
    ctx['cancel_url'] = 'portfolio:project_list'

    if request.method == 'POST':
        project.delete()
        messages.success(request, 'Project deleted.')
        return redirect('portfolio:project_list')

    return render(request, 'portfolio/confirm_delete.html', ctx)


# ── Experience ─────────────────────────────────────────────────────────────────
@login_required
def experience_list(request):
    ctx = _base_context(request, 'experience')
    ctx['experiences'] = request.user.experiences.all()
    form = ExperienceForm()
    ctx['form'] = form
    ctx['form_fields'] = _get_form_fields_with_widget_types(form)
    ctx['open_modal'] = False

    if request.method == 'POST':
        form = ExperienceForm(request.POST)
        if form.is_valid():
            exp = form.save(commit=False)
            exp.user = request.user
            exp.save()
            messages.success(request, 'Experience added.')
            return redirect('portfolio:experience_list')
        ctx['form'] = form
        ctx['form_fields'] = _get_form_fields_with_widget_types(form)
        ctx['open_modal'] = True
        messages.error(request, 'Please fix the errors below.')

    return render(request, 'portfolio/experience_list.html', ctx)


@login_required
def experience_edit(request, pk):
    experience = get_object_or_404(Experience, pk=pk, user=request.user)
    ctx = _base_context(request, 'experience')
    ctx['form'] = ExperienceForm(instance=experience)
    ctx['form_fields'] = _get_form_fields_with_widget_types(ctx['form'])
    ctx['object'] = experience

    if request.method == 'POST':
        form = ExperienceForm(request.POST, instance=experience)
        if form.is_valid():
            form.save()
            messages.success(request, 'Experience updated.')
            return redirect('portfolio:experience_list')
        ctx['form'] = form
        ctx['form_fields'] = _get_form_fields_with_widget_types(form)

    return render(request, 'portfolio/experience_form.html', ctx)


@login_required
def experience_delete(request, pk):
    experience = get_object_or_404(Experience, pk=pk, user=request.user)
    ctx = _base_context(request, 'experience')
    ctx['object'] = experience
    ctx['object_type'] = 'Experience'
    ctx['cancel_url'] = 'portfolio:experience_list'

    if request.method == 'POST':
        experience.delete()
        messages.success(request, 'Experience deleted.')
        return redirect('portfolio:experience_list')

    return render(request, 'portfolio/confirm_delete.html', ctx)


# ── Certifications ─────────────────────────────────────────────────────────────
@login_required
def certification_list(request):
    ctx = _base_context(request, 'certifications')
    ctx['certifications'] = request.user.certifications.all()
    form = CertificationForm()
    ctx['form'] = form
    ctx['form_fields'] = _get_form_fields_with_widget_types(form)
    ctx['open_modal'] = False

    if request.method == 'POST':
        form = CertificationForm(request.POST, request.FILES)
        if form.is_valid():
            cert = form.save(commit=False)
            cert.user = request.user
            cert.save()
            messages.success(request, f"Certification '{cert.title}' added.")
            return redirect('portfolio:certification_list')
        ctx['form'] = form
        ctx['form_fields'] = _get_form_fields_with_widget_types(form)
        ctx['open_modal'] = True
        messages.error(request, 'Please fix the errors below.')

    return render(request, 'portfolio/certification_list.html', ctx)


@login_required
def certification_edit(request, pk):
    certification = get_object_or_404(Certification, pk=pk, user=request.user)
    ctx = _base_context(request, 'certifications')
    ctx['form'] = CertificationForm(instance=certification)
    ctx['form_fields'] = _get_form_fields_with_widget_types(ctx['form'])
    ctx['object'] = certification

    if request.method == 'POST':
        form = CertificationForm(request.POST, request.FILES, instance=certification)
        if form.is_valid():
            form.save()
            messages.success(request, 'Certification updated.')
            return redirect('portfolio:certification_list')
        ctx['form'] = form
        ctx['form_fields'] = _get_form_fields_with_widget_types(form)

    return render(request, 'portfolio/certification_form.html', ctx)


@login_required
def certification_delete(request, pk):
    certification = get_object_or_404(Certification, pk=pk, user=request.user)
    ctx = _base_context(request, 'certifications')
    ctx['object'] = certification
    ctx['object_type'] = 'Certification'
    ctx['cancel_url'] = 'portfolio:certification_list'

    if request.method == 'POST':
        certification.delete()
        messages.success(request, 'Certification deleted.')
        return redirect('portfolio:certification_list')

    return render(request, 'portfolio/confirm_delete.html', ctx)
# ── End ─────────────────────────────────────────────────────────────
