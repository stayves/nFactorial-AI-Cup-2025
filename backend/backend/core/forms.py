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
                attrs={"placeholder": "Enter the list of hobbies separated by comma"}
            ),
            "interests": forms.Textarea(
                attrs={"placeholder": "Enter the list of intersets separated by cooma"}
            ),
            "bio": forms.Textarea(
                attrs={"placeholder": "Write a brief inroduction about yourself"}
            ),
        }
