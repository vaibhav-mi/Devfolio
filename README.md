# DevFolio — Personal Resume Dashboard

A full-stack Django portfolio dashboard.

## Quick Start

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Run migrations
python manage.py makemigrations portfolio
python manage.py migrate

# 3. Create superuser
python manage.py createsuperuser

# 4. Run development server
python manage.py runserver
```

Then visit: http://127.0.0.1:8000/login/

## URL Map

| URL | Description |
|-----|-------------|
| `/login/` | Login page |
| `/dashboard/` | Main dashboard with charts |
| `/profile/` | Profile editor + password change |
| `/skills/` | Skills CRUD |
| `/projects/` | Projects CRUD with filter |
| `/experience/` | Work history timeline |
| `/certifications/` | Certifications vault |
| `/admin/` | Django admin panel |

## Tech Stack

- **Backend**: Django 4.2, SQLite (swap to PostgreSQL for production)
- **Auth**: Django built-in auth with session management
- **Forms**: Crispy Forms + Bootstrap 5
- **Charts**: Chart.js 4 (CDN)
- **Fonts**: Space Mono + Syne (Google Fonts)
- **File uploads**: Pillow (images), FileField (resume)

## Project Structure


devfolio/
├── core/                   # Django project config
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── portfolio/              # Main app
│   ├── models.py           # Profile, Skill, Project, Experience, Certification
│   ├── views.py            # All CRUD views
│   ├── forms.py            # ModelForms
│   ├── urls.py             # URL routing
│   ├── admin.py            # Admin registration
│   ├── signals.py          # Auto-create Profile on User creation
│   ├── apps.py
│   ├── migrations/
│   ├── static/portfolio/
│   │   ├── css/devfolio.css
│   │   └── js/devfolio.js
│   └── templatetags/
├── templates/portfolio/    # All HTML templates
│   ├── base.html
│   ├── login.html
│   ├── dashboard.html
│   ├── profile.html
│   ├── skill_list.html
│   ├── skill_form.html
│   ├── project_list.html
│   ├── project_form.html
│   ├── experience_list.html
│   ├── experience_form.html
│   ├── certification_list.html
│   ├── certification_form.html
│   └── confirm_delete.html
├── media/                  # User uploads
├── manage.py
└── requirements.txt

