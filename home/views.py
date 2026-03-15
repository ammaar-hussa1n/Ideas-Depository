from django.shortcuts import render , redirect
from django.http import HttpResponse
from .models import *

def idea_submit(request):
    if request.method == "POST":
        data = request.POST

        idea_title = data.get("idea_title")
        idea_description = data.get("idea_description")

        Idea.objects.create(
            idea_title = idea_title,
            idea_description = idea_description
        )

        return redirect("home")

    return render(request, "home/ideas.html")

def home(request):
    queryset = Idea.objects.all()

    context = {
        "ideas": queryset
    }

    return render(request, "home/home.html", context)