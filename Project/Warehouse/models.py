from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class EditProfile(models.Model):
    first_name = models.CharField(max_length=100, null=True)
    last_name = models.CharField(max_length=100, null=True)
    email = models.EmailField(max_length=200)
    phone_no = models.DecimalField(max_digits=10, decimal_places=0, null=True)
    image = models.ImageField(default="images/default_user_image.jpg",upload_to="images/warehouse_owner/",blank=True,null=True)
    def __str__(self):
        return f'{self.first_name} {self.last_name}'
