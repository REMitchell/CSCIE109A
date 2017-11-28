from database import Database
from pymysql.err import InternalError
from track import Track

class Playlist:
    
    def __init__(self, spotifyId, name, description, trackCount, followers):
        self.id = None
        self.spotifyId = spotifyId
        self.name = name.encode('utf-8') if name else None
        self.description = description.encode('utf-8') if description else None
        self.trackCount = trackCount
        self.followers = followers
        self.tracks = None
        self.bestGenre = None


    def fromDBRow(row):
        tmpPlaylist = Playlist(row['spotifyId'], row['name'], row['description'], row['trackCount'], row['followers'])
        tmpPlaylist.id = row['id']
        return tmpPlaylist

    def loadAll(db):
        db.cur.execute("SELECT * FROM playlists")
        rows = db.cur.fetchall()
        playlists = []
        for row in rows:
            playlists.append(Playlist.fromDBRow(row).getTracks(db))
        return playlists

    def getTracks(self, db):
        db.cur.execute("SELECT tracks.* FROM tracks JOIN playlistTracks ON playlistTracks.trackId = tracks.id WHERE playlistTracks.playlistId = %s", (self.id))
        rows = db.cur.fetchall()
        self.tracks = []
        for row in rows:
            tmpTrack = Track.fromDBRow(row)
            self.tracks.append(tmpTrack.getArtists(db))
        return self

    def playlistExists(self, db):
        try:
            db.cur.execute("SELECT * FROM playlists WHERE spotifyId = %s", (self.spotifyId))
            return db.cur.rowcount != 0

        except InternalError as e:
            print("ERROR GETTING PLAYLIST EXISTENCE")


    def save(self, db):
        try:
            db.cur.execute("SELECT * FROM playlists WHERE spotifyId = %s", (self.spotifyId))
            if db.cur.rowcount == 0:
                db.cur.execute("INSERT INTO playlists (spotifyId, name, description, trackCount, followers) VALUES (%s, %s, %s, %s, %s)", (self.spotifyId, self.name, self.description, self.trackCount, self.followers))
                db.conn.commit()
                self.id = db.cur.lastrowid
            else:
                self.id = db.cur.fetchall()[0]["id"]

        except InternalError as e:
            print("Error inserting playlist")
            print(e)
            db.conn.rollback()


        return self