from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('business-list/', views.businessList, name='business-list'),
    path('neighbourhood-list/',views.neighbourhoodList, name='neighbourhood-list'),
    path('add-neighbourhood/', views.addNeighbourhood, name='add-neighbourhood'),
    path('add-contact/', views.addContact, name='add-contact'),
    path('add-post/', views.addPost, name='add-post'),
    path('add-business/', views.addBusiness, name='add-business'),
]