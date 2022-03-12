from django.test import TestCase
from rest_framework.test import APITestCase

from songs.models import Artists
# Create your tests here.
class  TestArtist(APITestCase):
    url = "/artists/"
    
    def setUp(self):
        Artists.objects.create(name='Bonny M', first_year_active =1960)
        Artists.objects.create(name='Jim Morission', first_year_active =1970)
        Artists.objects.create(name='Mohammed Rafi', first_year_active =1950)
        Artists.objects.create(name='Ed Sheeran', first_year_active =2009)
        Artists.objects.create(name='Tylor Swift', first_year_active =2004)
        Artists.objects.create(name='Lata Mangeshkar', first_year_active =1965)
        Artists.objects.create(name='Ariana Grande', first_year_active =2016)
        
       
    
    def test_get_artist(self):
        
        response = self.client.get(self.url)
        result = response.json()
        self.assertEquals(response.status_code,200)
        self.assertIsInstance(result,dict)
        self.assertEqual(result['results'][0]['name'],'Bonny M')
        self.assertEqual(result['results'][0]['first_year_active'],1960)
        self.assertEqual(result['results'][0]['first_year_active'],1960)
        
        # ordering by name ascending
        response = self.client.get(self.url+"?sort_asc=name")
        result = response.json()
        self.assertEquals(response.status_code,200)
        self.assertIsInstance(result,dict)
        self.assertEqual(result['results'][1]['name'],'Bonny M')
        
        # ordering by name descending
        response = self.client.get(self.url+"?sort_desc=name")
        result = response.json()
        self.assertEquals(response.status_code,200)
        self.assertIsInstance(result,dict)
        self.assertEqual(result['results'][0]['name'],'Tylor Swift')
        
        # ordering by first_year_active ascending
        response = self.client.get(self.url+"?sort_asc=first_year_active")
        result = response.json()
        self.assertEquals(response.status_code,200)
        self.assertIsInstance(result,dict)
        self.assertEqual(result['results'][1]['name'],'Bonny M')
        
        # ordering by first_year_active descending
        response = self.client.get(self.url+"?sort_desc=first_year_active")
        result = response.json()
        self.assertEquals(response.status_code,200)
        self.assertIsInstance(result,dict)
        self.assertEqual(result['results'][1]['name'],'Ed Sheeran')
        
    
    # def test_post_artist(self):
    #     # defination
    #     pass