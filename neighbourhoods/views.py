from django.shortcuts import render, redirect
from django.contrib import messages

from .models import Neighbourhood,Post,Contact, Business
from .forms import NeighbourhoodForm, ContactForm, PostForm, BusinessForm

# Create your views here.

def home(request):
    neighbourhood = request.user.profile.neighbourhood
    posts = Post.objects.filter(neighbourhood=neighbourhood)
    contacts = Contact.objects.filter(neighbourhood=neighbourhood)
    
    context = {
        'posts': posts,
        'contacts': contacts,
        'form': PostForm(),
    }

    return render(request, 'neighbourhoods/home.html',context)

def businessList(request):
    form = BusinessForm()
    neighbourhood = request.user.profile.neighbourhood
    businesses = Business.objects.filter(neighbourhood=neighbourhood)

    context={
        'form':form,
        'businesses':businesses,
    }
    return render(request, 'neighbourhoods/business-list.html', context)

def neighbourhoodList(request):
    context={
        'addNeighbourhoodForm': NeighbourhoodForm(),
        'neighbourhoods': Neighbourhood.objects.all(),
        'addContactForm': ContactForm(),
    }
    return render(request, 'neighbourhoods/neighbourhood-list.html',context)

def addNeighbourhood(request):
    form = NeighbourhoodForm()
    if request.method == 'POST':
        form = NeighbourhoodForm(request.POST)
        if form.is_valid():
            neighbourhood = form.save(commit=False)
            neighbourhood.owner = request.user
            neighbourhood.save()

            messages.success(request, 'Neighbourhood added successfully!')

        else:
            messages.success(
                request, 'An error has occurred!')
    
    return redirect('neighbourhood-list')

def addContact(request):
    form = ContactForm
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            contact = form.save(commit=False)
            contact.neighbourhood = request.user.profile.neighbourhood
            contact.save()

            messages.success(request, 'Contact added successfully!')

        else:
            messages.success(
                request, 'An error has occurred!')
    
    return redirect('neighbourhood-list')

def addPost(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.owner = request.user
            post.neighbourhood = request.user.profile.neighbourhood
            post.save()

            messages.success(request, 'Post added successfully!')

        else:
            messages.success(
                request, 'An error has occurred!')
    
    return redirect('home')


def addBusiness(request):
    if request.method == 'POST':
        form = BusinessForm(request.POST)
        if form.is_valid():
                business = form.save(commit=False)
                business.owner = request.user
                business.neighbourhood = request.user.profile.neighbourhood
                business.save()

                messages.success(request, 'Business added successfully!')

        else:
            messages.success(
                request, 'An error has occurred!')
    
    return redirect('business-list')