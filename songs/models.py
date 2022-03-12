import datetime
import uuid
from django.utils import timezone
from django.db import models

# Create your models here.
'''This model is used to store the Artists Details''' 

class Artists(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.TextField(max_length=80,blank=False, null=False,unique=True)
    first_year_active = models.IntegerField(null=True)
    create_date = models.DateTimeField(default=timezone.now)
    
    class Meta:
        db_table = 'artists'
        

'''This model is used to store the Album Details''' 

class Albums(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    artist = models.ForeignKey(Artists,on_delete=models.CASCADE)
    year = models.IntegerField(null=True)
    name = models.TextField(max_length=80,blank=False, null=False)
    create_date = models.DateTimeField(default=timezone.now)
    
    class Meta:
        db_table = 'albums'
        unique_together = ('artist', 'year', 'name')
        
'''This model is used to store the Lyrics Details''' 

class Lyrics(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    album = models.ForeignKey(Albums,on_delete=models.CASCADE)
    up_vote = models.IntegerField(default=0)
    down_vote = models.IntegerField(default=0)
    text = models.TextField(blank=False, null=False)
    name= models.TextField(max_length=80,blank=False, null=False)
    create_date = models.DateTimeField(default=timezone.now)
    
    class Meta:
        db_table = 'lyrics'
        unique_together = ('name', 'text')
        
