from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.db.models import Count
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.views.decorators.http import require_POST

from .forms import BusinessForm, ContactForm, NeighbourhoodForm, PostForm
from .models import Business, Contact, Neighbourhood, Post
from .sample import ensure_sample


def _neighbourhood(user):
    return user.profile.neighbourhood


def _same_neighbourhood(user, neighbourhood):
    return (
        neighbourhood is not None
        and user.is_authenticated
        and user.profile.neighbourhood_id == neighbourhood.id
    )


def _feed(neighbourhood):
    posts = Post.objects.filter(neighbourhood=neighbourhood).select_related("owner__profile")
    contacts = Contact.objects.filter(neighbourhood=neighbourhood)
    return posts, contacts.filter(category="health"), contacts.filter(category="security")


def home(request):
    if not request.user.is_authenticated:
        if request.method == "POST":
            return redirect(f"/login/?next=/")
        area = ensure_sample()
        posts, health, security = _feed(area)
        return render(
            request,
            "neighbourhoods/home.html",
            {
                "posts": posts,
                "health_contacts": health,
                "security_contacts": security,
                "neighbourhood": area,
                "read_only": True,
            },
        )

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
        health = Contact.objects.none()
        security = Contact.objects.none()
    else:
        posts, health, security = _feed(neighbourhood)

    return render(
        request,
        "neighbourhoods/home.html",
        {
            "posts": posts,
            "health_contacts": health,
            "security_contacts": security,
            "form": form,
            "neighbourhood": neighbourhood,
            "read_only": False,
        },
    )


def business_list(request):
    if not request.user.is_authenticated:
        area = ensure_sample()
        businesses = Business.objects.filter(neighbourhood=area).select_related("owner__profile")
        return render(
            request,
            "neighbourhoods/business-list.html",
            {"businesses": businesses, "neighbourhood": area, "read_only": True},
        )

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
            "read_only": False,
        },
    )


@login_required
def neighbourhood_list(request):
    ensure_sample()
    neighbourhood = _neighbourhood(request.user)
    neighbourhood_form = NeighbourhoodForm(prefix="area")
    contact_form = ContactForm(prefix="contact")

    if request.method == "POST" and request.POST.get("action") == "neighbourhood":
        neighbourhood_form = NeighbourhoodForm(request.POST, prefix="area")
        if neighbourhood_form.is_valid():
            created = neighbourhood_form.save(commit=False)
            created.owner = request.user
            created.save()
            profile = request.user.profile
            if profile.neighbourhood_id is None:
                profile.neighbourhood = created
                profile.save()
                messages.success(request, "Neighbourhood added. This is your feed.")
                return redirect("home")
            messages.success(request, "Neighbourhood added. Switch to it from your profile when you want its feed.")
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


def _editor(request, form, heading, eyebrow, delete_name, pk, can_delete=True):
    return render(
        request,
        "edit_record.html",
        {
            "form": form,
            "heading": heading,
            "eyebrow": eyebrow,
            "delete_url": reverse(delete_name, args=[pk]),
            "can_delete": can_delete,
        },
    )


@login_required
def edit_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if post.owner_id != request.user.id:
        raise PermissionDenied
    form = PostForm(request.POST or None, instance=post)
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Notice updated.")
        return redirect("home")
    return _editor(request, form, post.title, "Notice", "delete-post", post.id)


@login_required
@require_POST
def delete_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if post.owner_id != request.user.id:
        raise PermissionDenied
    post.delete()
    messages.success(request, "Notice removed.")
    return redirect("home")


@login_required
def edit_contact(request, pk):
    contact = get_object_or_404(Contact, pk=pk)
    if not _same_neighbourhood(request.user, contact.neighbourhood):
        raise PermissionDenied
    form = ContactForm(request.POST or None, instance=contact)
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Contact updated.")
        return redirect("home")
    return _editor(request, form, contact.name, "Contact", "delete-contact", contact.id)


@login_required
@require_POST
def delete_contact(request, pk):
    contact = get_object_or_404(Contact, pk=pk)
    if not _same_neighbourhood(request.user, contact.neighbourhood):
        raise PermissionDenied
    contact.delete()
    messages.success(request, "Contact removed.")
    return redirect("home")


@login_required
def edit_business(request, pk):
    business = get_object_or_404(Business, pk=pk)
    if not _same_neighbourhood(request.user, business.neighbourhood):
        raise PermissionDenied
    form = BusinessForm(request.POST or None, instance=business)
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Business updated.")
        return redirect("business-list")
    return _editor(request, form, business.name, "Business", "delete-business", business.id)


@login_required
@require_POST
def delete_business(request, pk):
    business = get_object_or_404(Business, pk=pk)
    if not _same_neighbourhood(request.user, business.neighbourhood):
        raise PermissionDenied
    business.delete()
    messages.success(request, "Business removed.")
    return redirect("business-list")


@login_required
def edit_neighbourhood(request, pk):
    area = get_object_or_404(Neighbourhood, pk=pk)
    if area.owner_id != request.user.id:
        raise PermissionDenied
    form = NeighbourhoodForm(request.POST or None, instance=area)
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Neighbourhood updated.")
        return redirect("neighbourhood-list")
    return _editor(
        request,
        form,
        area.name,
        "Neighbourhood",
        "delete-neighbourhood",
        area.id,
        can_delete=not area.is_sample,
    )


@login_required
@require_POST
def delete_neighbourhood(request, pk):
    area = get_object_or_404(Neighbourhood, pk=pk)
    if area.owner_id != request.user.id:
        raise PermissionDenied
    if area.is_sample:
        raise PermissionDenied
    area.delete()
    messages.success(request, "Neighbourhood removed.")
    return redirect("neighbourhood-list")
