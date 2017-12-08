import requests
import json
from category import Category
from database import Database
from playlist import Playlist
from track import Track
from artist import Artist
import time
# 7240a6140225470db92cfb998b11213b
# 5ab4418cd35443639f96eba74b01c445
# curl -X "POST" -H "Authorization: Basic 5ab4418cd35443639f96eba74b01c445" -d grant_type=client_credentials https://accounts.spotify.com/api/token
db = Database()
token = "BQCLM-UsCh-VZ7MCegXu6mwsrYKDT0wM9wQtSa0Zva8BTm8IM3up8QBoFhllJWbS0-jNB8SkBeLJGfKsmayAEfWE8PC83vIAxbGmOoRMwFTc8xUDTsYRj1UqFDF3gmroETHG5wWBrGeH8Mk"
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
        if not track['track'] or not track['track']['id']:
            print("NO SPOTIFY ID FOR TRACK:")
            print(track)
        else:
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
    if 'followers' not in playlist:
        print("NO FOLLOWERS!?")
        return
    if 'description' in playlist:
        playlistObj.description = playlist['description'].encode('utf-8') if playlist['description'] else None
    else:
        playlistObj.description = None
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

def populateArtists():
    db.cur.execute("SELECT * FROM tracks LEFT JOIN artists ON tracks.artist3 = artists.spotifyId WHERE artists.spotifyId IS NULL GROUP BY tracks.artist3 LIMIT 15;")
    #db.cur.execute("SELECT * FROM (SELECT * FROM tracks GROUP BY tracks.artist1) as track LEFT JOIN artists ON track.artist1 = artists.spotifyId WHERE artists.spotifyId IS NULL LIMIT 15;")
    rows = db.cur.fetchall()
    if len(rows) == 0:
        return

    missingArtistIds = []
    for row in rows:
        if row['artist3'] is not None:
            missingArtistIds.append(row['artist3'])
    if len(missingArtistIds) > 1:
        findArtist(','.join(missingArtistIds))
    else:
        return
    populateArtists()

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

def addPageViews():
    artists = Artist.getAllWithoutViews(db)
    for artist in artists:
        name = artist.name.decode("utf-8").replace(' ', '_')
        endpoint = "https://wikimedia.org/api/rest_v1/metrics/pageviews/per-article/en.wikipedia/all-access/user/"+name+"/monthly/2016010100/2017123100"
        data = requests.get(endpoint).json()
        time.sleep(.3)
        if 'items' in data:
            data = data['items']
            count = 0
            for data in data:
                count += data['views']
            artist.views = count
            print("ARTIST: "+str(artist.name)+" COUNT: "+str(artist.views))
        else:
            print("Zero views for "+str(artist.name))
            artist.views = 0
        artist.updateViews(db)
def getFeaturedPlaylists():
    endpoint = "https://api.spotify.com/v1/browse/featured-playlists"
    tracks = requests.get(endpoint, headers=headers).json()
    print(tracks)

#https://api.spotify.com/v1/users/spotify/playlists?offset=200&limit=20
#opulateArtists()
#findArtist('0036ceq10ETP3tGK3AHNcr,003Lrmd4Hy04kSf0wZm3xm,004s3WVecP2IQy7Hw8gfoi,008wJbpZnkHRPcykr2hUye,00atTAydhxoyUusqZuaJby,00cwrbFzC9PwjFOIxTXyuU,00E0xvoM67oRJk8a5iTyEh,00eldNtAqcdLF9adKlyFZf,00G7U1s09YLtYGnwZTGru5,00gh6kmKYOu8xyorRxQm6a,00iJnnUu476m1HX16e3por,00KH6gMTJuNeeU5DCsrjcF,00me4Ke1LsvMxt5kydlMyU,00oL7zWxmWveTsKF7DnIRd,00RdKm1RuV3yg0hd79ZcPF')
#playlistsUrl = "https://api.spotify.com/v1/users/spotify/playlists?offset=280&limit=20"
#getPlaylists(playlistsUrl)
#getFollowers("37i9dQZF1DWX3387IZmjNa")
# 	/v1/users/{user_id}/playlists
#addPageViews()
makeGenres()
#getFeaturedPlaylists()