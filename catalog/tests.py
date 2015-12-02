from django.test import TestCase, Client
import httplib
from django.core import urlresolvers
from catalog.models import Product, Category


class NewUserTestCase(TestCase):
    fixtures = ['my_data.json']

    def setUp(self):
        self.client = Client()

    def test_new_homepage(self):
        home_url = urlresolvers.reverse('catalog_home')
        response = self.client.get(home_url)
        print(response)
        # self.failUnless(response)
        self.assertEqual(response.status_code, httplib.OK)

    def test_view_category(self):
        category = Category.active.first()
        category_url = category.get_absolute_url()
        response = self.client.get(category_url)
        # self.failUnless(response)
        self.assertEqual(response.status_code, httplib.OK)
