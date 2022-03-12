from functools import partial
from http.client import HTTP_PORT
from django.shortcuts import render
from rest_framework import status, viewsets
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.response import Response
from django.db.models import Q
from rest_framework import filters
from songs.models import Albums, Artists, Lyrics
from songs.serializers import AlbumDetailSerializer, AlbumsListSerializer, ArtistsDetailSerializer, ArtistsListSerializer, LyricsDetailSerializer, LyricsListSerializer, LyricsUpdateSerializer
from django_filters.rest_framework import DjangoFilterBackend

# Create your views here.
class ArtistsListView(viewsets.ModelViewSet):
    serializer_class = ArtistsListSerializer
    queryset = Artists.objects.all()
    pagination_class = LimitOffsetPagination
  

    def create(self, request, *args, **kwargs):
        try:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except Exception as e:
            print(e)
            return Response("Record already exists.", status=status.HTTP_409_CONFLICT)
    
    
    def list(self, request, *args, **kwargs):
        try:
            queryset = Artists.objects.all()
            
            if request.GET.get('sort_asc'):
                queryset = queryset.order_by(request.GET.get('sort_asc'))
            if request.GET.get('sort_desc'):
                queryset = queryset.order_by('-'+request.GET.get('sort_desc'))
            
            if request.GET.get('year_greater'):
                queryset = queryset.filter(first_year_active__gt = request.GET.get('year_greater'))
            if request.GET.get('year_lesser'):
                queryset = queryset.filter(first_year_active__lt = request.GET.get('year_lesser'))
                
            if request.GET.get('search'):
                keyword = request.GET['search']
                queryset = queryset.filter(name__icontains=keyword)
                
            page = self.paginate_queryset(queryset)
            serializer = ArtistsListSerializer(page,many=True)
            return self.get_paginated_response(serializer.data)
        except Exception as e:
            print(e)
            return Response("something went wrong.", status=status.HTTP_400_BAD_REQUEST)
    
                    

class ArtistsDetailView(viewsets.ModelViewSet):
    serializer_class = ArtistsListSerializer
    queryset = Artists.objects.all()
    
    def retrive(self, request, *args, **kwargs):
        try:
            instance=self.get_object()            
            serializer = ArtistsDetailSerializer(instance)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            print(e)
            return Response("Artist not found", status=status.HTTP_404_NOT_FOUND)

    def destroy(self, request, *args, **kwargs):
        try:
            instance=self.get_object()
            self.perform_destroy(instance)
            return Response("Artist removed", status=status.HTTP_204_NO_CONTENT)
        except Exception as e:
            print(e)
            return Response("Artist not found", status=status.HTTP_404_NOT_FOUND)
    
    def partial_upadte(self, request, *args, **kwargs):
        try:
            instance=self.get_object()
            serializer = ArtistsDetailSerializer(instance,partial=True)
            self.perform_update(instance)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            print(e)
            return Response("Album not found", status=status.HTTP_404_NOT_FOUND)
    

