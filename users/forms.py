from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.forms import FileInput, ModelForm

from .models import Profile


def style_fields(form):
    for field in form.fields.values():
        field.widget.attrs.setdefault("class", "field")


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ("first_name", "email", "username", "password1", "password2")
        labels = {
            "first_name": "First name",
            "email": "Email",
            "username": "Username",
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["first_name"].widget.attrs["autocomplete"] = "given-name"
        self.fields["email"].widget.attrs["autocomplete"] = "email"
        self.fields["username"].widget.attrs["autocomplete"] = "username"
        self.fields["password1"].widget.attrs["autocomplete"] = "new-password"
        self.fields["password2"].widget.attrs["autocomplete"] = "new-password"
        style_fields(self)


class ProfileForm(ModelForm):
    class Meta:
        model = Profile
        fields = (
            "first_name",
            "other_name",
            "username",
            "phone_number",
            "email",
            "neighbourhood",
            "profile_image",
        )
        labels = {
            "first_name": "First name",
            "other_name": "Other names",
            "username": "Username",
            "phone_number": "Phone",
            "email": "Email",
            "neighbourhood": "Neighbourhood",
            "profile_image": "Photo",
        }
        widgets = {
            "profile_image": FileInput(),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["neighbourhood"].empty_label = "Choose a neighbourhood"
        self.fields["other_name"].required = False
        self.fields["phone_number"].required = False
        self.fields["first_name"].widget.attrs["autocomplete"] = "given-name"
        self.fields["other_name"].widget.attrs["autocomplete"] = "additional-name"
        self.fields["username"].widget.attrs["autocomplete"] = "username"
        self.fields["phone_number"].widget.attrs["autocomplete"] = "tel"
        self.fields["email"].widget.attrs["autocomplete"] = "email"
        style_fields(self)

    def clean_username(self):
        username = self.cleaned_data["username"]
        taken = User.objects.exclude(pk=self.instance.user_id).filter(username=username)
        if username and taken.exists():
            raise ValidationError("That username is already taken.")
        return username
