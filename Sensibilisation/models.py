from django.db import models
from PhishingShark.models import Employes
from PhishingShark.models import EMAIL_STATUS_CHOICES


# this is the quiz result class (the question are store in static json file: Qcm_Database/qcm.json)
class QcmResult(models.Model):
    employee_matricule = models.CharField(max_length=100, unique=True)
    employee_email = models.EmailField(null=True, blank=True)
    # socre evaluate wiht (%), 20 question in totale
    score = models.PositiveIntegerField(default=0)

    # both in this format (hh:mm)
    # both can be use to calculate the totale time
    start_at = models.TimeField()
    finish_at = models.TimeField()

    # the amount of time the employees take the quiz
    totale_qcm_taken = models.IntegerField(default=0)

    def __str__(self):
        return self.score

    def totale_time_spent(self):
        pass


class Sensibilisation(models.Model):
    employee = models.ForeignKey(
        Employes, on_delete=models.SET_NULL, null=True, related_name="sensibilisation"
    )

    employee_matricule = models.CharField(max_length=100)

    # totale time spen reading the Sensibilisation page (hh:mm)
    totale_time = models.TimeField()

    read_count = models.IntegerField(default=0)


class AlertsEmails(models.Model):
    employee = models.ForeignKey(
        Employes, on_delete=models.SET_NULL, null=True, related_name="alerts_email"
    )
    status = models.CharField(
        max_length=20, choices=EMAIL_STATUS_CHOICES, default="PENDING"
    )
    send_date = models.DateTimeField(auto_now_add=True)
    clicked_at = models.DateTimeField(null=True, blank=True)
    received_date = models.DateTimeField(null=True, blank=True)
    ip_address = models.GenericIPAddressField(
        protocol="both", null=True, unpack_ipv4=False
    )
