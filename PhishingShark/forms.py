from django import forms
from .models import Administrateur


class AdminProfileForm(forms.ModelForm):
    """ModelForm for updating admin profile information."""

    class Meta:
        model = Administrateur
        fields = ["first_name", "last_name", "email"]
        widgets = {
            "first_name": forms.TextInput(
                attrs={"class": "form-input", "placeholder": "First Name"}
            ),
            "last_name": forms.TextInput(
                attrs={"class": "form-input", "placeholder": "Last Name"}
            ),
            "email": forms.EmailInput(
                attrs={"class": "form-input", "placeholder": "Email Address"}
            ),
        }

    def clean_email(self):
        """Validate email uniqueness."""
        email = self.cleaned_data.get("email")
        if (
            Administrateur.objects.exclude(pk=self.instance.pk)
            .filter(email=email)
            .exists()
        ):
            raise forms.ValidationError("This email is already in use.")
        return email
