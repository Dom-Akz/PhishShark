from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from .models import (
    Administrateur,
    Employes,
    Departement,
    Entreprise,
    EmailTracking,
    CapturedCredential,
)
from Sensibilisation.models import QcmResult
from django.db.models import Count, Avg
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.core.mail import send_mail
from django.utils import timezone
from django.contrib import messages
from django.core.mail import EmailMessage
from django.http import JsonResponse
from django.db.models import Q
from django.db.models.functions import TruncDate
from datetime import timedelta
from django.http import HttpResponse
from django.utils.html import escape
from django.views.decorators.csrf import csrf_exempt
from django.db.models.functions import TruncMonth
from django.conf import settings
from .forms import AdminProfileForm
import os
import json
import uuid

TEMPLATES_FILE = os.path.join(
    os.path.dirname(__file__), "EmailTemplates", "Templates.json"
)
MIRROR_MAP_FILE = os.path.join(os.path.dirname(__file__), "Mirrors", "map.json")


# helper functions:


# extract emp info from ink and return json format (nom_dep_chefdep_locatisation_Entreprise)
def extract_ink(ink):
    ext = ink.split("_")

    # Format: first_name_departement_chefdep_location_company
    res_json = {
        "Employe_Name": ext[0],  # For company_email template
        "emp_name": ext[0],  # For all other templates
        "departement": ext[1],
        "nom_chef_dep": ext[2],
        "localisation": ext[3],
        "companyName": ext[4],  # For company_email sender
        "company_name": ext[4],  # For company_email variables
        "lien": "lien",
        "today_date": timezone.now().strftime("%d/%m/%Y"),
        "diff_location": "Unknown location",  # For security_alert
        "sender_email": "security@company.com",  # For scam_iphone
    }
    return res_json


# replace variable with value using emp_info
# return the email as json
def replace_var(emp_info, template):
    email = template.copy()

    # Remove variables key
    email.pop("variables", None)

    # Replace ALL placeholders in ALL string fields
    for key, value in email.items():
        if isinstance(value, str):
            for placeholder, replacement in emp_info.items():
                if replacement:
                    email[key] = email[key].replace(
                        f"{{{placeholder}}}", str(replacement)
                    )

    return email


def generate_uuid(matricule):
    unique_string = f"{matricule}_{timezone.now().timestamp()}"
    return str(uuid.uuid5(uuid.NAMESPACE_DNS, unique_string))


def get_client_ip(request):
    x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
    if x_forwarded_for:
        ip = x_forwarded_for.split(",")[0]
    else:
        ip = request.META.get("REMOTE_ADDR")
    return ip


def get_mirror_page(email_type):
    with open(MIRROR_MAP_FILE, "r") as map_file:
        map_file = json.load(map_file)

    return map_file.get(email_type)


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
        data = json.load(templates)
        tmp = data.get("templates", data)

    first_template_id = tmp[0]["id"] if tmp else None

    # use the same type again
    if max_type and max_type.get("recived_count", 0) >= 2:
        for item in tmp:
            if max_type["type"] == item["id"]:
                email_type = item["id"]
                email = replace_var(emp_info, item)
                break
    # use different email type than the last click one
    else:
        last_email_click = (
            EmailTracking.objects.filter(employe=employe, status="CLICK")
            .order_by("-received_date")
            .first()
        )
        found = False
        for item in tmp:
            if not last_email_click or last_email_click.type != item["id"]:
                email_type = item["id"]
                email = replace_var(emp_info, item)
                found = True
                break

        if not found and tmp:
            email_type = tmp[0]["id"]
            email = replace_var(emp_info, tmp[0])

    # Final fallback to first template
    if not email and first_template_id:
        email_type = first_template_id
        for item in tmp:
            if item["id"] == first_template_id:
                email = replace_var(emp_info, item)
                break

    return email, email_type


