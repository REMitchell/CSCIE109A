from database import Database
from pymysql.err import InternalError
from artist import Artist
class Track:
    def __init__(self, spotifyId, album, artist1, artist2, artist3, name, duration, explicit, popularity):
        self.id = None
        self.spotifyId = spotifyId
        self.album = album
        self.artist1 = artist1
        self.artist2 = artist2
        self.artist3 = artist3
        self.name = name.encode('utf-8')
        self.duration = duration
        self.explicit = explicit
        self.popularity = popularity

    def fromDBRow(row):
        trackObj = Track(row['spotifyId'], row['album'], row['artist1'], row['artist2'], row['artist3'], row['name'], row['duration_ms'], row['explicit'], row['popularity'])
        trackObj.id = row['id']
        return trackObj

    def getArtists(self, db):
        self.artist1 = Artist.loadBySpotifyId(db, self.artist1)
        self.artist2 = Artist.loadBySpotifyId(db, self.artist2)
        self.artist3 = Artist.loadBySpotifyId(db, self.artist3)
        return self

    def linkToPlaylist(self, db, playlist):
        db.cur.execute("SELECT * FROM playlistTracks WHERE trackId = %s AND playlistId = %s", (self.id, playlist.id))
        try:
            if db.cur.rowcount == 0:
                db.cur.execute("INSERT INTO playlistTracks (trackId, playlistId) VALUES (%s, %s)", (self.id, playlist.id))
                db.conn.commit()
                return db.cur.lastrowid
            else:
                return db.cur.fetchall()[0]["id"]
            
        except InternalError as e:
            print("Error inserting playlist link")
            print(e)
            db.conn.rollback()

    def save(self, db):
        try:
            print("SELECT * FROM tracks WHERE spotifyId = {}".format(str(self.spotifyId)))
            db.cur.execute("SELECT * FROM tracks WHERE spotifyId = %s", (self.spotifyId))
            if db.cur.rowcount == 0:
                db.cur.execute("INSERT INTO tracks (spotifyId, album, artist1, artist2, artist3, name, duration_ms, explicit, popularity) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)", (self.spotifyId, self.album, self.artist1, self.artist2, self.artist3, self.name, self.duration, self.explicit, self.popularity))
                db.conn.commit()
                self.id = db.cur.lastrowid
            else:
                self.id = db.cur.fetchall()[0]["id"]
                print("ID IS NOW: "+str(self.id))

        except InternalError as e:
            print("Error inserting track "+self.name)
            print(e)
            db.conn.rollback()
        print("SAVED "+str(self.name))
        return self

