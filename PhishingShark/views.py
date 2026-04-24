from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from .models import Administrateur, Employes, Departement, Entreprise, EmailTracking
from Sensibilisation.models import QcmResult, Sensibilisation
from django.db.models import Count
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django import forms
from django.core.mail import send_mail
from django.utils import timezone
from django.conf import settings
from django.db.models import Count, Q
from django.db.models.functions import TruncDate
from datetime import datetime, timedelta
import os
import json
import hashlib
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
        "today_date": timezone.now(),
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
        return redirect("/admin/dashboard")
    return render(request, "admin/Login.html")


def login_u(request):
    if request.user.is_authenticated:
        return redirect("/admin/dashboard/")

    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)  # Django handles the session securely
            return redirect("/admin/dashboard/")
        else:
            return render(request, "admin/Login.html", {"error": "Invalid credentials"})

    return render(request, "admin/Login.html")


def logout_u(request):
    logout(request)
    request.session.flush()
    return redirect("/admin/login/")


# DASHBOARD :


def get_phishing_data(days, department_id=None, admin=None):
    end_date = timezone.now()
    start_date = end_date - timedelta(days=days)

    # Base queryset
    email_qs = EmailTracking.objects.filter(
        send_date__gte=start_date, send_date__lte=end_date
    )

    # Filter by department (if not superuser)
    if department_id and department_id != "all" and department_id != "None":
        email_qs = email_qs.filter(employe__departement__id=department_id)
    elif admin and not admin.is_supperuser and admin.departement:
        # Non-superuser sees only their department
        email_qs = email_qs.filter(employe__departement=admin.departement)

    # KPI values
    total_sent = email_qs.exclude(status="PENDING").count()
    total_clicks = email_qs.filter(status="CLICK").count()
    click_rate = round((total_clicks / total_sent * 100), 1) if total_sent > 0 else 0

    # Email status distribution
    pending = email_qs.filter(status="PENDING").count()
    sent = email_qs.filter(status="SENT").count()
    received = email_qs.filter(status="RECEIVED").count()
    clicked = email_qs.filter(status="CLICK").count()
    failed = email_qs.filter(status="FAILED").count()

    # Email type breakdown
    type_company = email_qs.filter(type="COMPANY_EMAIL").count()
    type_payment = email_qs.filter(type="PAYMENT_REQUEST").count()
    type_job = email_qs.filter(type="JOB_OFFER").count()
    type_it = email_qs.filter(type="ID_DEP").count()
    type_iphone = email_qs.filter(type="SCAM_IPHONE").count()
    type_lottery = email_qs.filter(type="SCAM_LOTTERY").count()
    type_security = email_qs.filter(type="SECURITY_ALERT").count()

    # Type clicks
    type_company_click = email_qs.filter(type="COMPANY_EMAIL", status="CLICK").count()
    type_payment_click = email_qs.filter(type="PAYMENT_REQUEST", status="CLICK").count()
    type_job_click = email_qs.filter(type="JOB_OFFER", status="CLICK").count()
    type_it_click = email_qs.filter(type="ID_DEP", status="CLICK").count()
    type_iphone_click = email_qs.filter(type="SCAM_IPHONE", status="CLICK").count()
    type_lottery_click = email_qs.filter(type="SCAM_LOTTERY", status="CLICK").count()
    type_security_click = email_qs.filter(type="SECURITY_ALERT", status="CLICK").count()

    # Timeline data
    timeline = (
        email_qs.annotate(date=TruncDate("send_date"))
        .values("date")
        .annotate(sent=Count("id"), clicked=Count("id", filter=Q(status="CLICK")))
        .order_by("date")
    )

    timeline_labels = json.dumps(
        [item["date"].strftime("%d/%m") for item in timeline if item["date"]]
    )
    timeline_sent = json.dumps([item["sent"] for item in timeline])
    timeline_clicked = json.dumps([item["clicked"] for item in timeline])

    # Department click rates (only show accessible departments)
    dept_names = []
    dept_rates = []

    if admin and not admin.is_supperuser and admin.departement:
        # Single department for non-superuser
        dept = admin.departement
        dept_emails = email_qs.filter(employe__departement=dept)
        dept_sent = dept_emails.count()
        dept_clicks = dept_emails.filter(status="CLICK").count()
        rate = round((dept_clicks / dept_sent * 100), 1) if dept_sent > 0 else 0
        dept_names.append(dept.name)
        dept_rates.append(rate)
    else:
        # All departments for superuser
        for dept in Departement.objects.all():
            dept_emails = email_qs.filter(employe__departement=dept)
            dept_sent = dept_emails.count()
            dept_clicks = dept_emails.filter(status="CLICK").count()
            rate = round((dept_clicks / dept_sent * 100), 1) if dept_sent > 0 else 0
            dept_names.append(dept.name)
            dept_rates.append(rate)

    # Recent activity (only visible employees)
    recent = []
    for track in email_qs.select_related("employe").order_by("-send_date")[:10]:
        recent.append(
            {
                "employee": track.employe,
                "type": track.get_status_display(),
                "status": track.get_status_display(),
                "send_date": track.send_date,
            }
        )

    # Total employees count (only accessible employees)
    if admin and not admin.is_supperuser and admin.departement:
        total_employees = Employes.objects.filter(departement=admin.departement).count()
    else:
        total_employees = Employes.objects.count()

    return {
        "total_emails_sent": total_sent,
        "total_clicks": total_clicks,
        "click_rate": click_rate,
        "total_employees": total_employees,
        "email_pending": pending,
        "email_sent": sent,
        "email_received": received,
        "email_clicked": clicked,
        "email_failed": failed,
        "type_company": type_company,
        "type_payment": type_payment,
        "type_job": type_job,
        "type_it": type_it,
        "type_iphone": type_iphone,
        "type_lottery": type_lottery,
        "type_security": type_security,
        "type_company_click": type_company_click,
        "type_payment_click": type_payment_click,
        "type_job_click": type_job_click,
        "type_it_click": type_it_click,
        "type_iphone_click": type_iphone_click,
        "type_lottery_click": type_lottery_click,
        "type_security_click": type_security_click,
        "timeline_labels": timeline_labels,
        "timeline_sent": timeline_sent,
        "timeline_clicked": timeline_clicked,
        "department_names": json.dumps(dept_names),
        "dept_click_rate": json.dumps(dept_rates),
        "recent_activity": recent,
    }


@login_required(login_url="/admin/login")
def dashboard(request):

    admin = request.user

    days = int(request.GET.get("days", 30))
    if admin.is_supperuser:
        dep_id = None
        departements = Departement.objects.all()
    else:
        dep_id = admin.departement_id
        departements = Departement.objects.filter(id=dep_id)

    context = {
        "user": request.user,
        "departments": departements,
        "selected_days": days,
        "selected_department": dep_id,
        "is_superuser": admin.is_supperuser,
        "admin_department": admin.departement.name if admin.departement else None,
    }

    context.update(get_phishing_data(days, dep_id, admin))

    return render(request, "admin/dashboard.html", context=context)
