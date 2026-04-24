from django.db import models


EMAIL_STATUS_CHOICES = [
    ("PENDING", "Pending"),
    ("SENT", "Sent"),
    ("RECEIVED", "Received"),
    ("CLICK", "click"),
    ("FAILED", "Failed"),
]

EMAIL_TYPE_CHOICES = [
    ("COMPANY_EMAIL", "company_email"),
    ("PAYMENT_REQUEST", "payment_request"),
    ("JOB_OFFER", "job_offer"),
    ("ID_DEP", "it_dep"),
    ("SCAM_IPHONE", "scam_iphone"),
    ("SCAM_LOTTERY", "scam_lottery"),
    ("SECURITY_ALERT", "security_alert"),
]


class Departement(models.Model):
    name = models.CharField(max_length=100, unique=True)
    chef_departement = models.CharField(max_length=100)
    description = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class Administrateur(models.Model):
    name = models.CharField(max_length=100)
    username = models.CharField(max_length=100, unique=True)
    email = models.EmailField(max_length=100, unique=True)
    password = models.CharField(
        max_length=500,
        unique=True,
    )
    departement = models.ForeignKey(
        Departement, on_delete=models.SET_NULL, null=True, related_name="admin"
    )
    is_active = models.BooleanField(default=False)
    is_supperuser = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class Entreprise(models.Model):
    name = models.CharField(max_length=100)
    alias = models.CharField(max_length=20, null=True)
    administrateur = models.ForeignKey(
        Administrateur, on_delete=models.SET_NULL, null=True, related_name="entreprise"
    )

    def __str__(self):
        return self.name


class Employes(models.Model):
    # this is just a internal identifer (use only inside the project apps to identife the Employes)
    # alias-last-Letterfrom(first_name/last_name)-year(2026)-id
    matricule = models.CharField(max_length=100, unique=True)

    # this is use in email generation.
    # structure : dep_chefdep_locatisation_Entreprise
    ink = models.CharField(max_length=500)

    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(max_length=100, unique=True)
    location = models.CharField(max_length=200)

    entreprise = models.ForeignKey(
        Entreprise, on_delete=models.SET_NULL, null=True, related_name="employees"
    )
    departement = models.ForeignKey(
        Departement, on_delete=models.SET_NULL, null=True, related_name="employees"
    )

    # related info here :

    updated_at = models.DateTimeField(auto_now_add=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.first_name


class EmailTracking(models.Model):
    employe = models.ForeignKey(
        Employes, on_delete=models.CASCADE, related_name="email_tracking"
    )
    type = models.CharField(max_length=20, choices=EMAIL_TYPE_CHOICES)
    status = models.CharField(
        max_length=20, choices=EMAIL_STATUS_CHOICES, default="PENDING"
    )
    send_date = models.DateTimeField(auto_now_add=True)
    clicked_at = models.DateTimeField(null=True, blank=True)
    received_date = models.DateTimeField(null=True, blank=True)
    ip_address = models.GenericIPAddressField(
        protocol="both", null=True, unpack_ipv4=False
    )
    # use to track the email by the employe
    uuid = models.CharField(max_length=100, unique=True)
