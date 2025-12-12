import tornado.web
import tornado.escape

class ResourceHandler(tornado.web.RequestHandler):
    def initialize(self, xapp):
        self.xapp = xapp

    def post(self):
        body = tornado.escape.json_decode(self.request.body)
        self.xapp.kafka().json().send_message("resource-reconfiguration", body)
        self.write("Resource reconfiguration succesfully requested! \n")
