pip install tornado
pip install simplejson
pip install FastAPI
# postgres 
# remove pip install aiopg

# pass word 
pip install bcrypt

# print word
pip install markdown


    # Create the global connection pool.
    # async with aiopg.create_pool(
    #     host=options.db_host,
    #     port=options.db_port,
    #     user=options.db_user,
    #     password=options.db_password,
    #     dbname=options.db_database,
    # ) as db:
    #     app = Application(db)
    #     app.listen(options.port)
        # http_server = tornado.httpserver.HTTPServer(app)                                                            
        # http_server.listen(options.port)
        # print("😁😁😁😁😁 Start listern DB server !! 😁😁😁😁😁 port:" +str(options.db_port))
        # In this demo the server will simply run until interrupted
        # with Ctrl-C, but if you want to shut down more gracefully,
        # call shutdown_event.set().

    # shutdown_event = tornado.locks.Event()
    # await shutdown_event.wait()


        # app = tornado.web.Application([        
    #         (r"/", IndexHandler),
    #         (r"/login", LoginHandler),
    #         (r"/chat", ChatHandler),  
    #         (r"/logout", db_server.AuthCreateHandler)     
    #     ],
    #     websocket_ping_interval = 5,
    #     static_path = os.path.join(os.path.dirname(__file__), "static"),           
    #     template_path = os.path.join(os.path.dirname(__file__), "templates"),
    #     login_url='/login',                                                                                                               
    #     xsrf_cookies=True,                                                         
    #     cookie_secret="2hcicVu+TqShDpfsjMWQLZ0Mkq5NPEWSk9fi0zsSt3A=",
    #     debug = True,                                                         
    #     )