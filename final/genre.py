from database import Database
from pymysql.err import InternalError
from collections import Counter

class Genre:
    def __init__(self, genreId, name):
        self.id = genreId
        self.name = name


    def getByPopularity(db):
        db.cur.execute('SELECT genres.name as name FROM artists JOIN artistGenres ON artists.id = artistGenres.artistId JOIN genres ON artistGenres.genreId = genres.id')
        rows = db.cur.fetchall()
        genres = Counter([row['name'] for row in rows])
        return genres
