from django.shortcuts import render

# Create your views here.

def home(request):
    return render(request, 'neighbourhoods/home.html')

def businessList(request):
    return render(request, 'neighbourhoods/business-list.html')

def neighbourhoodList(request):
    return render(request, 'neighbourhoods/neighbourhood-list.html')