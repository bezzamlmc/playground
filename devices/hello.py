# -*- coding: utf-8 -*-
"""
Created on Wed Jun  9 13:09:39 2021

@author: laura
"""
import tornado.ioloop
import tornado.web
import nest_asyncio

class MainHandler(tornado.web.RequestHandler) :
    def get(self):
        self.write("Hello, world")

def make_app():
    return tornado.web.Application([
        (r"/", MainHandler),
    ])

if __name__ == "__main__":
    nest_asyncio.apply()
    app = make_app()
    app.listen(8888)
    tornado.ioloop.IOLoop.current().start()