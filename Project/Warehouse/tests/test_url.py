from django.test import SimpleTestCase
from django.urls import reverse, resolve
from Warehouse.views import warehouses

class TestUrls(SimpleTestCase):
    
    def test_list_url_is_resolved(self):
        url = reverse('warehouses')
        self.assertEquals(resolve(url).func, warehouses)