class LyricsListView(viewsets.ModelViewSet):
    serializer_class = LyricsListSerializer
    queryset = Lyrics.objects.all()
    pagination_class = LimitOffsetPagination
    
    def create(self, request, *args, **kwargs):
        try:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)
            serializer = LyricsUpdateSerializer(Lyrics.objects.get(id=serializer.data['id']),many=False)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except Exception as e:
            print(e)
            return Response("Album name arleady exists or Artist not found.", status=status.HTTP_400_BAD_REQUEST)
    
    def list(self, request, *args, **kwargs):
        try:
            queryset = Lyrics.objects.all()
                
            if request.GET.get('search'):
                keyword = request.GET['search']
                queryset = queryset.filter(Q(name__icontains=keyword) | Q(album__artist__name__icontains = keyword))
                
            page = self.paginate_queryset(queryset)
            serializer = LyricsDetailSerializer(page,many=True)
            return self.get_paginated_response(serializer.data)
        except Exception as e:
            print(e)
            return Response("something went wrong.", status=status.HTTP_400_BAD_REQUEST)
    
    def list_random_lyric(self, request):
        try:
            queryset = Lyrics.objects.all().order_by('?')[:1]
            serializer = LyricsDetailSerializer(queryset,many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            print(e)
            return Response("Album name arleady exists or Artist not found.", status=status.HTTP_400_BAD_REQUEST)
        

class LyricsDetailView(viewsets.ModelViewSet):
    serializer_class = LyricsDetailSerializer
    queryset = Lyrics.objects.all()
    pagination_class = LimitOffsetPagination
    
    def retrive(self, request, *args, **kwargs):
        try:
            instance=self.get_object()            
            serializer = LyricsDetailSerializer(instance)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            print(e)
            return Response("Lyric not found", status=status.HTTP_404_NOT_FOUND)

    def partial_update(self, request, *args, **kwargs):
        try:
            instance=self.get_object()
            serializer = LyricsUpdateSerializer(instance,partial=True)
            self.perform_update(instance)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            print(e)
            return Response("Lyric not found", status=status.HTTP_404_NOT_FOUND)
    
    def destroy(self, request, *args, **kwargs):
        try:
            instance=self.get_object()
            self.perform_destroy(instance)
            return Response("Lyric removed", status=status.HTTP_204_NO_CONTENT)
        except Exception as e:
            print(e)
            return Response("Lyric not found", status=status.HTTP_404_NOT_FOUND)
    
    def lyrics_vote(self, request, *args, **kwargs):
        try:
            instance=self.get_object()
            if 'up_vote' in request.data:
                if int(request.data['up_vote']) > 0:
                    instance.up_vote += 1
            if 'down_vote' in request.data:
                if int(request.data['down_vote']) > 0:
                    instance.down_vote += 1
            instance.save()
            serializer = LyricsDetailSerializer(instance)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            print(e)
            return Response("Lyric not found or wrong data provided", status=status.HTTP_404_NOT_FOUND)   
    

class AlbumsListView(viewsets.ModelViewSet):
    serializer_class = AlbumsListSerializer
    queryset = Albums.objects.all()
    pagination_class = LimitOffsetPagination
    
    def create(self, request, *args, **kwargs):
        try:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except Exception as e:
            print(e)
            return Response("Lyrics name arleady exists or Album not found.", status=status.HTTP_409_CONFLICT)
    
    def list(self, request, *args, **kwargs):
        try:
            queryset = Albums.objects.all()
                
            if request.GET.get('search'):
                keyword = request.GET['search']
                queryset = queryset.filter(name__icontains=keyword)
                
            page = self.paginate_queryset(queryset)
            serializer = AlbumDetailSerializer(page,many=True)
            return self.get_paginated_response(serializer.data)
        except Exception as e:
            print(e)
            return Response("something went wrong.", status=status.HTTP_400_BAD_REQUEST)

class AlbumsDetailView(viewsets.ModelViewSet):
    serializer_class = AlbumDetailSerializer
    queryset = Albums.objects.all()
    
    def retrive(self, request, *args, **kwargs):
        try:
            instance=self.get_object()            
            serializer = AlbumDetailSerializer(instance)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            print(e)
            return Response("Album not found", status=status.HTTP_404_NOT_FOUND)

    def destroy(self, request, *args, **kwargs):
        try:
            instance=self.get_object()
            self.perform_destroy(instance)
            return Response("Album removed", status=status.HTTP_204_NO_CONTENT)
        except Exception as e:
            print(e)
            return Response("Album not found", status=status.HTTP_404_NOT_FOUND)
    
    def partial_upadte(self, request, *args, **kwargs):
        try:
            instance=self.get_object()
            serializer = AlbumDetailSerializer(instance,partial=True)
            self.perform_update(instance)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            print(e)
            return Response("Album not found", status=status.HTTP_404_NOT_FOUND)
    