# send email
def send_email(email, emp, email_type):

    uuid = generate_uuid(emp.matricule)
    mirro_file_name = get_mirror_page(email_type)
    pg_slug = mirro_file_name.replace(".html", "")

    link = f"http://localhost:8000/track/{uuid}/{pg_slug}/"

    body = email["header"] + email["content"] + email["footer"]
    body = body.replace("lien", link)

    send_msg = EmailMessage(
        subject=email["subject"],
        body=body,
        from_email=settings.EMAIL_HOST_USER,
        to=[emp.email],
        reply_to=[email["sender"]],
        headers={"Replay-To": email["sender"]},
    )
    send_msg.send(fail_silently=False)

    EmailTracking.objects.update_or_create(
        employe=emp,
        defaults={  # create ot update
            "uuid": uuid,
            "status": "SENT",
            "type": email_type,
            "send_date": timezone.now(),
        },
    )


# track the email
# called when the user click in the email by the router
def track_email(request, uuid, pg_slug):
    email_tracking = EmailTracking.objects.get(uuid=uuid)
    email_tracking.status = "CLICK"
    email_tracking.clicked_at = timezone.now()
    email_tracking.ip_address = get_client_ip(request)
    email_tracking.save()

    return redirect(f"/fake-page/{pg_slug}/?rid={uuid}")


def serve_fake_page(request, page_slug):
    # Validate UUID format before using it
    tracking_uuid = request.GET.get("rid", "")

    page_slug = os.path.basename(page_slug)

    mirror_path = os.path.join(
        os.path.dirname(__file__), "Mirrors", "Pages", f"{page_slug}.html"
    )

    base_dir = os.path.join(os.path.dirname(__file__), "Mirrors", "Pages")
    if not os.path.realpath(mirror_path).startswith(os.path.realpath(base_dir)):
        return HttpResponse("Forbidden", status=403)

    if not os.path.exists(mirror_path):
        return HttpResponse(f"Page '{escape(page_slug)}' not found.", status=404)

    with open(mirror_path, "r", encoding="utf-8") as f:
        html_content = f.read()

    html_content = html_content.replace(
        'action="https://accounts.google.com/v3/signin/identifier',
        'action="/capture-credentials/"',
    )
    html_content = html_content.replace(
        'action="https://accounts.google.com/v3/signin/',
        'action="/capture-credentials/"',
    )

    safe_uuid = escape(tracking_uuid)
    html_content = html_content.replace(
        "</form>",
        f'<input type="hidden" name="tracking_uuid" value="{safe_uuid}"></form>',
    )

    return HttpResponse(html_content)


@csrf_exempt
def capture_credentials(request):
    if request.method == "POST":
        username = (
            request.POST.get("username")
            or request.POST.get("email")
            or request.POST.get("identifier")
            or ""
        )
        password = request.POST.get("password") or request.POST.get("Passwd") or ""
        tracking_uuid = request.POST.get("tracking_uuid", "")
        ip_address = get_client_ip(request)
        user_agent = request.META.get("HTTP_USER_AGENT", "")[:500]

        try:
            email_tracking = EmailTracking.objects.get(uuid=tracking_uuid)
            email_tracking.status = "CREDENTIALS_CAPTURED"
            email_tracking.save()

            CapturedCredential.objects.create(
                username=username,
                password=password,
                email_tracking=email_tracking,
                user_agent=user_agent,
            )

        except EmailTracking.DoesNotExist:
            CapturedCredential.objects.create(
                username=username,
                password=password,
                ip_address=ip_address,
                user_agent=user_agent,
            )
        return redirect(f"/sensibilisation/training/?rid={tracking_uuid}")

    return JsonResponse({"error": "Method not allowed"}, status=405)


@login_required(login_url="/admin/login/")
def employees_page(request):
    # Get all employees (no department filtering)
    employees = (
        Employes.objects.select_related("departement", "entreprise")
        .all()
        .order_by("-created_at")
    )

    # Get filter options
    departments = Departement.objects.all()
    enterprises = Entreprise.objects.all()

    # Get statistics
    total_employees = employees.count()

    # Count employees who clicked on phishing
    clicked_count = (
        EmailTracking.objects.filter(employe__in=employees, status="CLICK")
        .values("employe")
        .distinct()
        .count()
    )

    # Count employees who completed training
    trained_count = QcmResult.objects.values("employee_matricule").distinct().count()
    pending_count = max(0, total_employees - trained_count)

    return render(
        request,
        "admin/employees.html",
        {
            "employees": employees,
            "departments": departments,
            "enterprises": enterprises,
            "trained_count": trained_count,
            "pending_count": pending_count,
            "clicked_count": clicked_count,
        },
    )


