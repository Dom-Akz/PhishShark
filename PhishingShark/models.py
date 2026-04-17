from django.db import models


class Departement(models.Model):
    name = models.CharField(max_length=100, unique=True)
    chef_departement = models.CharField(max_length=100)
    description = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


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


class Entreprise(models.Model):
    name = models.CharField(max_length=100)
    administrateur = models.ForeignKey(
        Administrateur, on_delete=models.SET_NULL, null=True, related_name="entreprise"
    )

    def __str__(self):
        return self.name


class Employes(models.Model):
    # this is just a internal identifer (use only inside the project apps to identife the Employes)
    # entreprise-Fisrt/last-Letterfrom(first_name/last_name)-year(2026)-id
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

    # add related info here :

    updated_at = models.DateTimeField(auto_now_add=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.first_name
