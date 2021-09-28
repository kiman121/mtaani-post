from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse

from .models import Neighbourhood,Post,Contact, Business
from .forms import NeighbourhoodForm, ContactForm, PostForm, BusinessForm

# Create your views here.
@login_required(login_url='login')
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

@login_required(login_url='login')
def businessList(request):
    form = BusinessForm()
    neighbourhood = request.user.profile.neighbourhood
    businesses = Business.objects.filter(neighbourhood=neighbourhood)

    context={
        'form':form,
        'businesses':businesses,
    }
    return render(request, 'neighbourhoods/business-list.html', context)

@login_required(login_url='login')
def neighbourhoodList(request):
    context={
        'addNeighbourhoodForm': NeighbourhoodForm(),
        'neighbourhoods': Neighbourhood.objects.all(),
        'addContactForm': ContactForm(),
    }
    return render(request, 'neighbourhoods/neighbourhood-list.html',context)

@login_required(login_url='login')
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


# @login_required(login_url='login')
# def editProfile(request):
#     profile = request.user.profile
#     form = ProfileForm(instance=profile)
    
#     if request.method == 'POST':
#         form = ProfileForm(request.POST, request.FILES, instance=profile)
#         if form.is_valid():
#             form.save()
#             return redirect('profile')

#     return render(request, 'users/profile.html', {'form':form})

@login_required(login_url='login')
def getNeighbourhood(request, pk):
    neighbourhood = Neighbourhood.objects.get(id=pk)

    data = {
        'name': neighbourhood.name,
        'location': neighbourhood.location,
    }
    return JsonResponse(data)


@login_required(login_url='login')
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

@login_required(login_url='login')
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

@login_required(login_url='login')
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