from django.test import TestCase
from rest_framework.test import APITestCase

from songs.models import Albums, Artists, Lyrics
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
        ariana=Artists.objects.create(name='Ariana Grande', first_year_active =2016)
        Albums.objects.create(name='Youth', year =2021, artist =ariana)
    
        
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
        
         # ordering by first_year_active descending
        response = self.client.get(self.url+"?search=rafi")
        result = response.json()
        self.assertEquals(response.status_code,200)
        self.assertIsInstance(result,dict)
        self.assertEqual(result['results'][0]['name'],'Mohammed Rafi')
    
    
    def test_get_artist_detail(self):
        pk= Artists.objects.get(name='Ariana Grande')
        response =self.client.get(self.url+f'{pk.id}')
        result = response.json()
        # assert
        self.assertEqual(response.status_code,200)
        self.assertIsInstance(result,dict)
        self.assertEqual(result['album'][0]['name'],'Youth')
    
    
    def test_post_artist(self):
        # defination
        data={
                    "name": "Kid Laroi",
                    "first_year_active": 2021
                }
        
        # process
        response =self.client.post(self.url,data=data)
        result = response.json()
        
        # assert
        self.assertEqual(response.status_code,201)
        self.assertEqual(result['name'],'Kid Laroi')
        
        
    def test_update_artist(self):
        pk= Artists.objects.get(name='Bonny M').id
        data={
                "name": "Hanuma",
            }
        response =self.client.patch(self.url+f'{pk}',data=data)
        result = response.json()
        
        # assert
        self.assertEqual(response.status_code,200)
        self.assertEqual(result['name'],'Hanuma')
    
    
    def test_delete_artist(self):
        pk=Artists.objects.create(name='Tommy', first_year_active =2018)
        response =self.client.delete(self.url+f'{pk.id}')
        # assert
        self.assertEqual(response.status_code,204)


class  TestAlbums(APITestCase):
    url = "/albums/"
    
    def setUp(self):
        jim=Artists.objects.create(name='Jim Morission', first_year_active =1970)
        tylor=Artists.objects.create(name='Tylor Swift', first_year_active =2004)
        ed=Artists.objects.create(name='Ed Sheeran', first_year_active =2009)
        
        Albums.objects.create(name='Dance', year =1970, artist =jim)
        Albums.objects.create(name='Up', year =2009, artist =ed)
        Albums.objects.create(name='Fearless', year =2017, artist =tylor)
        
        
    def test_get_albums(self):
        
        response = self.client.get(self.url)
        result = response.json()
        self.assertEquals(response.status_code,200)
        self.assertIsInstance(result,dict)
        
        self.assertEqual(result['results'][0]['name'],'Dance')
        self.assertEqual(result['results'][1]['artist']['first_year_active'],2009)
        self.assertEqual(result['results'][2]['artist']['name'],'Tylor Swift')
        
        
    def test_get_albums_detail(self):
        pk= Albums.objects.get(name='Dance')
        response =self.client.get(self.url+f'{pk.id}')
        result = response.json()
        # assert
        self.assertEqual(response.status_code,200)
        self.assertIsInstance(result,dict)
        self.assertEqual(result['artist']['name'],'Jim Morission')
        
        
    def test_delete_albums(self):
        pk=Albums.objects.get(name='Fearless')
        response =self.client.delete(self.url+f'{pk.id}')
        # assert
        self.assertEqual(response.status_code,204)
    
    
    def test_post_albums(self):
        # defination
        pk = Artists.objects.get(name='Ed Sheeran')
        data={   
                "name": "Dance",
                "year": 2015,
                "artist": pk.id
            }
        
        # process
        response =self.client.post(self.url,data=data)
        result = response.json()
        
        # assert
        self.assertEqual(response.status_code,201)
        self.assertIsInstance(result,dict)
        self.assertEqual(result['name'],'Dance')
        self.assertEqual(result['artist'],str(pk.id))
    
    
    def test_update_albums(self):
        pk = Albums.objects.get(name='Dance').id
        data={
                "name": "Hanuma",
                "year": 2014
            }
        
        response =self.client.patch(self.url+f'{str(pk)}',data=data)
        result = response.json()
        # assert
        self.assertEqual(response.status_code,200)
        self.assertIsInstance(result,dict)
        self.assertEqual(result['name'],'Hanuma')
    
class  TestLyrics(APITestCase):
    url = "/lyrics/"
    
    
    def setUp(self):
        jim = Artists.objects.create(name='Jim Morission', first_year_active =1970)
        tylor = Artists.objects.create(name='Tylor Swift', first_year_active =2004)
        ed = Artists.objects.create(name='Ed Sheeran', first_year_active =2009)
        
        dance = Albums.objects.create(name='Dance', year =1970, artist =jim)
        up = Albums.objects.create(name='Up', year =2009, artist =ed)
        fearless = Albums.objects.create(name='Fearless', year =2017, artist =tylor)
        
        Lyrics.objects.create(name='Night', text="Looking up the night ....", album =dance)
        Lyrics.objects.create(name='Day', text="Looking up the day..", album =up)
        Lyrics.objects.create(name='Dawn', text="Looking up the Dawn", album =fearless)
    
    
    def test_get_lyrics(self):
        response = self.client.get(self.url)
        result = response.json()
        self.assertEquals(response.status_code,200)
        self.assertIsInstance(result,dict)
        self.assertEqual(result['results'][0]['album']['artist']['name'],'Jim Morission')
        self.assertEqual(result['results'][1]['album']['artist']['first_year_active'],2009)
        self.assertEqual(result['results'][1]['album']['name'],'Up')
        self.assertEqual(result['results'][2]['up_vote'],0)
        
        
    def test_get_lyrics_detail(self):
        pk= Lyrics.objects.get(name='Dawn')
        response =self.client.get(self.url+f'{pk.id}')
        result = response.json()
        # assert
        self.assertEqual(response.status_code,200)
        self.assertIsInstance(result,dict)
        self.assertEqual(result['album']['artist']['name'],'Tylor Swift')
        
        
    def test_delete_lyrics(self):
        pk= Lyrics.objects.get(name='Dawn')
        response =self.client.delete(self.url+f'{pk.id}')
        # assert
        self.assertEqual(response.status_code,204)
    
    
    def test_post_lyrics(self):
        # defination
        pk = Albums.objects.get(name='Fearless')
        data={   
                "name": "Dance",
                "text":"Yo Yo",
                "album": str(pk.id)
            }
        # process
        response =self.client.post(self.url,data=data)
        result = response.json()
        
        # assert
        self.assertEqual(response.status_code,201)
        self.assertIsInstance(result,dict)
        self.assertEqual(result['album']['artist']['name'],'Tylor Swift')
        self.assertEqual(result['name'],'Dance')
    
    
    def test_update_lyrics(self):
        pk = Lyrics.objects.get(name='Dawn').id
        data={
                "name": "Hanuma",
                "text": '2014'
            }
        response =self.client.patch(self.url+f'{str(pk)}',data=data)
        result = response.json()
        # assert
        self.assertEqual(response.status_code,200)
        self.assertIsInstance(result,dict)
        self.assertEqual(result['name'],'Hanuma')
        
    def test_vote_lyrics(self):
        pk = Lyrics.objects.get(name='Dawn').id
        data={
            "up_vote":1 
                }
        response =self.client.patch(f'/lyrics_vote/{str(pk)}',data=data)
        result = response.json()
        # assert
        self.assertEqual(response.status_code,200)
        self.assertIsInstance(result,dict)
        self.assertEqual(result['up_vote'],1)
    