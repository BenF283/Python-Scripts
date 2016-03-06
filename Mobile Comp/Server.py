import tornado.httpserver
import tornado.ioloop
import tornado.web
import sqlite3
import sys

_db = sqlite3.connect('sensors.db')
_cursor = _db.cursor()

class sensorRequestHandler(tornado.web.RequestHandler):
	def get(self, ID):
	    range = self.get_argument("range",default="0,"+str(sys.maxint)).split(',')
	    params = [ID]+range
	    _cursor.execute("SELECT * FROM data WHERE ID=? AND time>=? AND time <=?", params)
	    records = []
	    for row in _cursor:
		records = records + [{'ID':row[0],'value':row[1],'time':row[2]}]
	    self.write(tornado.escape.json_encode(records))
	def put(self, ID):
	    record = (int(ID), float(self.get_argument("value")), int(self.get_argument("time")))
	    _cursor.execute("INSERT INTO data VALUES (?,?,?)", record)
	    _db.commit()
	    self.write('OK')
	def delete(self):
		_cursor.execute("DROP TABLE IF EXISTS data")
		_cursor.execute("CREATE TABLE data (ID INT, value REAL, time INT)")
		_db.commit()
		self.write('OK')

application = tornado.web.Application([
	(r"/sensor/([0-9]+)", sensorRequestHandler),
	(r"/sensors/all", sensorRequestHandler),
])

if __name__ == "__main__":
	http_server = tornado.httpserver.HTTPServer(application)
	http_server.listen(43210)
	tornado.ioloop.IOLoop.instance().start()
