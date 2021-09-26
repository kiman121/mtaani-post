from django.shortcuts import render, redirect
from django.contrib.auth import login,authenticate,logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User


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

def logoutUser(request):
    logout(request)
    messages.info(request, 'User was logged out!')
    return redirect('login')
    
@login_required(login_url='login')
def profile(request):
    return render(request, 'users/profile.html')

@login_required(login_url='login')
def users(request):
    return render(request, 'users/users.html')