from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Count
from django.shortcuts import redirect, render

from .forms import BusinessForm, ContactForm, NeighbourhoodForm, PostForm
from .models import Business, Contact, Neighbourhood, Post


def _neighbourhood(user):
    return user.profile.neighbourhood


@login_required
def home(request):
    neighbourhood = _neighbourhood(request.user)
    form = PostForm()

    if request.method == "POST":
        if neighbourhood is None:
            messages.error(request, "Choose a neighbourhood on your profile before posting.")
            return redirect("profile")
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.owner = request.user
            post.neighbourhood = neighbourhood
            post.save()
            messages.success(request, "Notice posted.")
            return redirect("home")

    if neighbourhood is None:
        posts = Post.objects.none()
        contacts = Contact.objects.none()
    else:
        posts = Post.objects.filter(neighbourhood=neighbourhood).select_related("owner__profile")
        contacts = Contact.objects.filter(neighbourhood=neighbourhood)

    return render(
        request,
        "neighbourhoods/home.html",
        {
            "posts": posts,
            "health_contacts": contacts.filter(category="health"),
            "security_contacts": contacts.filter(category="security"),
            "form": form,
            "neighbourhood": neighbourhood,
        },
    )


@login_required
def business_list(request):
    neighbourhood = _neighbourhood(request.user)
    form = BusinessForm()

    if request.method == "POST":
        if neighbourhood is None:
            messages.error(request, "Choose a neighbourhood on your profile before adding a business.")
            return redirect("profile")
        form = BusinessForm(request.POST)
        if form.is_valid():
            business = form.save(commit=False)
            business.owner = request.user
            business.neighbourhood = neighbourhood
            business.save()
            messages.success(request, "Business added.")
            return redirect("business-list")

    businesses = Business.objects.none()
    if neighbourhood is not None:
        businesses = Business.objects.filter(neighbourhood=neighbourhood).select_related("owner__profile")

    return render(
        request,
        "neighbourhoods/business-list.html",
        {
            "form": form,
            "businesses": businesses,
            "neighbourhood": neighbourhood,
        },
    )


@login_required
def neighbourhood_list(request):
    neighbourhood = _neighbourhood(request.user)
    neighbourhood_form = NeighbourhoodForm(prefix="area")
    contact_form = ContactForm(prefix="contact")

    if request.method == "POST" and request.POST.get("action") == "neighbourhood":
        neighbourhood_form = NeighbourhoodForm(request.POST, prefix="area")
        if neighbourhood_form.is_valid():
            created = neighbourhood_form.save(commit=False)
            created.owner = request.user
            created.save()
            messages.success(request, "Neighbourhood added. Join it from your profile.")
            return redirect("neighbourhood-list")

    if request.method == "POST" and request.POST.get("action") == "contact":
        if neighbourhood is None:
            messages.error(request, "Choose a neighbourhood on your profile before adding a contact.")
            return redirect("profile")
        contact_form = ContactForm(request.POST, prefix="contact")
        if contact_form.is_valid():
            contact = contact_form.save(commit=False)
            contact.neighbourhood = neighbourhood
            contact.save()
            messages.success(request, "Contact added.")
            return redirect("neighbourhood-list")

    neighbourhoods = (
        Neighbourhood.objects.select_related("owner")
        .annotate(resident_count=Count("profile"))
        .order_by("name")
    )
    return render(
        request,
        "neighbourhoods/neighbourhood-list.html",
        {
            "neighbourhoods": neighbourhoods,
            "neighbourhood_form": neighbourhood_form,
            "contact_form": contact_form,
            "neighbourhood": neighbourhood,
        },
    )
