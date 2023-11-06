from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class EditProfile(models.Model):
    first_name = models.CharField(max_length=100, null=True)
    last_name = models.CharField(max_length=100, null=True)
    email = models.EmailField(max_length=200)
    phone_no = models.DecimalField(max_digits=10, decimal_places=0, null=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)
    loggedin_userid = models.IntegerField()
