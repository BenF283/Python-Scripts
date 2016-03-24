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

        for line in _db.iterdump():
            self.write(line)         
         
class itemRequestHandler(tornado.web.RequestHandler):
    def put(self, item):
	_cursor.execute("SELECT * FROM data WHERE item=?", (item,))
 	result = _cursor.fetchone()
	if result != None:
	        if self.get_argument("price","x") != "x":
                    record = (self.get_argument("price"), item)
                    _cursor.execute("UPDATE data SET price=? WHERE item=?", record)
                    _db.commit()
                    self.write('OK')
     		elif self.get_argument("quantity", "x") != "x":
            		record = (self.get_argument("quantity"), item)
          		_cursor.execute("UPDATE data SET quantity=? WHERE item=?", record)
            		_db.commit()
		        self.write('OK')
	else:
		self.set_status(404)
	
    def get(self, item):
	_cursor.execute("SELECT * FROM data WHERE item=?", (item,))
	result = _cursor.fetchone()
	if result != None:
	        if self.get_argument("price", "x") == 'true':
	    
        	    _cursor.execute("SELECT price FROM data WHERE item=?", (item,))
	    	    for row in _cursor:
        	    	self.write(item+" unit price: "+str("{0:.2f}".format(row[0])))
	        elif self.get_argument("quantity", "x") == 'true':
        	    _cursor.execute("SELECT quantity FROM data WHERE item=(?)", (item,))            
	    	    for row in _cursor:
		        self.write(item+" stock level: "+str(row[0]))
		elif self.get_argument("value", "x") == 'true':
		    _cursor.execute("SELECT quantity FROM data WHERE item=(?)", (item,))
		    for row in _cursor:
			quantity = row[0]
		    _cursor.execute("SELECT price FROM data WHERE item=(?)", (item,))
		    for row in _cursor:
			price = row[0]
	    	    self.write(item+" total stock value: " + str("{0:.2f}".format(price * quantity)))
	else:
	        self.set_status(404)
        

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
