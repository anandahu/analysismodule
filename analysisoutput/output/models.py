from django.db import models

# Create your models here.
from django.contrib.auth.models import User #used to import the built-in User model provided by Django’s authentication system
class UserFile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    file = models.FileField(upload_to='uploads/')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    cleaned_file = models.FileField(upload_to='cleaned/', blank=True, null=True)  # Store cleaned file
    uploaded_at = models.DateTimeField(auto_now_add=True)