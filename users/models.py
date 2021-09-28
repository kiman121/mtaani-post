from django.db import models
from django.contrib.auth.models import User
from django.dispatch import receiver
import uuid

from neighbourhoods.models import Neighbourhood
# Create your models here.
class Profile(models.Model):
    SYSTEM_USERS = (
        ('user', 'User'),
        ('admin', 'Admin')
    )
    
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, null=True, blank=True)
    first_name = models.CharField(max_length=200, null=True)
    other_name = models.CharField(max_length=200, null=True)
    email = models.EmailField(max_length=500, blank=True, null=True)
    phone_number = models.CharField(max_length=200, blank=True, null=True)
    username = models.CharField(max_length=200, blank=True, null=True)
    user_type =models.CharField(max_length=200, choices=SYSTEM_USERS, default='user',blank=True, null=True,)
    neighbourhood = models.ForeignKey(
        Neighbourhood, on_delete=models.SET_NULL, null=True)
    profile_image = models.ImageField(
        blank=True, null=True, upload_to='profiles/', default='profiles/user-default.png')
    created = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(default=uuid.uuid4, unique=True,
                          primary_key=True, editable=False)

    def __str__(self):
        return str(self.username)

    class Meta:
        ordering = ['created']

    @property
    def imageUrl(self):
        try:
            url = self.profile_image.url
        except:
            url = ''
        return url
