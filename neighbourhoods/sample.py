import uuid

from django.contrib.auth.models import User

from .models import Business, Contact, Neighbourhood, Post

SAMPLE_ID = uuid.UUID("11111111-1111-4111-8111-111111111111")


def ensure_sample():
    area, created = Neighbourhood.objects.get_or_create(
        id=SAMPLE_ID,
        defaults={
            "name": "Kileleshwa",
            "location": "Nairobi",
            "is_sample": True,
        },
    )
    if not created:
        return area

    resident, was_created = User.objects.get_or_create(
        username="mtaani-sample",
        defaults={"email": "sample@mtaani.local", "first_name": "Amina"},
    )
    if was_created:
        resident.set_unusable_password()
        resident.save()

    profile = resident.profile
    profile.first_name = "Amina"
    profile.neighbourhood = area
    profile.save()
    area.owner = resident
    area.is_sample = True
    area.save()

    Post.objects.create(
        owner=resident,
        title="Water interruption on Thursday",
        description="Supply along Othaya Road is off from 9am to 4pm.",
        neighbourhood=area,
        post_type="announcement",
    )
    Contact.objects.create(
        neighbourhood=area,
        name="Kileleshwa clinic",
        phone_number="0700 111 222",
        location="Othaya Road",
        category="health",
    )
    Contact.objects.create(
        neighbourhood=area,
        name="Police desk",
        phone_number="0700 333 444",
        location="Ring Road",
        category="security",
    )
    Business.objects.create(
        neighbourhood=area,
        owner=resident,
        name="Corner grocer",
        email="grocer@example.com",
        phone_number="0711 222 333",
        description="Vegetables and bread. Open until eight in the evening.",
    )
    return area
