from database import Database
from pymysql.err import InternalError

class Category:
	
	def __init__(self, id, name, idstr):
		self.id = name
		self.name = name
		self.idstr = idstr

	def save(self, db):
		try:
			print("SELECT * FROM categories WHERE name = %s".format(self.name))
			db.cur.execute("SELECT * FROM categories WHERE name = %s", (self.name))

			if db.cur.rowcount == 0:
				db.cur.execute("INSERT INTO categories (name, idstr) VALUES (%s, %s)", (self.name, self.idstr))
				db.conn.commit()
				self.id = db.cur.lastrowid
			else:
				self.id = db.cur.fetchall()[0]["id"]

		except InternalError as e:
			print("Error inserting category")
			print(e)
			db.conn.rollback()


		return self

