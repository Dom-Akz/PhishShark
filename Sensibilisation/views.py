from django.shortcuts import render
from .models import QcmResult, Sensibilisation
from django.contrib.auth.decorators import login_required
from PhishingShark.models import Employes, EmailTracking


@login_required
def training_page(request):

    # Get tracking UUID from URL
    tracking_uuid = request.GET.get("rid", "")
    employee_name = None
    employee_email = None

    # Try to find employee by tracking UUID
    if tracking_uuid:
        try:
            email_tracking = EmailTracking.objects.get(uuid=tracking_uuid)
            employee = email_tracking.employe
            employee_name = f"{employee.first_name} {employee.last_name}"
            employee_email = employee.email
        except EmailTracking.DoesNotExist:
            pass

    context = {
        "tracking_uuid": tracking_uuid,
        "employee_name": employee_name,
        "employee_email": employee_email,
    }

    return render(request, "sensibilisation/sens.html", context)
