import tornado.ioloop
import tornado.web
import tornado.websocket
import nest_asyncio
import logging
import json
import datetime
from pseudoSensor import PseudoSensor
from humtempdb import HumTempDB

class Application(tornado.web.Application):
	def __init__(self,db,ps):
		logging.basicConfig(filename='sensorserver.log', filemode='w', level=logging.DEBUG)
		handlers = [(r"/", MainHandler), 
		(r"/ws", WSHandler), 
		(r'/css/(.*)', tornado.web.StaticFileHandler, {'path': './css'}),
		(r'/scripts/(.*)', tornado.web.StaticFileHandler, {'path': './scripts'}),
		]
		settings = dict(debug=True)
		tornado.web.Application.__init__(self, handlers, settings)
		self.ps = ps
		self.db = db

class MainHandler(tornado.web.RequestHandler) :
    def get(self):
	    self.render("sensorUI.html")

class WSHandler(tornado.websocket.WebSocketHandler):
	def open(self):
		logging.info("Connection to websocket open")

	def on_close(self):
        	logging.info("A client disconnected")

	def on_message(self, message):
		logging.info("message: {}".format(message))
		jsonObject = json.loads(message)
		action = jsonObject["action"]
		response = {}
		if action == "single":
			ts, hr, tr = self.get_1sample()
			response["timestamp"] = ts
			response["response"] = "reading"
			response["humidity"] = hr
			response["temperature"] = tr
		elif action == "stats":
			rows, stats = self.get_stats()
			response["response"] = "stats"
			response["humidity-min"] = stats[1]
			response["humidity-max"] = stats[2]
			response["humidity-avg"] = stats[0]
			response["temperature-min"] = stats[4]
			response["temperature-max"] = stats[5]
			response["temperature-avg"] = stats[3]
			dataHum = []
			dataTemp = []
			for sample in rows:
				dataHum.append(sample[2])
				dataTemp.append(sample[3])
			response["humidity-array"] = dataHum
			response["temperature-array"] = dataTemp
		self.write_message(json.dumps(response))

	def get_1sample(self):
		logging.info("Getting 1 sample")
		h,t = self.application.ps.generate_values()
		hr = round(h)
		tr = round(t)
		ts = get_timestamp()
		self.application.db.insert_record(ts,hr,tr)
		return ts,hr,tr

	def get_stats(self):
		rows = self.application.db.query_samples(10)
		stats = self.application.db.stats_samples(10)
		return rows, stats

def get_timestamp():
	ct = datetime.datetime.now()
	ts = ct.timestamp()
	return ts


if __name__ == "__main__":
    nest_asyncio.apply()
    database = r"C:\Users\laura\work\db\humtemp.db"
    db = HumTempDB(database)
    ps = PseudoSensor()
    app = Application(db,ps) 
    app.listen(8888)
    tornado.ioloop.IOLoop.current().start()