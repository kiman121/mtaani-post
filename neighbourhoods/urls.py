from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('business-list/', views.businessList, name='business-list'),
    path('Neighbourhood-list',views.neighbourhoodList, name='neighbourhood-list'),
]