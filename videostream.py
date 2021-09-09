from tornado.httputil import HTTPHeaders, ResponseStartLine
import tornado.httpserver
import tornado.options
import tornado.ioloop
import tornado.routing
import tornado.httputil


from tornado.httputil import HTTPMessageDelegate
from tornado.httpserver import HTTPServer
from tornado.options import define, options
from tornado.routing import Router

class CustomRouter(Router):
    def find_handler(self, request, **kwargs):
        return MessageDelegate(request.connection)
class MessageDelegate(HTTPMessageDelegate):
    def __init__(self, connection):
        self.connection = connection
    def finish(self):
        self.connection.write_headers(
            ResponseStartLine("HTTP/1.1 200 OK"),
            HTTPHeaders({"Content-Length": "2"}),
            b"OK")
        self.connection.finish()
router = CustomRouter()
server = HTTPServer(router)