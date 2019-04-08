from django.db import models


class Users(models.Model):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    email = models.CharField(max_length=50, primary_key=True)
    password = models.CharField(max_length=30)
    last_logged_in = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)
