"""portfolio/models.py"""
from datetime import date
from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    tagline = models.CharField(max_length=160, blank=True)
    bio = models.TextField(blank=True)
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)
    github = models.URLField(blank=True)
    linkedin = models.URLField(blank=True)
    twitter = models.URLField(blank=True)
    website = models.URLField(blank=True)
    resume = models.FileField(upload_to='resumes/', blank=True, null=True)
    location = models.CharField(max_length=120, blank=True)

    def __str__(self):
        return f"{self.user.username}'s Profile"


class Skill(models.Model):
    CATEGORY_CHOICES = [
        ('frontend', 'Frontend'),
        ('backend', 'Backend'),
        ('database', 'Database'),
        ('devops', 'DevOps'),
        ('mobile', 'Mobile'),
        ('tools', 'Tools'),
        ('other', 'Other'),
    ]
    LEVEL_CHOICES = [
        ('beginner', 'Beginner'),
        ('intermediate', 'Intermediate'),
        ('advanced', 'Advanced'),
        ('expert', 'Expert'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='skills')
    name = models.CharField(max_length=100)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default='other')
    proficiency = models.IntegerField(
        default=50,
        validators=[MinValueValidator(0), MaxValueValidator(100)],
        help_text='0-100'
    )
    level = models.CharField(max_length=20, choices=LEVEL_CHOICES, default='intermediate')
    icon_class = models.CharField(max_length=80, blank=True)

    class Meta:
        ordering = ['-proficiency']

    def __str__(self):
        return f"{self.name} ({self.get_level_display()})"


class Project(models.Model):
    STATUS_CHOICES = [
        ('completed', 'Completed'),
        ('in_progress', 'In Progress'),
        ('planned', 'Planned'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='projects')
    title = models.CharField(max_length=200)
    description = models.TextField()
    tech_used = models.CharField(max_length=500, help_text='Comma-separated technologies')
    github_link = models.URLField(blank=True)
    live_link = models.URLField(blank=True)
    thumbnail = models.ImageField(upload_to='projects/', blank=True, null=True)
    date = models.DateField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='completed')
    featured = models.BooleanField(default=False)

    class Meta:
        ordering = ['-date']

    def __str__(self):
        return self.title

    def tech_list(self):
        return [t.strip() for t in self.tech_used.split(',') if t.strip()]


class Experience(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='experiences')
    company = models.CharField(max_length=200)
    role = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    start_date = models.DateField()
    end_date = models.DateField(blank=True, null=True)
    is_current = models.BooleanField(default=False)

    class Meta:
        ordering = ['-start_date']

    def __str__(self):
        return f"{self.role} @ {self.company}"

    def duration(self):
        end = date.today() if (self.is_current or not self.end_date) else self.end_date
        total_months = (end.year - self.start_date.year) * 12 + (end.month - self.start_date.month)
        years, months = divmod(total_months, 12)
        parts = []
        if years:
            parts.append(f"{years} yr{'s' if years > 1 else ''}")
        if months:
            parts.append(f"{months} mo{'s' if months > 1 else ''}")
        return ' '.join(parts) or '< 1 month'


class Certification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='certifications')
    title = models.CharField(max_length=200)
    issuer = models.CharField(max_length=200)
    date = models.DateField()
    expiry_date = models.DateField(blank=True, null=True)
    credential_url = models.URLField(blank=True)
    badge_image = models.ImageField(upload_to='badges/', blank=True, null=True)
    credential_id = models.CharField(max_length=200, blank=True)

    class Meta:
        ordering = ['-date']

    def __str__(self):
        return f"{self.title} — {self.issuer}"
