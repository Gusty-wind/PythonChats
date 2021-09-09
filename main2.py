import os.path
import tornado.web
import tornado.ioloop
import tornado.autoreload
import tornado.options
import asyncio
import tornado.locks
import uuid
import tornado.escape

import tornado.httpserver
from tornado.web import RequestHandler
from tornado.options import options, define, parse_command_line

define("port", default=9007, type="int", help="run in the basic root url")
define("title", default="Talk To Free", type="str", help="just a title")
define("debug", default=True, type="bool", help="is open debug module")


class MessageBuffer(object):
      def __init__(self):
            self.cond = tornado.locks.Condition()
            self.cache = []
            self.cache_sie = 300
      def get_message_since(self, cursor):
            result = []
            for msg in reversed(self.cache):
                if msg["id"] == cursor:
                  break
                result.append(msg)
            result.reverse()
            return result
      def add_message(self, message):
          self.cache.append(message)
          if len(self.cache) > self.cache_sie:
                self.cache = self.cache[-self.cache_sie :]
          self.cond.notify_all()
global_message_buffer = MessageBuffer()

class BadRequestHandler(RequestHandler):
    def get(self):
        raise tornado.web.HTTPError(400)

    post = get

class MainHandler(RequestHandler):
  def get(self):
      user = str(uuid.uuid4())
      self.set_cookie("username", user, domain=None,expires=None, path="/")
      self.render("index.html",title= options.title , messages = global_message_buffer.cache, username = user)

class MessageNewHandler(RequestHandler):
      
      def set_default_headers(self):
          print('set headers!!')
          self.set_header('Access-Control-Allow-Origin', '*')
          self.set_header('Access-Control-Allow-Headers', '*')
          self.set_header('Access-Control-Max-Age', 1000)
          self.set_header("Content-Type", "application/json; charset=UTF-8")  
          self.set_header('Access-Control-Allow-Methods', 'POST, GET, OPTIONS')
          self.set_header('Access-Control-Allow-Headers',
                        'Content-Type, Access-Control-Allow-Origin, Access-Control-Allow-Headers, X-Requested-By, Access-Control-Allow-Methods')
      def options(self):
            pass

      def get(self):
            username = str(self.get_cookie("username"))
            message = {"id": str(uuid.uuid4()), "body": username + ": " + self.get_argument("body")}
            message["html"] = tornado.escape.to_unicode(
              self.render_string("message.html", message = message)
            )
            if self.get_argument("next", None):
                  self.redirect(self.get_argument("next"))
            else:
                  self.write(message)
      def post(self):
            username = str(self.get_cookie("username"))
            message = {"id": str(uuid.uuid4()), "body": username + ": " + self.get_argument("body")}
            message["html"] = tornado.escape.to_unicode(
              self.render_string("message.html", message = message)
            )
            if self.get_argument("next", None):
                  self.redirect(self.get_argument("next"))
            else:
                  self.write(message)
            global_message_buffer.add_message(message)

class MessageUpdatesHandler(tornado.web.RequestHandler):
      async def post(self):
            cursor = self.get_argument("cursor", None)
            messages = global_message_buffer.get_message_since(cursor)
            while not messages:
                  self.wait_future = global_message_buffer.cond.wait()
                  try:
                    await self.wait_future
                  except asyncio.CancelledError:
                    return
                  messages = global_message_buffer.get_message_since(cursor)
            if self.request.connection.stream.closed():
                return
            self.write(dict(messages = messages))
      def on_connection_close(self):
            self.wait_future.cancel()

def make_app():
    return tornado.web.Application([
      (r"/", MainHandler),
      (r"/a/message/new", MessageNewHandler),
      (r"/a/message/updates", MessageUpdatesHandler),
      (r"/.*", BadRequestHandler),
    ], 
      cookies_secret = "_TODO:_GENERATE_YOUR_OWN_RANDOM_VALUE_HERE__",
      debug=options.debug,
      template_path= os.path.join(os.path.dirname(__file__), "templates"),
      static_path = os.path.join(os.path.dirname(__file__), "static"),
      xsrf_cookies=True,
    )

def main():
    parse_command_line()
    print('create app....')
    app = make_app()
    print('create listen port....')
    app.listen(options.port)
    print('server is start at: localhost:'+ str(options.port))
    tornado.ioloop.IOLoop.current().start()
    

if __name__ == "__main__":
   main()

