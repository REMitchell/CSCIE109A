import requests
import json
from category import Category
from database import Database
from playlist import Playlist
from track import Track
from artist import Artist
from collections import Counter

db = Database()

playlists = Playlist.loadAll(db)

for playlist in playlists:
    genres = []
    for track in playlist.tracks:
        genres.extend(track.artist1.genres)
    print("Playlist "+str(playlist.name)+" genres are: ")
    print(Counter(genres))