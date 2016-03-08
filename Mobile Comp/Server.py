import tornado.httpserver
import tornado.ioloop
import tornado.web
import sqlite3
import sys

_db = sqlite3.connect('milkandball.db')
_cursor = _db.cursor()

class databaseRequestHandler(tornado.web.RequestHandler):
    def delete(self):
        _cursor.execute("DROP TABLE IF EXISTS data")
        _cursor.execute("CREATE TABLE data (item STRING, price REAL, quantity INT)")
        milk_values = ["milk", None, None]
        ball_values = ["ball", None, None]
        _cursor.execute("INSERT INTO data VALUES (?,?,?)", milk_values)
        _cursor.execute("INSERT INTO data VALUES (?,?,?)", ball_values)
        _db.commit()
        self.write('OK')
    def get(self):
        _cursor.execute("SELECT * FROM sqlite_master")
        for row in _cursor:
            self.write(row)
         
         
class itemRequestHandler(tornado.web.RequestHandler):
    def put(self, item):
      
        if self.get_argument("price") != None:
            record = (self.get_argument("price"), item)
            _cursor.execute("UPDATE data SET price=? WHERE item=?", record)
            _db.commit()
            self.write('OK')
        elif self.get_argument("quantity") != None:
            record = (self.get_argument("quantity"), item)
            _cursor.execute("UPDATE data SET quantity=? WHERE item=?", record)
            _db.commit()
            self.write('OK')
    def get(self, item):
        if self.get_argument("price") == 'true':
	    
            _cursor.execute("SELECT price FROM data WHERE item=?", (item,))
	    for row in _cursor:
                self.write(item+" unit price: "+str(row[0]))
        elif self.get_argument("quantity") == 'true':
            _cursor.execute("SELECT quantity FROM data WHERE item=(?)", (item,))            
	    for row in _cursor:
                self.write(item+" stock level: "+str(row[0]))
        

application = tornado.web.Application([
#(r"/sensor/([0-9]+)", sensorRequestHandler),
    (r"/database", databaseRequestHandler),
    (r"/item/(.*)", itemRequestHandler),
    #(r"/item/ball", ballRequestHandler),    
 
])

if __name__ == "__main__":
	http_server = tornado.httpserver.HTTPServer(application)
	http_server.listen(43210)
	tornado.ioloop.IOLoop.instance().start()
