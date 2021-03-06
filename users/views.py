from django.shortcuts import render, redirect
from django.contrib.auth import login,authenticate,logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User
from django.http import JsonResponse

from .forms import CustomUserCreationForm, ProfileForm
from .models import Profile
# Create your views here.
def loginUser(request):

    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        username = request.POST['username'].lower()
        password = request.POST['password']

        try:
            user = User.objects.get(username=username)
        except:
            messages.error(request, 'Wrong username or password')
        
        user = authenticate(request, username = username, password=password)

        if user is not None:
            login(request, user)
            return redirect(request.GET['next'] if 'next' in request.GET else 'home')
        else:
            messages.error(request, 'Username or password is incorrect')

    return render(request, 'users/login.html')

def registerUser(request):
    form = CustomUserCreationForm()

    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()


            messages.success(request, 'User account was created!')

            login(request, user)
            return redirect('home')
        else:
            messages.success(
                request, 'An error has occurred during registration!')


    return render(request, 'users/register.html', {'form':form})

@login_required(login_url='login')
def editProfile(request, pk):
    profile = Profile.objects.get(id=pk)
    form = ProfileForm(instance=profile)
    print('outside')
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        print('out')
        if form.is_valid():
            print('in')
            form.save()

    return redirect(request.GET['next'] if 'next' in request.GET else 'profile')

@login_required(login_url='login')
def getProfile(request, pk):
    profile = Profile.objects.get(id=pk)

    data = {
        'first_name': profile.first_name,
        'other_name': profile.other_name,
        'email': profile.email,
        'phone_number': profile.phone_number,
        'username':profile.username,
        'user_type':profile.user_type,
        'neighbourhood':profile.neighbourhood.id,
    }
    return JsonResponse(data)


def logoutUser(request):
    logout(request)
    messages.info(request, 'User was logged out!')
    return redirect('login')
    
@login_required(login_url='login')
def profile(request):
    profile = request.user.profile
    form = ProfileForm(instance=profile)

    return render(request, 'users/profile.html', {'form':form})

@login_required(login_url='login')
def users(request):
    form = ProfileForm()
    profiles = Profile.objects.all()
    return render(request, 'users/users.html', {'profiles':profiles, 'form':form})