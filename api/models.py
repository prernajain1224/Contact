from django.db import models
from django.contrib.auth.models import User

class Content(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,related_name='api_content')
    name = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=15)
    alternate_phone_number = models.CharField(max_length=15, blank=True)
    profile_image = models.ImageField(upload_to='profile_images/', blank=True)

    def __str__(self):
        return self.name
