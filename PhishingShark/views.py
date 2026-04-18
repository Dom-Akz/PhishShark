from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout
from .models import Administrateur, Employes, Departement, Entreprise, EmailTracking
from django.db.models import Count
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django import forms
import json

# ROOT_FOLDER="/home/soufiane/cs/PFA/PhishingShark/PhishShark/PhishShark/"
TEMPLATES = "EmailTemplates/Templates.json"


# helper functions:


# extract emp info from ink and return json format (nom_dep_chefdep_locatisation_Entreprise)
def extract_ink(ink):
    ext = ink.split("_")  # [dep, chefdep, ...]

    res_json = {
        "nom": ext[0],
        "departement": ext[1],
        "chef departement": ext[2],
        "localisation": ext[3],
        "entreprise": ext[4],
    }
    return res_json


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
                # get the variable field
                variables = tmp.get("variables", [])
                # remove the variable field
                email = tmp
                del email["variables"]
                email["header"] = email["header"].replace("{emp_name}", emp_info["nom"])

    # use different email type than the last click one
    else:
        last_email_click = (
            EmailTracking.objects.filter(user=employe, status="CLICK")
            .order_by("-received_date")
            .first()
        )


# send email
def send_email():
    pass


# track the email
def track_email():
    pass


# here is the function that handle all steps
@login_required
@require_POST
def phishing_email(request):
    admin = request.user
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
@login_required
def dashboard(request):
    pass
