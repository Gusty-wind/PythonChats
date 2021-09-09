import tornado.web
import tornado.ioloop
import tornado.httpserver
import tornado.options
import os,json
import datetime
import base64, uuid
import tornado.escape
import commen
import logging

import db_sql

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from tornado.web import RequestHandler
from tornado.options import define, options
from tornado.websocket import WebSocketHandler
from tornado import gen
from connection import connect_to_db, close_db_connection


define("port", default=9008, type="int", help="run in the basic root url")
define("title", default="Free To Talk !", type="string", help="web title")
logger = logging.getLogger(__name__)
summary_users = []
cookie = base64.b64encode(uuid.uuid4().bytes + uuid.uuid4().bytes)

class IndexHandler(RequestHandler):

    def get_current_user(self):
        user = self.get_argument(name='username_cur',default='None')
        if user and user != 'None':
            commen.created_file(self)
            print('IndexHandler CLASS get_current_user get current user:',user)
            return user
    @gen.coroutine
    @tornado.web.authenticated 
    def get(self):
        print("IndexHandler  GET Request")
        self.render("online_index.html",current_user=self.current_user)

    @tornado.web.authenticated
    def post(self, *args, **kwargs):
        # if self.current_user == None:
        #     self.redirect("/")
        print(self.current_user, '##############')
        self.render("online_index.html", current_user=self.current_user)


class LoginHandler(RequestHandler):
    def get(self, *args, **kwargs):
        cookie_value = self.get_secure_cookie('count')
        print('cookie_value :', cookie_value)
        count = int(cookie_value) + 1 if cookie_value else 1
        self.set_secure_cookie("count", str(count))
        self.render('login_use_form.html', title=options.title)

    def post(self, *args, **kwargs):
        print("send request post success !!!!!!!")
        pass
# return the iamge format string or bool value
def check_img_msg(cur_str):
    if cur_str.find('<img') > 0:
        first_part = cur_str[cur_str.find('<img'): len(cur_str)]
        image_str = first_part[0:first_part.find('",')]
        return image_str
    else:
        False

class ChatHandler(WebSocketHandler):
    def get_current_user(self):
        user = self.get_argument(name='username_cur',default='None')
        if user and user != 'None':
            return user 
    users = set()  # save the user list
    @tornado.web.authenticated
    def open(self):
        print('Get New WebSocket socket', self.current_user)
        self.users.add(self)  # create link and add user to connection 
        summary_users.append(self.current_user)
        #user join to channel
        for u in self.users:  
            obj = {
                "name": self.current_user,
                "isHeaderData": "true",
                "joinData":"true",
                "date": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "ip_address": self.request.remote_ip,
                "summary_users": summary_users
            }
            u.write_message(obj)

    def on_message(self, message):
        #send messsage to web
        message = json.loads(message)
        # print(type(message),message)
        if message.get('get_history_flg') != None:
            list_user = list(self.users)
            for i in range(len(list_user)):
                if message.get('current_view_user')  == list_user[i].current_user:
                    history_data_message = commen.file_read_message(message.get('user'))
                    if history_data_message != None:
                        for index in range(len(history_data_message)):
                            record = history_data_message[index]
                            record = json.loads(record)
                            record = record.replace("'", '"')
                            record = json.dumps(record)
                            hh = json.loads(record)
                            # if the message include the image file, do the format fuc
                            ifimge_str =  check_img_msg(hh)
                            if ifimge_str == None:
                                hh = json.loads(hh)
                                msg_datas = {
                                    "name": hh['chatFrom'],
                                    "message": hh['message'],
                                    "date": hh['date'],
                                    "isHeaderData": hh['isHeaderData'],
                                    "chatFromchatTo": hh['chatTo'],
                                    "chatFrom": hh['chatFrom'],
                                    "flow_single_user": "true"
                                }
                            else:
                                hh = hh.replace(ifimge_str, '##')
                                hh = json.loads(hh)
                                msg_datas = {
                                    "name": hh['chatFrom'],
                                    "message": ifimge_str,
                                    "date": hh['date'],
                                    "isHeaderData": hh['isHeaderData'],
                                    "chatFromchatTo": hh['chatTo'],
                                    "chatFrom": hh['chatFrom'],
                                    "flow_single_user": "true"
                                }

                            # for u in self.users:
                            if (list_user[i].current_user == hh['chatFrom'] or list_user[i].current_user == hh['chatTo']):
                                list_user[i].write_message(msg_datas)
        else:
            for u in self.users:  # send message to all users
                obj = {
                    "name": self.current_user,
                    "message": message.get('msg'),
                    "date": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    "isHeaderData": "false",
                    "chatTo": message.get('pointer')['chatTo'],
                    "chatFrom": message.get('pointer')['chatFrom'],
                    "flow_single_user": "false"
                }

                if u._current_user == message.get('pointer')['chatTo'] or  u._current_user == message.get('pointer')['chatFrom']:
                    # create_get_filename = commen.get_user_file_name_path(str(u._current_user))
                    commen.file_write_message(str(u._current_user), obj)
                    # commen.file_read_message(create_get_filename)
                    u.write_message(obj)

    def on_close(self):
        self.users.remove(self)
        summary_users.remove(self.current_user) 
         #user left message
        for u in self.users:
            obj = {
                "name": self.current_user,
                "isHeaderData": "true",
                "joinData":"false",
                "date": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "ip_address": self.request.remote_ip,
                "summary_users": summary_users
            }
            u.write_message(obj)

    def check_origin(self, origin):
        #parsed_origin =urllib.parse.urlparse(origin)
        #return parsed_origin.netloc.endswith(".xxx.com")
        return True

class Test(RequestHandler):
    #lister the router
    async def get(self):
        print("GET !!!!!")
        await db_sql.Apihandler.test()
        self.render("register.html", cur_title = '@@@')

def main():
    return tornado.web.Application([        
        (r"/", IndexHandler),
        (r"/login", LoginHandler),
        (r"/chat", ChatHandler), 
        (r"/test", Test),  
    ],
    websocket_ping_interval = 5,
    static_path = os.path.join(os.path.dirname(__file__), "static"),           
    template_path = os.path.join(os.path.dirname(__file__), "templates"),
    login_url='/login',                                                                                                               
    xsrf_cookies=True,                                                         
    cookie_secret="2hcicVu+TqShDpfsjMWQLZ0Mkq5NPEWSk9fi0zsSt3A=",
    debug = True,                                                         
    )
async def get_listener_host():
    conn = await connect_to_db()
    cursor = conn.cursor()
    logger.warn("--- **** DB connect success **** ---")
    logger.warn("--- **** Start query listern platfrom name **** ---")
    sql = "select hostname from  listenuserdatas where deleted  = 'false' "
    cursor.execute(sql)
    data = cursor.fetchall()
    conn.commit()
    await close_db_connection(conn, cursor)
    logger.warn("--- **** end query listern platfrom name **** ---")
    return data

async def main_app():
    # conn = await connect_to_db()
    # cursor = conn.cursor()

    # datas = await get_listener_host()
    # print (datas)

    app = main()
    app.listen(options.port)
    """
        keep server connect 
    """
    shutdown_event = tornado.locks.Event()
    await shutdown_event.wait()

if __name__ == '__main__':
    tornado.options.parse_command_line()
    print('🤟🤟🤟 Create server connect ....🤟🤟🤟')
    print('👏👏👏 Main Server is start at: localhost:'+ str(options.port))   
    tornado.ioloop.IOLoop.current().run_sync(main_app)   
               