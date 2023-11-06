from django.db import models

# Create your models here.
class Contact(models.Model):
    # msg_id =models.AutoField(primary_key=True)
     first_name = models.CharField(max_length=100, null=True)
     last_name = models.CharField(max_length=100, null=True)
     email = models.EmailField(max_length=200, null=True)
     phone_no = models.DecimalField(max_digits=10, decimal_places=0, null=True)
     city = models.CharField(max_length=100, null=True)
     state = models.CharField(max_length=100, null=True)