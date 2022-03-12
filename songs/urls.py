
from django.urls import path

from songs.views import AlbumsDetailView, AlbumsListView, ArtistsDetailView, ArtistsListView, LyricsDetailView, LyricsListView


artists_list = ArtistsListView.as_view({
    'get':'list',
    'post':'create',
})

artists_detail = ArtistsDetailView.as_view({
    'get':'retrive',
    'patch':'partial_update',
    'delete':'destroy'
})

lyrics_list = LyricsListView.as_view({
    'get':'list',
    'post':'create',
})

lyrics_detail = LyricsDetailView.as_view({
    'get':'retrive',
    'patch':'partial_update',
    'delete':'destroy'
})

lyrics_vote=LyricsDetailView.as_view({
    'patch':'lyrics_vote'
})

album_list = AlbumsListView.as_view({
    'get':'list',
    'post':'create',
})

album_detail = AlbumsDetailView.as_view({
    'get':'retrive',
    'patch':'partial_update',
    'delete':'destroy'
})

random_lyric = LyricsListView.as_view({
    'get':'list_random_lyric',
})

urlpatterns = [
    path('artists/', artists_list, name="Artist List"),
    path('artists/<uuid:pk>', artists_detail, name="Artist Detail"),
    path('albums/', album_list, name="Album List"),
    path('albums/<uuid:pk>', album_detail, name="Album Detail"),
    path('lyrics/', lyrics_list, name="Lyric List"),
    path('lyrics/<uuid:pk>', lyrics_detail, name="Lyric Detail"),
    path('lyrics_vote/<uuid:pk>', lyrics_vote, name="Lyrics Vote"),
    path('random_lyric/', random_lyric, name="Random Lyric"),
]
