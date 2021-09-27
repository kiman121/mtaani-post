from django.shortcuts import render, redirect
from django.contrib import messages

from .models import Neighbourhood
from .forms import NeighbourhoodForm

# Create your views here.

def home(request):
    
    return render(request, 'neighbourhoods/home.html')

def businessList(request):
    return render(request, 'neighbourhoods/business-list.html')

def neighbourhoodList(request):
    form = NeighbourhoodForm()
    neighbourhoods = Neighbourhood.objects.all()
    return render(request, 'neighbourhoods/neighbourhood-list.html',{'neighbourhoods':neighbourhoods, 'form':form})

def addNeighbourhood(request):
    form = NeighbourhoodForm()
    if request.method == 'POST':
        form = NeighbourhoodForm(request.POST)
        if form.is_valid():
            neighbourhood = form.save(commit=False)
            neighbourhood.owner = request.user
            neighbourhood.save()

            messages.success(request, 'Neighbourhood add successfully!')

        else:
            messages.success(
                request, 'An error has occurred!')
    
    return redirect('neighbourhood-list')