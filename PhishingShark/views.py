from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import  login, logout
from .models import Administrateur, Employes, Departement, Entreprise
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django import forms 
import json

#ROOT_FOLDER="/home/soufiane/cs/PFA/PhishingShark/PhishShark/PhishShark/"
TEMPLATES="EmailTemplates/Templates.json"


# helper functions:

# extract emp info from ink and return json format (dep_chefdep_locatisation_Entreprise)
def extract_ink(ink):
    if "_" not in ink:
        return 0

    ext = ink.split("_")  # [dep, chefdep, ...]

    res_json = {
        "departement": ext[0],
        "chef departement": ext[1],
        "localisation": ext[2],
        "entreprise": ext[3],
    }
    return res_json


# main functions:

# generate email from templates using ink
def gen_email():
    

# send email
def send_email():
    pass

# track the email
def track_email():
    pass


@login_required
@require_POST
def phishing_email(request):
    admin = request.user

    
    
