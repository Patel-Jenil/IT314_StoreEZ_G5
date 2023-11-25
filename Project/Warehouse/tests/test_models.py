from django.test import TestCase
from mainapp.models import Warehouse

class TestModel(TestCase):
    
    def setUp(self):
        self.warehouse1 = Warehouse.objects.create(
            name = "Jay Bhavani"
            address = "Vijay char Rasta, Navrangpura"
            city = "Ahmedabad"
            state = "Gujarart"
            poc_name = "Adit"
            poc_phone_no = "9876543211"
            owner = 
            image = models.ImageField(default="images/default_warehouse_image.jpg",upload_to="images/warehouse/",blank=True,null=True)
            latitude = 23.1862737352
            longitude = 72.6283225558
        )