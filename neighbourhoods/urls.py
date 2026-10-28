from django.urls import path

from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("business-list/", views.business_list, name="business-list"),
    path("neighbourhood-list/", views.neighbourhood_list, name="neighbourhood-list"),
]
