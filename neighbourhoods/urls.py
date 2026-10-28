from django.urls import path
from django.views.generic import RedirectView

from . import views

urlpatterns = [
    path("", RedirectView.as_view(pattern_name="home", permanent=False)),
    path("business-list/", views.business_list, name="business-list"),
    path("neighbourhood-list/", views.neighbourhood_list, name="neighbourhood-list"),
    path("notices/<uuid:pk>/edit/", views.edit_post, name="edit-post"),
    path("notices/<uuid:pk>/delete/", views.delete_post, name="delete-post"),
    path("contacts/<uuid:pk>/edit/", views.edit_contact, name="edit-contact"),
    path("contacts/<uuid:pk>/delete/", views.delete_contact, name="delete-contact"),
    path("businesses/<uuid:pk>/edit/", views.edit_business, name="edit-business"),
    path("businesses/<uuid:pk>/delete/", views.delete_business, name="delete-business"),
    path("places/<uuid:pk>/edit/", views.edit_neighbourhood, name="edit-neighbourhood"),
    path("places/<uuid:pk>/delete/", views.delete_neighbourhood, name="delete-neighbourhood"),
]
