from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from django.utils.http import url_has_allowed_host_and_scheme

from .forms import CustomUserCreationForm, ProfileForm
from .models import Profile


def _safe_next(request):
    candidate = request.POST.get("next") or request.GET.get("next")
    if candidate and url_has_allowed_host_and_scheme(
        candidate,
        allowed_hosts={request.get_host()},
        require_https=request.is_secure(),
    ):
        return candidate
    return None


def login_user(request):
    if request.user.is_authenticated:
        return redirect("home")

    username = ""
    if request.method == "POST":
        username = request.POST.get("username", "").strip().lower()
        password = request.POST.get("password", "")
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect(_safe_next(request) or "home")
        messages.error(request, "Username or password is incorrect.")

    return render(request, "users/login.html", {"username": username})


def logout_user(request):
    if request.method == "POST":
        logout(request)
        messages.info(request, "You are signed out.")
    return redirect("login")


def register_user(request):
    if request.user.is_authenticated:
        return redirect("home")

    form = CustomUserCreationForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        user = form.save(commit=False)
        user.username = user.username.lower()
        user.save()
        login(request, user)
        messages.success(request, "Account created.")
        return redirect("home")

    return render(request, "users/register.html", {"form": form})


@login_required
def profile(request):
    person = request.user.profile
    if request.method == "POST":
        form = ProfileForm(request.POST, request.FILES, instance=person)
    else:
        form = ProfileForm(instance=person)
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Profile saved.")
        return redirect("profile")

    return render(request, "users/profile.html", {"form": form, "profile": person})


@login_required
def residents(request):
    profiles = Profile.objects.select_related("neighbourhood").all()
    return render(request, "users/users.html", {"profiles": profiles})
