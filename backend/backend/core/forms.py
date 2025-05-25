from django import forms
from .models import UserProfile

class ProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = [
            "phone_number",
            "hobbies",
            "interests",
            "bio",
            "resume",
        ]
        widgets = {
            "hobbies": forms.Textarea(
                attrs={"placeholder": "Введите список хобби через запятую"}
            ),
            "interests": forms.Textarea(
                attrs={"placeholder": "Введите список интересов через запятую"}
            ),
            "bio": forms.Textarea(
                attrs={"placeholder": "Напишите краткую информацию о себе"}
            ),
        }
