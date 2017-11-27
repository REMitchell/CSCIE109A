import requests
import json
from category import Category
from database import Database
from playlist import Playlist
from track import Track
from artist import Artist
# 7240a6140225470db92cfb998b11213b
# 5ab4418cd35443639f96eba74b01c445
# curl -X "POST" -H "Authorization: Basic 5ab4418cd35443639f96eba74b01c445" -d grant_type=client_credentials https://accounts.spotify.com/api/token
db = Database()
token = "BQAYiTOGyhL9XvkPJyfQu-RID4D5ZuhoQYdTehvwez3BADiIxsPscvUrYlGGtMN9r4sqQ2qgzD0tyJ4R-J5JoCHEG3kqUgpU_W_HLMpGwcPMSSwRv9KVhwT7Bkebt5sDzMRFWghWDa8H"
headers = {'Authorization': "Bearer "+token}
def getCategories():
    endpoint = "https://api.spotify.com/v1/browse/categories?offset=20&limit=20"
    categories = requests.get(endpoint, headers=headers).json()

    for category in categories['categories']['items']:
        print("\nCATEGORY")
        print(category)
        categoryObj = Category(None, category['name'], category['id'])
        categoryObj.save(db)

def getFollowers(playlistId):
    endpoint = "https://api.spotify.com/v1/users/spotify/playlists/"+playlistId+"/followers"
    data = requests.get(endpoint, headers=headers)
    print(data)

def getPlaylistsByUser():
    endpoint = 	"/v1/users/{user_id}/playlists"

def saveTracks(tracks, playlistObj):
    for track in tracks['items']:
        #spotifyId, artist1, artist2, artist3, name, 
        #duration, explicit, 
        #popularity):
        spotifyId = track['track']['id']
        name = track['track']['name']
        duration = track['track']['duration_ms']
        explicit = track['track']['explicit']
        popularity = track['track']['popularity']
        artists = track['track']['artists']
        if len(artists) > 3:
            print("TOO MANY ARTISTS! "+str(name))
        artist1 = artists[0]['id']
        artist2 = None
        artist3 = None
        if len(artists) > 1:
            artist2 = artists[1]['id']
        if len(artists) > 2:
            artist3 = artists[2]['id']
        album = track['track']['album']['id']
        trackObj = Track(spotifyId, album, artist1, artist2, artist3, name, duration, explicit, popularity)
        trackObj = trackObj.save(db)
        trackObj.linkToPlaylist(db, playlistObj)


def getPlaylistDetails(url, playlistObj):
    if playlistObj.playlistExists(db):
        print("Playlist already exists")
        return
    playlist = requests.get(url, headers=headers).json()
    playlistObj.description = playlist['description'].encode('utf-8') if playlist['description'] else None
    playlistObj.followers = playlist['followers']['total']
    playlistObj = playlistObj.save(db)
    saveTracks(playlist['tracks'], playlistObj)

def findArtist(spotifyId):
    endpoint = "https://api.spotify.com/v1/artists?ids="+spotifyId
    print(endpoint)
    artists = requests.get(endpoint, headers=headers).json()

    for artist in artists['artists']:
        followers = artist['followers']['total']
        genres = ','.join(artist['genres'])
        name = artist['name']
        popularity = artist['popularity']
        artistObj = Artist(artist['id'], name, genres, followers, popularity)
        artistObj = artistObj.save(db)

def makeGenres():
    db.cur.execute("TRUNCATE TABLE genres")
    db.conn.commit()
    db.cur.execute("TRUNCATE TABLE artistGenres")
    db.conn.commit()
    db.cur.execute("SELECT * FROM artists")
    artists = db.cur.fetchall()
    genres = set()
    for artist in artists:
        if artist['genres']:
            genres.update(artist['genres'].split(','))
    genreDict = {}
    for genre in genres:
        db.cur.execute("INSERT INTO genres (name) VALUES (%s)", (genre))
        db.conn.commit()
        genreDict[genre] = db.cur.lastrowid
    
    for artist in artists:
        artistGenres = artist['genres'].split(',')
        for artistGenre in artistGenres:
            print("INSERT INTO artistGenres (artistId, genreId) VALUES ({}, {})".format(artist['id'], genreDict[artistGenre]))
            db.cur.execute("INSERT INTO artistGenres (artistId, genreId) VALUES (%s, %s)", (artist['id'], genreDict[artistGenre]))
            db.conn.commit()

def populateArtists(offset):
    artistNum = 'artist3'
    db.cur.execute("SELECT * FROM tracks WHERE "+artistNum+" IS NOT NULL AND id > %s LIMIT 10", (offset))
    rows = db.cur.fetchall()
    if len(rows) == 0:
        return
    missingArtistIds = []
    for row in rows:
        trackObj = Track.fromDBRow(row)
        db.cur.execute("SELECT * FROM artists WHERE spotifyId = %s", (trackObj.artist3))
        if db.cur.rowcount == 0:
            # Get artist
            missingArtistIds.append(trackObj.artist3)
    if len(missingArtistIds) > 0:
        findArtist(','.join(missingArtistIds))
    populateArtists(row['id'])

def getPlaylists(url):
    playlists = requests.get(url, headers=headers).json()
    for playlist in playlists['items']:
        description = None
        spotifyId = playlist['id']
        name = playlist['name']

        if 'tracks' in playlist:
            trackCount = playlist['tracks']['total']

        playlistObj = Playlist(spotifyId, name, None, trackCount, None)
        getPlaylistDetails(playlist['href'], playlistObj)
    if playlists['next']:
        print("Fetching next batch")
        print(playlists['next'])
        getPlaylists(playlists['next'])

def getTracks():
    endpoint = "https://api.spotify.com/v1/users/spotify/playlists/37i9dQZF1DWSUFOo47GEsI/tracks"
    tracks = requests.get(endpoint, headers=headers).json()
    for track in tracks['items']:
        print('\n')
        print(track)
#https://api.spotify.com/v1/users/spotify/playlists?offset=200&limit=20
#populateArtists(0)
#playlistsUrl = "https://api.spotify.com/v1/users/spotify/playlists?offset=200&limit=20"
#getPlaylists(playlistsUrl)
#getFollowers("37i9dQZF1DWX3387IZmjNa")
#getTracks()
# 	/v1/users/{user_id}/playlists

makeGenres()