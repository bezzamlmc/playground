import tornado.ioloop
import tornado.web
import tornado.websocket
import nest_asyncio
import logging
import json

class Application(tornado.web.Application):
	def __init__(self):
		logging.basicConfig(filename='sensorserver.log', filemode='w', level=logging.DEBUG)
		handlers = [(r"/", MainHandler), 
		(r"/ws", WSHandler)]
		settings = dict(debug=True)
		tornado.web.Application.__init__(self, handlers, settings)

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
			response["timestamp"] = "9000"
			response["response"] = "reading"
			response["humidity"] = 50
			response["temperature"] = 20
		elif action == "stats":
			response["response"] = "stats"
			response["humidity-min"] = 0
			response["humidity-max"] = 100
			response["humidity-avg"] = 30
			response["temperature-min"] = 0
			response["temperature-max"] = 80
			response["temperature-avg"] = 40
		self.write_message(json.dumps(response))


if __name__ == "__main__":
    nest_asyncio.apply()
    app =Application() 
    app.listen(8888)
    tornado.ioloop.IOLoop.current().start()