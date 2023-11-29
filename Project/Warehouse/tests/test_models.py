from django.test import TestCase
from mainapp.models import Warehouse

class TestModel(TestCase):
    
    def setUp(self):
        self.warehouse1 = Warehouse.objects.create(
            name = "Jay Bhavani",
            address = "Vijay char Rasta, Navrangpura",
            city = "Ahmedabad",
            state = "Gujarart",
            poc_name = "Adit",
            poc_phone_no = "9876543211",
            owner = self.owner,
        )