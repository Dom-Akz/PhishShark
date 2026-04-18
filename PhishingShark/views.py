from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout
from .models import Administrateur, Employes, Departement, Entreprise, EmailTracking
from django.db.models import Count
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django import forms
import json
import datetime
import os

# ROOT_FOLDER="/home/soufiane/cs/PFA/PhishingShark/PhishShark/PhishShark/"
TEMPLATES = "EmailTemplates/Templates.json"


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
        "lien": "lien",  # todo
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


# main functions:


# generate email from templates using ink
def generate_email(employe):
    if not os.path.exists(TEMPLATES):
        raise FileNotFoundError(f"The file '{TEMPLATES}' does not exist")

    ink = Employes.objects.filter(user=employe).only("ink")
    emp_info = extract_ink(ink)
    email = {}  # json response

    # Email Type Choice:
    # get totale email clicks and there type
    received_counts = (
        EmailTracking.objects.filter(user=employe, status="CLICK")
        .values("type")
        .annotate(received_count=Count("id"))
        .order_by("-received_count")
    )

    # Get the type with highest count
    max_type = received_counts.first()

    # open ttemplates file
    with open(TEMPLATES, "r") as templates:
        tmp = json.load(templates)

    # use the same type again
    if max_type["received_count"] >= 2:
        for item in tmp:
            if max_type["type"] == item["id"]:
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
                email = replace_var(emp_info, item)
                break
    return email


# send email
def send_email():
    pass


# track the email
def track_email():
    pass


# here is the function that handle all steps
@login_required(login_url="login")
@require_POST
def phishing_email(request):
    # email = generate_email(ink)
    # uuid = send_email(email)
    # track_email()  # thread
    pass


# Authentification :
@require_POST
def login_u(request):
    pass


def logout_u(request):
    logout(request)
    request.session.flush()
    return redirect("login")


# DASHBOARD :

# sub-dashboard function


# main dashboard
@login_required(login_url="login")
def dashboard(request):
    pass
