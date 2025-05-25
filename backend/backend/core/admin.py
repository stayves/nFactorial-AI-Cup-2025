from django.contrib import admin
from .models import UserProfile, Competition, CompetitionRegistration

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ("user", "phone_number", "hobbies", "interests")
    search_fields = ("user__username", "phone_number", "hobbies", "interests")

@admin.register(Competition)
class CompetitionAdmin(admin.ModelAdmin):
    list_display = ("title", "date", "direction")
    search_fields = ("title", "direction")
    list_filter = ("direction",)

@admin.register(CompetitionRegistration)
class CompetitionRegistrationAdmin(admin.ModelAdmin):
    list_display = ("user", "competition", "registered_at")
    search_fields = ("user__username", "competition__title")
    list_filter = ("competition",)
