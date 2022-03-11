
from rest_framework import serializers

from songs.models import Albums, Artists, Lyrics


""" **************** This Class allows you to specify the serializers for Artists List Field Type ****************  """

class ArtistsListSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Artists
        exclude = ('create_date',)
        
""" **************** This Class allows you to specify the serializers for Artists Details Field Type ****************  """

class ArtistsDetailSerializer(serializers.ModelSerializer):
    album =serializers.SerializerMethodField()
    
    def get_album(self, obj):
        albums = Albums.objects.filter(artist=obj.pk)       
        return AlbumSerializer(albums, many=True).data
    
    class Meta:
        model = Artists
        exclude = ('create_date',)

""" **************** This Class allows you to specify the serializers for Album Field Type ****************  """

class AlbumSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Albums
        exclude = ('artist','create_date')

""" **************** This Class allows you to specify the serializers for Album List Field Type ****************  """
        
class AlbumsListSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Albums
        fields = '__all__'

""" **************** This Class allows you to specify the serializers for Album Detail Field Type ****************  """

class AlbumDetailSerializer(serializers.ModelSerializer):
    artist = ArtistsListSerializer(read_only=True, many=False)
    
    class Meta:
        model = Albums
        fields = '__all__'

""" **************** This Class allows you to specify the serializers for Lyric List Field Type ****************  """

class LyricsListSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Lyrics
        fields = '__all__'

""" **************** This Class allows you to specify the serializers for Lyrics Detail Field Type ****************  """

class LyricsDetailSerializer(serializers.ModelSerializer):
    album = AlbumDetailSerializer(read_only=True, many=False)
 
    class Meta:
        model = Lyrics
        fields = '__all__'


""" **************** This Class allows you to specify the serializers for Lyrics Update Field Type ****************  """

class LyricsUpdateSerializer(serializers.ModelSerializer):
    album = AlbumDetailSerializer(read_only=True, many=False)
 
    class Meta:
        model = Lyrics
        exclude = ('up_vote','down_vote',)
