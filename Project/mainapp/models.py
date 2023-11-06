from django.db import models
from datetime import date
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import User

    
class Warehouse_owner(models.Model):
    first_name = models.CharField(max_length=100, null=True)
    last_name = models.CharField(max_length=100, null=True)
    email = models.EmailField(max_length=200)
    phone_no = models.DecimalField(max_digits=10, decimal_places=0, null=True)
    # warehouse_id = models.ForeignKey(Warehouse, on_delete=models.CASCADE, null=True)
    
    
class Warehouse(models.Model):
    name = models.CharField(max_length=100)
    address = models.TextField()
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    poc_name = models.CharField(max_length=100)
    poc_phone_no = models.DecimalField(max_digits=10, decimal_places=0)
    owner = models.ForeignKey(Warehouse_owner, on_delete=models.CASCADE , default =0)
    def __str__(self):
        return self.name
    
class Unit(models.Model):
    type = models.CharField(max_length=100) # Check box feild
    capacity = models.IntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)  
    warehouse = models.ForeignKey(Warehouse, on_delete=models.CASCADE)
    
    
class Booking(models.Model):
    start_date = models.DateField(default= date.today)
    end_date = models.DateField(default= date.today)
    description = models.TextField()
    unit_id = models.ManyToManyField(Unit)
    
    
class Farmer(models.Model):
    first_name = models.CharField(max_length=100, null=True)
    last_name = models.CharField(max_length=100, null=True)
    # email = models.EmailField(max_length=200, null=True)
    phone_no = models.DecimalField(max_digits=10, decimal_places=0, null=True)
    city = models.CharField(max_length=100, null=True)
    state = models.CharField(max_length=100, null=True)
    booking_id = models.ForeignKey(Booking, on_delete=models.CASCADE, null=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)