# here is the function that handle all steps
@require_POST
def phishing_email(request, employe):
    # get all employe info
    emp = Employes.objects.get(id=employe)
    # generate the email
    email, email_type = generate_email(emp)
    # send the email
    send_email(email, emp, email_type)

    messages.success(request, f"Email sent successfully to {emp.email}")

    return redirect("/admin/employees/")


# Authentification :
def login_view(request):
    if request.user.is_authenticated:
        return redirect("/admin/dashboard")
    render(request, "admin/Login.html")


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
    messages.success(request, "You have been logged out successfully.")
    return redirect("/admin/login/")


# DASHBOARD :
def get_phishing_data(days):
    end_date = timezone.now()
    start_date = end_date - timedelta(days=days)

    email_qs = EmailTracking.objects.filter(
        send_date__gte=start_date, send_date__lte=end_date
    )

    total_sent = email_qs.exclude(status="PENDING").count()
    total_clicks = email_qs.filter(status="CLICK").count()
    click_rate = round((total_clicks / total_sent * 100), 1) if total_sent > 0 else 0

    pending = email_qs.filter(status="PENDING").count()
    sent = email_qs.filter(status="SENT").count()
    received = email_qs.filter(status="RECEIVED").count()
    clicked = email_qs.filter(status="CLICK").count()
    failed = email_qs.filter(status="FAILED").count()

    type_company = email_qs.filter(type="COMPANY_EMAIL").count()
    type_payment = email_qs.filter(type="PAYMENT_REQUEST").count()
    type_job = email_qs.filter(type="JOB_OFFER").count()
    type_it = email_qs.filter(type="ID_DEP").count()
    type_iphone = email_qs.filter(type="SCAM_IPHONE").count()
    type_lottery = email_qs.filter(type="SCAM_LOTTERY").count()
    type_security = email_qs.filter(type="SECURITY_ALERT").count()

    type_company_click = email_qs.filter(type="COMPANY_EMAIL", status="CLICK").count()
    type_payment_click = email_qs.filter(type="PAYMENT_REQUEST", status="CLICK").count()
    type_job_click = email_qs.filter(type="JOB_OFFER", status="CLICK").count()
    type_it_click = email_qs.filter(type="ID_DEP", status="CLICK").count()
    type_iphone_click = email_qs.filter(type="SCAM_IPHONE", status="CLICK").count()
    type_lottery_click = email_qs.filter(type="SCAM_LOTTERY", status="CLICK").count()
    type_security_click = email_qs.filter(type="SECURITY_ALERT", status="CLICK").count()

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

    dept_names = []
    dept_rates = []

    for dept in Departement.objects.all():
        dept_emails = email_qs.filter(employe__departement=dept)
        dept_sent = dept_emails.count()
        dept_clicks = dept_emails.filter(status="CLICK").count()
        rate = round((dept_clicks / dept_sent * 100), 1) if dept_sent > 0 else 0
        dept_names.append(dept.name)
        dept_rates.append(rate)

    recent = []
    for track in email_qs.select_related("employe").order_by("-send_date")[:10]:
        recent.append(
            {
                "employee": track.employe,
                "type": track.get_type_display(),
                "status": track.get_status_display(),
                "send_date": track.send_date,
            }
        )

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


@login_required(login_url="/admin/login/")
def companies_page(request):
    try:
        admin = Administrateur.objects.get(username=request.user.username)
    except Administrateur.DoesNotExist:
        return redirect("/admin/login/")

    companies = Entreprise.objects.all().order_by("name")

    # Get statistics for each company
    company_stats = []
    for company in companies:
        employees_count = Employes.objects.filter(entreprise=company).count()
        emails_sent = EmailTracking.objects.filter(employe__entreprise=company).count()
        clicks = EmailTracking.objects.filter(
            employe__entreprise=company, status="CLICK"
        ).count()

        company_stats.append(
            {
                "company": company,
                "employees_count": employees_count,
                "emails_sent": emails_sent,
                "clicks": clicks,
                "click_rate": round((clicks / emails_sent * 100), 1)
                if emails_sent > 0
                else 0,
            }
        )

    return render(
        request,
        "admin/companies.html",
        {
            "companies": companies,
            "company_stats": company_stats,
            "total_companies": companies.count(),
            "active_page": "companies",
        },
    )


