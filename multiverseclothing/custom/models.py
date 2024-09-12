from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone



class Design(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    design = models.ImageField(upload_to='designs/')
    color = models.CharField(max_length=300)
    print = models.CharField(max_length=300)
    size = models.CharField(max_length=300)
    fit = models.CharField(max_length=300)
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.user.username} - {self.design.name}"

    def get_user_email(self):
        return self.user.email
