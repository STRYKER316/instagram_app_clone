from django.db import models
from django.contrib.auth.models import User


class TimeStamp(models.Model):

    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class UserProfile(TimeStamp):

    DEFAULT_PROFILE_PIC_URL = "https://mywebsite.com/placeholder.png"
    profile_pic_url = models.ImageField(upload_to='profile_pictures/', blank=True)

    # ToDo: Add verification for size and type of profile pic being uploaded

    # ToDo: Modify the naming of the file being saved so that the update view becomes Idempotent or Compliant with PUT request

    bio = models.TextField(max_length=255, blank=True)
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        null=False,
        related_name="profile"
    )

    is_verified = models.BooleanField(default=False)

    def __str__(self):
        return self.user.name


class NetworkEdge(TimeStamp):

    from_user = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name="following")

    to_user = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name="followers")