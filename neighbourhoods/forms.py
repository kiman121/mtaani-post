from django.forms import ModelForm, Textarea

from .models import Business, Contact, Neighbourhood, Post


def style_fields(form):
    for field in form.fields.values():
        field.widget.attrs.setdefault("class", "field")


def drop_blank_choice(field):
    field.choices = [(value, label) for value, label in field.choices if value]


class NeighbourhoodForm(ModelForm):
    class Meta:
        model = Neighbourhood
        fields = ("name", "location")
        labels = {
            "name": "Name",
            "location": "Location",
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["name"].required = True
        self.fields["location"].required = True
        style_fields(self)


class ContactForm(ModelForm):
    class Meta:
        model = Contact
        fields = ("name", "phone_number", "email", "location", "category")
        labels = {
            "name": "Name",
            "phone_number": "Phone",
            "email": "Email",
            "location": "Location",
            "category": "Category",
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["name"].required = True
        drop_blank_choice(self.fields["category"])
        self.fields["phone_number"].widget.attrs["autocomplete"] = "tel"
        self.fields["email"].widget.attrs["autocomplete"] = "email"
        style_fields(self)


class PostForm(ModelForm):
    class Meta:
        model = Post
        fields = ("post_type", "title", "description")
        labels = {
            "post_type": "Type",
            "title": "Title",
            "description": "Details",
        }
        widgets = {
            "description": Textarea(attrs={"rows": 4, "class": "field"}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["title"].required = True
        self.fields["description"].required = True
        drop_blank_choice(self.fields["post_type"])
        style_fields(self)


class BusinessForm(ModelForm):
    class Meta:
        model = Business
        fields = ("name", "description", "phone_number", "email")
        labels = {
            "name": "Name",
            "description": "What they offer",
            "phone_number": "Phone",
            "email": "Email",
        }
        widgets = {
            "description": Textarea(attrs={"rows": 3, "class": "field"}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["name"].required = True
        self.fields["description"].required = True
        self.fields["phone_number"].widget.attrs["autocomplete"] = "tel"
        self.fields["email"].widget.attrs["autocomplete"] = "email"
        style_fields(self)
