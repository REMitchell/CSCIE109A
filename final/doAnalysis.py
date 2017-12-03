import requests
import json
from category import Category
from database import Database
from playlist import Playlist
from track import Track
from artist import Artist
from genre import Genre

from collections import Counter
import matplotlib
import matplotlib.pyplot as plt
import numpy as np

db = Database()

genresByPopularity = list(Genre.getByPopularity(db))

playlists = Playlist.loadAll(db)
'''playlistFollowers = []
for playlist in playlists:
    artistFollowers = []
    for track in playlist.tracks:
        if track.artist1:
            artistFollowers.append(track.artist1.followers)
        if track.artist2:
            artistFollowers.append(track.artist2.followers)
        if track.artist3:
            artistFollowers.append(track.artist3.followers)
    playlistFollowers.append(np.mean(artistFollowers))
plt.plot([playlist.followers for playlist in playlists], playlistFollowers)
'''
for playlist in playlists:
    genres = []
    for track in playlist.tracks:
        if track.artist1:
            genres.extend(track.artist1.genres)
        if track.artist2:
            genres.extend(track.artist2.genres)
        if track.artist3:
            genres.extend(track.artist3.genres)
    print("Playlist "+str(playlist.name)+" genres are: ")
    genres = Counter(genres)
    # Empty string is getting in here. need to figure that out
    del genres['']          
    print(genres.most_common(1))
    common_count = genres.most_common(1)
    if len(common_count) > 0:
        common_count = [0][1]
        commonest_genres = []
        for key, value in dict(genres).items():
            if value == common_count:
                commonest_genres.append(key)
        if len(commonest_genres) == 1:
            playlist.bestGenre = str(commonest_genres[0])
        else:
            indexes_by_popularity = [genresByPopularity.index(x) for x in commonest_genres]
            playlist.bestGenre = commonest_genres[np.argmin(indexes_by_popularity)]


    print(playlist.bestGenre)

genrePopularities = {}
for playlist in playlists:
    if playlist.bestGenre not in genrePopularities:
        genrePopularities[playlist.bestGenre] = []
    genrePopularities[playlist.bestGenre].append(playlist.followers)
print("GENRE POPULARITIES")
print(genrePopularities)
'''genres = []
followers = []
for key, value in genrePopularities.items():
    genres.append(key)
    followers.append(np.mean(value))
print(genres)
print(followers)
plt.bar(list(range(len(genres))), followers, align='center')
plt.xticks(list(range(len(genres))), genres, rotation='vertical')
plt.show()'''


