from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path("", views.home_view, name="home"),
    path("accounts/profile/", views.profile_view, name="profile"),
    path("recommendations/", views.recommendations_view, name="recommendations"),
    path(
        "accounts/login/",
        auth_views.LoginView.as_view(template_name="core/login.html"),
        name="login",
    ),
    path("accounts/logout/", views.logout_view, name="logout"),
    path("accounts/signup/", views.signup_view, name="signup"),
    path(
        "competition/<int:competition_id>/register/",
        views.register_competition_view,
        name="register_competition",
    ),
]
