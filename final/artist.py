from database import Database
from pymysql.err import InternalError

class Artist:
    def __init__(self, spotifyId, name, genres, followers, popularity):
        self.id = None
        self.spotifyId = spotifyId
        self.name = name.encode('utf-8')
        self.genres = genres
        self.followers = followers
        self.popularity = popularity
        self.views = None
    
    def fromDB(row):
        artist = Artist(row['spotifyId'], row['name'], row['genres'].split(','), row['followers'], row['popularity'])
        artist.id = row['id']
        artist.views = row['views']
        return artist

    def getAllWithoutViews(db):
        db.cur.execute("SELECT * FROM artists WHERE views IS NULL")
        rows = db.cur.fetchall()
        return [Artist.fromDB(row) for row in rows]

    def updateViews(self, db):
        db.cur.execute("UPDATE artists SET views = %s WHERE id = %s", (self.views, self.id))
        db.conn.commit()

    def loadBySpotifyId(db, spotifyId):
        if not spotifyId:
            return None
        db.cur.execute("SELECT * FROM artists WHERE spotifyId = %s", (spotifyId))
        row = db.cur.fetchall()
        if len(row) < 1:
            return None
        row = row[0]
        newArtist = Artist(row['spotifyId'], row['name'], row['genres'].split(','), row['followers'], row['popularity'])
        newArtist.id = row['id']
        newArtist.views = row['views']
        return newArtist

    def save(self, db):
        try:
            print("SELECT * FROM artists WHERE spotifyId = %s".format(self.spotifyId))
            db.cur.execute("SELECT * FROM artists WHERE spotifyId = %s", (self.spotifyId))

            if db.cur.rowcount == 0:
                print("Saving "+str(self.name))
                db.cur.execute("INSERT INTO artists (spotifyId, name, genres, followers, popularity) VALUES (%s, %s, %s, %s, %s)", (self.spotifyId, self.name, self.genres, self.followers, self.popularity))
                db.conn.commit()
                self.id = db.cur.lastrowid
            else:
                print("Already exists: "+str(self.name))
                self.id = db.cur.fetchall()[0]["id"]

        except InternalError as e:
            print("Error inserting artist")
            print(e)
            db.conn.rollback()


        return self

