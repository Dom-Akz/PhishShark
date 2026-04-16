from django.db import models


class Departement:
    name = models.CharField(max_length=100, unique=True)
    description = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    @property
    def totale_employee(self):
        return self.employees.count()


# Model Administrateur :
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


class Employes:
    uuid = models.CharField(max_length=50, unique=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(max_length=100, unique=True)
    departement = models.ForeignKey(
        Departement, on_delete=models.SET_NULL, null=True, related_name="employees"
    )

    # add related info here :

    updated_at = models.DateTimeField(auto_now_add=True)
    created_at = models.DateTimeField(auto_now_add=True)
