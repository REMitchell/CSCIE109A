import requests
import json
from category import Category
from database import Database
# 7240a6140225470db92cfb998b11213b
# 5ab4418cd35443639f96eba74b01c445
# curl -X "POST" -H "Authorization: Basic 5ab4418cd35443639f96eba74b01c445" -d grant_type=client_credentials https://accounts.spotify.com/api/token
db = Database()
token = "BQB5-BrQCqMIy51Izj8_SDk8c1VsAwf2P8f8g4zz-CeFPo6HCOYSAHXSo7tXLIjQxYOykzu4eXUn-2P9GiZOrJLIevvNBozG7-IaOxCpIje5-K2v8d9pNm-alOowJIGRdnc9GwMbcj2ajG9rjFvLDoUvrAnvYVOM0FC8QG73BNKTbJCvRzFw4HthJv1i_eMCHNaiM7Z-SPVDNKFLDaK-DJ2QR_N_jDJaLwvzjCyDudfUw1l17-AmwsJmAzKLyCtrycj1w6xY"
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

def getPlaylists():
    endpoint = "https://api.spotify.com/v1/browse/featured-playlists"
    playlists = requests.get(endpoint, headers=headers).json()

    for playlist in playlists['playlists']['items']:
        print(playlist)

def getTracks():
    endpoint = "https://api.spotify.com/v1/users/spotify/playlists/37i9dQZF1DWSUFOo47GEsI/tracks"
    tracks = requests.get(endpoint, headers=headers).json()
    for track in tracks['items']:
        print('\n')
        print(track)
#getPlaylists()
#getFollowers("37i9dQZF1DWX3387IZmjNa")
getTracks()
# 	/v1/users/{user_id}/playlists