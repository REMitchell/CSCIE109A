import pymysql

class Database:

    def __init__(self):
        #Assumes port 3306
        #self.conn = pymysql.connect(host='localhost', port=3306, unix_socket='/tmp/mysql.sock', user='root', passwd='root', db='mysql', charset='utf8')
        self.conn = pymysql.connect(host='localhost', port=3306, user='root', passwd='root', db='mysql')
        self.cur = self.conn.cursor(pymysql.cursors.DictCursor)
        self.cur.execute("USE playlists")