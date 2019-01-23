# This is a demo app backend configuration
### System requirement: Django 1.11.11 on Ubuntu 18.04

# How do I run this demo?
1. Clone this repo to server */home/django_project/*
2. On bash, run *service gunicorn restart* <br />
This will restart the application completely
3. Run *python manage.py runserver localhost:9000*

# What this demo can do?
1. addchatt
2. getchatt

# File structure
.
├── chat<br />
│   ├── __init__.py<br />
│   ├── __init__.pyc<br />
│   ├── admin.py<br />
│   ├── apps.py<br />
│   ├── migrations<br />
│   │   └── __init__.py<br />
│   ├── models.py<br />
│   ├── tests.py<br />
│   └── views.pyc<br />
├── chatter<br />
│   ├── __init__.py<br />
│   ├── __init__.pyc<br />
│   ├── admin.py<br />
│   ├── apps.py<br />
│   ├── migrations<br />
│   │   └── __init__.py<br />
│   ├── models.py<br />
│   ├── tests.py<br />
│   ├── views.py<br />
│   └── views.pyc<br />
├── demo<br />
│   ├── README.md<br />
│   └── manage.py<br />
├── django_project<br />
│   ├── __init__.py<br />
│   ├── __init__.pyc<br />
│   ├── settings.py<br />
│   ├── settings.py.orig<br />
│   ├── settings.pyc<br />
│   ├── urls.py<br />
│   ├── urls.pyc<br />
│   ├── wsgi.py<br />
│   └── wsgi.pyc<br />
└── manage.py<br />
