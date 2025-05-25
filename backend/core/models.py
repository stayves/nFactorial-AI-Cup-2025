from django.db import models
from django.contrib.auth.models import User


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    hobbies = models.TextField(blank=True)
    interests = models.TextField(blank=True)
    bio = models.TextField(blank=True)
    resume = models.FileField(upload_to="resumes/", blank=True, null=True)

    def __str__(self):
        return self.user.username


class Competition(models.Model):
    title = models.CharField(max_length=255)
    date = models.DateField()
    direction = models.CharField(max_length=50)
    description = models.TextField()
    tags = models.TextField(blank=True)

    def __str__(self):
        return self.title


class CompetitionRegistration(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    competition = models.ForeignKey(Competition, on_delete=models.CASCADE)
    registered_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'competition')