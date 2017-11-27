from database import Database
from pymysql.err import InternalError

class Genre:
	def __init__(self, genreId, name):
        self.id = genreId
		self.name = name



