from django.shortcuts import render , redirect, get_object_or_404
from django.http import HttpResponse
from .models import *
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.utils.http import url_has_allowed_host_and_scheme

@login_required(login_url='login')
def idea_submit(request):
    if request.method == "POST":
        data = request.POST

        idea_title = data.get("idea_title")
        idea_description = data.get("idea_description")

        Idea.objects.create(
            user = request.user,
            idea_title = idea_title,
            idea_description = idea_description
        )

        return redirect("home")

    return render(request, "home/ideas.html")

def home(request):
    queryset = Idea.objects.all()

    if request.GET.get("search"):
        queryset = queryset.filter(idea_title__icontains = request.GET.get("search"))

    context = {
        "ideas": queryset
    }

    return render(request, "home/home.html", context)

def view_idea(request, id):
    idea = get_object_or_404(Idea, id=id)
    context = {
        "idea": idea
    }

    return render(request, "home/view_idea.html", context)

def login_page(request):
    next_url = request.POST.get("next") or request.GET.get("next")

    if request.user.is_authenticated:
        if next_url and url_has_allowed_host_and_scheme(next_url, allowed_hosts={request.get_host()}):
            return redirect(next_url)
        return redirect("home")

    if request.method == "POST":
        data = request.POST
        username = data.get("username")
        password = data.get("password")

        if not username or not password:
            messages.error(request, "Please enter both username and password.")
            return render(request, "home/login.html", {"next": next_url})

        user = authenticate(username=username, password=password)
        if user is None:
            messages.error(request, "Invalid username or password!")
            return render(request, "home/login.html", {"next": next_url})
        else:
            login(request, user)
            if next_url and url_has_allowed_host_and_scheme(next_url, allowed_hosts={request.get_host()}):
                return redirect(next_url)
            return redirect("home")

    if next_url == "/submit-idea/":
        messages.error(request, "You need to be logged in to submit an idea.")

    return render(request, "home/login.html", {"next": next_url})

def register_page(request):
    if request.method == "POST":
        data = request.POST

        username = data.get("username")
        password = data.get("password")
        confirm_password = data.get("confirm_password")

        if password != confirm_password:
            messages.error(request, "Passwords do not match!")
            return redirect("register")

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already taken!")
            return redirect("register")

        User.objects.create_user(username=username, password=password)

        messages.success(request, "Account created successfully! Please login.")
        return redirect("register")
    return render(request, "home/register.html")

@login_required(login_url='login')
def logout_page(request):
    if request.method == "POST":
        logout(request)
        messages.success(request, "You have been logged out successfully.")
        return redirect("login")

    return redirect("login")