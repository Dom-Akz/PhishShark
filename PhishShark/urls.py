"""
URL configuration for PhishShark project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path, include
from PhishingShark import views

app_name = "dashboard"

urlpatterns = [
    path("", views.logout_u, name="login"),
    path("admin/login/", views.login_u, name="login"),
    path("admin/logout/", views.logout_u, name="logout"),
    path("admin/profile/", views.profile_view, name="profile"),
    path("admin/dashboard/", views.dashboard, name="dashboard"),
    path("admin/employees/", views.employees_page, name="employees"),
    path("phishing/send/<int:employe>/", views.phishing_email, name="phishing_email"),
    path("track/<str:uuid>/<slug:pg_slug>/", views.track_email, name="track_email"),
    path("fake-page/<slug:page_slug>/", views.serve_fake_page, name="fake_page"),
    path("capture-credentials/", views.capture_credentials, name="capture_credentials"),
    path("admin/companies/", views.companies_page, name="companies"),
    path("admin/departements/", views.departments_page, name="departments"),
    path("admin/training/", views.training_awareness, name="training_awareness"),
    path("sensibilisation/", include("Sensibilisation.urls")),
    # path("admin/", admin.site.urls),
]
