from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from .models import Administrateur, Employes, Departement, Entreprise, EmailTracking
from django.db.models import Count
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django import forms
from django.core.mail import send_mail
from django.utils import timezone
from django.conf import settings
import os
import json
import hashlib
import datetime
import requests

# ROOT_FOLDER="/home/soufiane/cs/PFA/PhishingShark/PhishShark/PhishShark/"
TEMPLATES_FILE = "EmailTemplates/Templates.json"


# helper functions:


# extract emp info from ink and return json format (nom_dep_chefdep_locatisation_Entreprise)
def extract_ink(ink):
    ext = ink.split("_")  # [dep, chefdep, ...]

    res_json = {
        "emp_name": ext[0],
        "departement": ext[1],
        "nom_chef_dep": ext[2],
        "localisation": ext[3],
        "company_name": ext[4],
        "lien": "lien",
        "today_date": datetime.date.today(),
    }
    return res_json


# replace variable with value using emp_info
# return the email as json
def replace_var(emp_info, template):
    email = template
    del email["variables"]
    for var_mapping in template["variables"]:
        for field_name, placeholder in var_mapping.items():
            if isinstance(placeholder, list):
                # Multiple placeholders for one field
                for p in placeholder:
                    if p in emp_info:
                        email[field_name] = email[field_name].replace(
                            f"{{{p}}}", emp_info[p]
                        )
            else:
                # Single placeholder
                if placeholder in emp_info:
                    email[field_name] = email[field_name].replace(
                        f"{{{placeholder}}}", emp_info[placeholder]
                    )

    return email


def generate_uuid(matricule):
    uuid = hashlib.sha256(matricule.encode()).hexdigest()
    return str(uuid[:32])


def get_client_ip(request):
    x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
    if x_forwarded_for:
        ip = x_forwarded_for.split(",")[0]
    else:
        ip = request.META.get("REMOTE_ADDR")
    return ip


# main functions:


# generate email from templates using ink
def generate_email(employe):
    if not os.path.exists(TEMPLATES_FILE):
        raise FileNotFoundError(f"The file '{TEMPLATES_FILE}' does not exist")

    emp_info = extract_ink(employe.ink)
    email = {}
    email_type = ""

    # Email Type Choice:
    # get totale email clicks and there type
    received_counts = (
        EmailTracking.objects.filter(employe=employe, status="CLICK")
        .values("type")
        .annotate(received_count=Count("id"))
        .order_by("-received_count")
    )

    # Get the type with highest count
    max_type = received_counts.first()

    # open templates file
    with open(TEMPLATES_FILE, "r") as templates:
        tmp = json.load(templates)

    # use the same type again
    if max_type["received_count"] >= 2:
        for item in tmp:
            if max_type["type"] == item["id"]:
                email_type = item["id"]
                email = replace_var(emp_info, item)
                break
    # use different email type than the last click one
    else:
        last_email_click = (
            EmailTracking.objects.filter(user=employe, status="CLICK")
            .order_by("-received_date")
            .first()
        )
        for item in tmp:
            if last_email_click.type != item["id"]:
                email_type = item["id"]
                email = replace_var(emp_info, item)
                break
    return email, email_type


# send email
def send_email(email, emp, email_type):
    body = email["header"] + email["content"] + email["footer"]

    send_mail(
        subject=email["subject"],
        message=body,
        from_email=email["sender"],
        recipient_list=[emp.email],  # can take a list of emails
        fail_silently=False,
    )

    uuid = generate_uuid(emp.matricule)
    EmailTracking.objects.create(
        employe=emp,
        uuid=uuid,
        status="SENT",
        type=email_type,
        sent_date=timezone.now(),
    )


# track the email
# called when the user click in the email by the router
def track_email(request, uuid):
    email_tracking = EmailTracking.objects.get(uuid=uuid)

    email_tracking.status = "CLICKED"
    email_tracking.clicked_at = timezone.now()
    email_tracking.ip_address = get_client_ip(request)

    email_tracking.save()


# here is the function that handle all steps
@require_POST
def phishing_email(request, employe):
    # get all employe info
    emp = Employes.objects.get(id=employe)

    email, email_type = generate_email(emp)

    send_email(email, emp, email_type)


# Authentification :
def login_view(request):
    if request.user.is_authenticated:
        return redirect("dashboard")
    return render(request, "admin/Login.html")


def login_u(request):
    if request.session.get("admin_id"):
        return redirect("dashboard")

    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        # Hash the password (assuming you stored hashed passwords)
        hashed_password = hashlib.sha256(password.encode()).hexdigest()

        try:
            admin = Administrateur.objects.get(
                username=username, password=hashed_password
            )

            request.session["admin_id"] = admin.id
            request.session["admin_name"] = admin.name

            return redirect("dashboard")
        except Administrateur.DoesNotExist:
            return render(request, "admin/Login.html", {"error": "Invalid credentials"})

    return render(request, "admin/Login.html")


def logout_u(request):
    logout(request)
    request.session.flush()
    return redirect("login")


# DASHBOARD :

# sub-dashboard function


# main dashboard


@login_required
def dashboard(request):
    if not request.user.is_authenticated:
        return redirect("admin/Login.html")
