from django.db import models
from datetime import date
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import User
from django.conf import settings

    
class Warehouse_owner(models.Model):
    first_name = models.CharField(max_length=100, null=True)
    last_name = models.CharField(max_length=100, null=True)
    email = models.EmailField(max_length=200)
    phone_no = models.DecimalField(max_digits=10, decimal_places=0, null=True)
    image = models.ImageField(default="images/default_user_image.jpg",upload_to="images/warehouse_owner/",blank=True,null=True)
    def __str__(self):
        return f'{self.first_name} {self.last_name}'
    
    
class Warehouse(models.Model):
    name = models.CharField(max_length=100)
    address = models.TextField()
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    poc_name = models.CharField(max_length=100, null=True)
    poc_phone_no = models.DecimalField(max_digits=10, decimal_places=0)
    owner = models.ForeignKey(Warehouse_owner, on_delete=models.CASCADE)
    image = models.ImageField(default="images/default_warehouse_image.jpg",upload_to="images/warehouse/",blank=True,null=True)
    latitude = models.FloatField(default=23.1862737352)
    longitude = models.FloatField(default = 72.6283225558)
    def __str__(self):
        return f'{self.name}'
    
class Unit(models.Model):
    id = models.BigAutoField(primary_key=True)
    type = models.CharField(max_length=100) # Check box field
    capacity = models.IntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)  
    warehouse = models.ForeignKey(Warehouse, on_delete=models.CASCADE)
    def __str__(self):
        return f'{self.id} {self.type} {self.capacity}'
    
    
class Farmer(models.Model):
    first_name = models.CharField(max_length=100, null=True)
    last_name = models.CharField(max_length=100, null=True)
    email = models.EmailField(max_length=200, null=True)
    phone_no = models.DecimalField(max_digits=10, decimal_places=0, null=True)
    city = models.CharField(max_length=100, null=True)
    state = models.CharField(max_length=100, null=True)
    image = models.ImageField(default="images/default_user_image.jpg",upload_to="images/farmer/",blank=True,null=True)
    def __str__(self) -> str:
        return f'{self.first_name} {self.last_name}'
    
    @property
    def imageURL(self):
        try:
            url = self.image.url
        except:
            url = settings.STATIC_URL + 'profile-img.avif'
        return url
    
    
class Booking(models.Model):
    id = models.BigAutoField(primary_key=True)
    start_date = models.DateField(default= date.today)
    end_date = models.DateField(default= date.today)
    description = models.TextField()
    unit = models.ManyToManyField(Unit)
    farmer = models.ForeignKey(Farmer,on_delete=models.CASCADE, null=True)
    date = models.DateTimeField(auto_now_add=True)
    def __str__(self) -> str:
        return f"{self.id} {self.start_date}-{self.end_date}"