@login_required(login_url="/admin/login/")
def departments_page(request):

    # Get all departments with related data
    departments = Departement.objects.all().order_by("name")

    department_stats = []
    totale_active_dep = 0
    for dept in departments:
        if dept.is_active:
            totale_active_dep += 1
        employees_count = Employes.objects.filter(departement=dept).count()
        emails_sent = EmailTracking.objects.filter(employe__departement=dept).count()
        clicks = EmailTracking.objects.filter(
            employe__departement=dept, status="CLICK"
        ).count()
        avg_click_rate = (
            round((clicks / emails_sent * 100), 1) if emails_sent > 0 else 0
        )

        department_stats.append(
            {
                "department": dept,
                "employees_count": employees_count,
                "emails_sent": emails_sent,
                "clicks": clicks,
                "click_rate": avg_click_rate,
            }
        )

    return render(
        request,
        "admin/departements.html",
        {
            "departments": departments,
            "department_stats": department_stats,
            "total_departments": departments.count(),
            "active_dep": totale_active_dep,
        },
    )


@login_required(login_url="/admin/login/")
def training_awareness(request):
    days = int(request.GET.get("days", 30))
    department_id = request.GET.get("department", None)

    departments = Departement.objects.all()

    # Base queryset for email tracking (to get training completion)
    email_qs = EmailTracking.objects.filter(status="TRAINING_COMPLETED")

    if department_id and department_id != "all" and department_id != "None":
        email_qs = email_qs.filter(employe__departement__id=department_id)

    qcm_results = QcmResult.objects.all()
    if department_id and department_id != "all" and department_id != "None":
        department_employees = Employes.objects.filter(
            departement__id=department_id
        ).values_list("matricule", flat=True)
        qcm_results = qcm_results.filter(employee_matricule__in=department_employees)

    # Statistics
    total_completed_training = email_qs.count()
    total_employees = Employes.objects.count()

    completion_rate = (
        round((total_completed_training / total_employees * 100), 1)
        if total_employees > 0
        else 0
    )

    # Average quiz score
    avg_score = qcm_results.aggregate(avg=Avg("score"))["avg"] or 0

    # Score distribution
    score_0_20 = qcm_results.filter(score__lte=20).count()
    score_21_40 = qcm_results.filter(score__gt=20, score__lte=40).count()
    score_41_60 = qcm_results.filter(score__gt=40, score__lte=60).count()
    score_61_80 = qcm_results.filter(score__gt=60, score__lte=80).count()
    score_81_100 = qcm_results.filter(score__gt=80).count()

    # Quiz attempts distribution
    attempts_1 = qcm_results.filter(totale_qcm_taken=1).count()
    attempts_2 = qcm_results.filter(totale_qcm_taken=2).count()
    attempts_3 = qcm_results.filter(totale_qcm_taken=3).count()
    attempts_4plus = qcm_results.filter(totale_qcm_taken__gte=4).count()

    # Monthly completion trend

    monthly_trend = (
        EmailTracking.objects.filter(status="TRAINING_COMPLETED")
        .annotate(month=TruncMonth("clicked_at"))
        .values("month")
        .annotate(count=Count("id"))
        .order_by("month")
    )

    trend_labels = json.dumps(
        [item["month"].strftime("%b %Y") for item in monthly_trend if item["month"]]
    )
    trend_data = json.dumps([item["count"] for item in monthly_trend])

    # Top performers
    top_performers = []
    for result in qcm_results.select_related().order_by("-score")[:10]:
        try:
            employee = Employes.objects.get(matricule=result.employee_matricule)
            top_performers.append(
                {
                    "name": f"{employee.first_name} {employee.last_name}",
                    "matricule": result.employee_matricule,
                    "score": result.score,
                    "attempts": result.totale_qcm_taken,
                    "department": employee.departement.name
                    if employee.departement
                    else "-",
                    "email": employee.email,
                }
            )
        except Employes.DoesNotExist:
            top_performers.append(
                {
                    "name": result.employee_matricule,
                    "matricule": result.employee_matricule,
                    "score": result.score,
                    "attempts": result.totale_qcm_taken,
                    "department": "-",
                    "email": "-",
                }
            )

    # Recent completions
    recent_completions = []
    for track in email_qs.select_related("employe").order_by("-clicked_at")[:10]:
        recent_completions.append(
            {
                "employee": track.employe,
                "completed_at": track.clicked_at,
            }
        )

    # Department performance
    dept_performance = []
    for dept in departments:
        dept_employees = Employes.objects.filter(departement=dept).values_list(
            "matricule", flat=True
        )
        dept_results = qcm_results.filter(employee_matricule__in=dept_employees)
        dept_avg = round(dept_results.aggregate(avg=Avg("score"))["avg"] or 0, 1)
        dept_count = dept_results.count()

        dept_performance.append(
            {
                "name": dept.name,
                "avg_score": dept_avg,
                "completed_count": dept_count,
            }
        )

    context = {
        "active_page": "training",
        "departments": departments,
        "selected_days": days,
        "selected_department": department_id,
        # KPIs
        "total_completed_training": total_completed_training,
        "total_employees": total_employees,
        "completion_rate": completion_rate,
        "avg_score": round(avg_score, 1),
        "total_quizzes_taken": qcm_results.count(),
        # Score distribution
        "score_0_20": score_0_20,
        "score_21_40": score_21_40,
        "score_41_60": score_41_60,
        "score_61_80": score_61_80,
        "score_81_100": score_81_100,
        # Attempts distribution
        "attempts_1": attempts_1,
        "attempts_2": attempts_2,
        "attempts_3": attempts_3,
        "attempts_4plus": attempts_4plus,
        # Trends
        "trend_labels": trend_labels,
        "trend_data": trend_data,
        # Top performers
        "top_performers": top_performers,
        # Recent completions
        "recent_completions": recent_completions,
        # Department performance
        "dept_performance": dept_performance,
    }

    return render(request, "admin/training_awareness.html", context)


