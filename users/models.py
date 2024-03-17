from django.db import models


class User(models.Model):
    name = models.CharField(max_length=255, null=False)
    email = models.EmailField(max_length=255, null=False, unique=True)
    password = models.CharField(max_length=50, null=False)
    phone_number = models.CharField(max_length=10, unique=True)
    is_active = models.BooleanField(default=False)

    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class UserProfile(models.Model):
    DEFAULT_PROFILE_PIC_URL = "https://mywebsite.com/placeholder.png"

    profile_pic_url = models.URLField(default=DEFAULT_PROFILE_PIC_URL)
    bio = models.TextField(max_length=255, blank=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=False, related_name="profile")

    def __str__(self):
        return self.user.name
