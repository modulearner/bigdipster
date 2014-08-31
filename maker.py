#!/usr/bin/env python3.4

from tornado import web
from tornado import options
from tornado import httpserver
from tornado import ioloop

from app.usernode import (UserNode, UserNodeGraph)
from app.contentnode import ContentNode
from app.user import User
from app.ui import (CardView, CirclePack, TextbookView, EditContent)
import lib.database

options.define("port", default=8080, type=int, help="Port to serve on")
options.define("debug", default=False, type=bool, help="Debug Mode")
options.define("backend", default='disk', type=str, help="Database backend to use")

if __name__ == "__main__":
    options.parse_command_line()
    port = options.options.port
    debug = options.options.debug

    application = web.Application(
        [
            # API
            ('/api/v0/usernode'      , UserNode      )  , 
            ('/api/v0/contentnode'   , ContentNode   )  , 
            ('/api/v0/user'          , User          )  , 
            ('/api/v0/usernodegraph' , UserNodeGraph )  , 

            # Visualizations
            ('/ui/cardview'   , CardView   )  , 
            ('/ui/circlepack' , CirclePack )  , 
            ('/ui/textbookview' , TextbookView)  , 
            ('/ui/editcontent' , EditContent) ,
        ],
        debug = debug,
        template_path = './templates/',
        static_path = './static/',
    )

    print "Using database: ", options.options.backend
    lib.database.init_backend(options.options.backend)


    server = httpserver.HTTPServer(application)
    server.listen(port)
    print("Starting server on: {}".format(port))
    ioloop.IOLoop.instance().start()
