from django.db import models
from datetime import date
from django.contrib.auth.models import AbstractUser

class Unit(models.Model):
    type = models.CharField(max_length=100) # Check box feild
    capacity = models.IntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)  
    
    def __str__(self):
        return self.title


class Booking(models.Model):
    start_date = models.DateField(default= date.today)
    end_date = models.DateField(default= date.today)
    description = models.TextField()
    unit_id = models.ManyToManyField(Unit)
    
    def __str__(self):
        return self.title


class Farmer(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(max_length=200)
    phone_no = models.DecimalField(max_digits=10, decimal_places=0)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    booking_id = models.ForeignKey(Booking, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.title
    
    
class Warehouse(models.Model):
    name = models.CharField(max_length=100)
    address = models.TextField()
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    poc_name = models.CharField(max_length=100)
    poc_phone_no = models.DecimalField(max_digits=10, decimal_places=0)
    unit_id = models.ForeignKey(Unit, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.title

    
class Warehouse_owner(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(max_length=200)
    phone_no = models.DecimalField(max_digits=10, decimal_places=0)
    warehouse_id = models.ForeignKey(Warehouse, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.title
    

    