from django.shortcuts import render, redirect
from .forms import ProfileForm
from .models import Competition, UserProfile, CompetitionRegistration
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, logout
from django.conf import settings
from .openai_utils import (
    process_resume_and_update_profile,
    generate_recommendations,
    select_best_teammates,
    generate_competitions_ai,
)
from django.contrib import messages


def logout_view(request):
    logout(request)
    return redirect("home")


def home_view(request):
    return render(request, "core/home.html")


def signup_view(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("profile")
    else:
        form = UserCreationForm()
    return render(request, "core/signup.html", {"form": form})


@login_required
def profile_view(request):
    profile, created = UserProfile.objects.get_or_create(user=request.user)
    if request.method == "POST":
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            profile = form.save()
            if "resume" in request.FILES:
                resume_path = profile.resume.path
                process_resume_and_update_profile(profile, resume_path)
            return redirect("profile")
    else:
        form = ProfileForm(instance=profile)
    return render(request, "core/profile.html", {"form": form})


@login_required
def recommendations_view(request):
    profile = request.user.userprofile
    competitions_data = generate_competitions_ai(
        profile.bio, profile.interests, profile.hobbies
    )

    class CompetitionObj:
        def __init__(self, data):
            self.id = data.get("id", 0)
            self.title = data.get("title", "")
            self.date = data.get("date", "")
            self.direction = data.get("direction", "")
            self.description = data.get("description", "")
            self.tags = data.get("tags", "")

    competitions = [CompetitionObj(data) for data in competitions_data]

    all_profiles = UserProfile.objects.exclude(user=request.user)
    usernames = select_best_teammates(profile, all_profiles)
    teammates = UserProfile.objects.filter(user__username__in=usernames)
    return render(
        request,
        "core/recommendations.html",
        {
            "recommendations": competitions,
            "teammates": teammates,
        },
    )


@login_required
def register_competition_view(request, competition_id):
    competition = Competition.objects.get(id=competition_id)
    CompetitionRegistration.objects.get_or_create(
        user=request.user, competition=competition
    )
    messages.success(request, f"Вы зарегистрированы на конкурс: {competition.title}")
    return redirect("recommendations")
