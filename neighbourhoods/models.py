from django.db import models
from django.contrib.auth.models import User
import uuid

# from users.models import Profile

# Create your models here.
class Neighbourhood(models.Model):
    owner = models.ForeignKey(
        User, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=200, blank=True, null=True)
    location = models.CharField(max_length=200, blank=True, null=True)
    occupants_count = models.IntegerField(default=0, null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(default=uuid.uuid4, unique=True,
                          primary_key=True, editable=False)

    def __str__(self):
        return str(self.name)
    
class Post(models.Model):
    POST_TYPES = (
        ('news', 'News'),
        ('announcement', 'Announcement')
    )
    owner = models.ForeignKey(
        User, on_delete=models.CASCADE, null=True, blank=True)
    title = models.CharField(max_length=200, blank=True, null=True)
    description = models.TextField(null=True, blank=True)
    neighbourhood = models.ForeignKey(
        Neighbourhood, on_delete=models.CASCADE, null=True)
    post_type =models.CharField(max_length=200, choices=POST_TYPES)
    created = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(default=uuid.uuid4, unique=True,
                          primary_key=True, editable=False)

    class Meta:
        ordering = ['-created']

    def __str__(self):
        return str(self.title)

class Contact(models.Model):
    CATEGORY = (
        ('health', 'Health'),
        ('security', 'Security')
    )
    neighbourhood = models.ForeignKey(
        Neighbourhood, on_delete=models.CASCADE, null=True)
    name = models.CharField(max_length=200, blank=True, null=True)
    email = models.EmailField(max_length=500, blank=True, null=True)
    phone_number = models.CharField(max_length=200, blank=True, null=True)
    location = models.CharField(max_length=200, blank=True, null=True)
    category =models.CharField(max_length=200, choices=CATEGORY)
    created = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(default=uuid.uuid4, unique=True,
                          primary_key=True, editable=False)

class Business(models.Model):
    neighbourhood = models.ForeignKey(
        Neighbourhood, on_delete=models.CASCADE, null=True)
    owner = models.ForeignKey(
        User, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=200, blank=True, null=True)
    email = models.EmailField(max_length=500, blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(default=uuid.uuid4, unique=True,
                          primary_key=True, editable=False)