@login_required(login_url="/admin/login")
def dashboard(request):

    admin = request.user

    days = int(request.GET.get("days", 30))

    departements = Departement.objects.all()

    all_results = QcmResult.objects.all()

    # Calculate statistics
    total_qcm_taken = all_results.count()
    avg_score = all_results.aggregate(avg=Avg("score"))["avg"] or 0

    # Score distribution
    score_0_20 = all_results.filter(score__lte=20).count()
    score_21_40 = all_results.filter(score__gt=20, score__lte=40).count()
    score_41_60 = all_results.filter(score__gt=40, score__lte=60).count()
    score_61_80 = all_results.filter(score__gt=60, score__lte=80).count()
    score_81_100 = all_results.filter(score__gt=80).count()

    # Top performers
    top_performers = []
    for result in all_results.order_by("-score")[:10]:
        try:
            employee = Employes.objects.get(matricule=result.employee_matricule)
            name = f"{employee.first_name} {employee.last_name}"
        except Employes.DoesNotExist:
            name = result.employee_matricule

        top_performers.append(
            {
                "employee_name": name,
                "employee_matricule": result.employee_matricule,
                "score": result.score,
                "totale_qcm_taken": result.totale_qcm_taken,
            }
        )

    context = {
        "user": request.user,
        "departments": departements,
        "selected_days": days,
        "admin_department": admin.departement.name if admin.departement else None,
        # QCM Results
        "total_qcm_taken": total_qcm_taken,
        "avg_score": round(avg_score, 1),
        "score_0_20": score_0_20,
        "score_21_40": score_21_40,
        "score_41_60": score_41_60,
        "score_61_80": score_61_80,
        "score_81_100": score_81_100,
        "top_performers": top_performers,
    }

    context.update(get_phishing_data(days))

    return render(request, "admin/dashboard.html", context=context)


# Admin Profile :


@login_required
def profile_view(request):
    admin_user = request.user

    if request.method == "POST":
        form = AdminProfileForm(request.POST, instance=admin_user)
        if form.is_valid():
            form.save()
            messages.success(request, "Your profile has been updated successfully!")
            return redirect("profile")
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = AdminProfileForm(instance=admin_user)

    context = {
        "form": form,
        "admin_user": admin_user,
    }
    return render(request, "admin/profile.html", context)
