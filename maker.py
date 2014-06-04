#!/usr/bin/env python3.4

from tornado import web
from tornado import options
from tornado import httpserver
from tornado import ioloop

from app.usernode import (GetUserNode, GetUserNodeGraph)
from app.contentnode import GetContentNode
from app.user import GetUser
from app.ui import (CardView, CirclePack, TextbookView, EditContent)

options.define("port", default=8080, type=int, help="Port to serve on")
options.define("debug", default=False, type=bool, help="Debug Mode")

if __name__ == "__main__":
    options.parse_command_line()
    port = options.options.port
    debug = options.options.debug

    application = web.Application(
        [
            # API
            ('/api/v0/getusernode'      , GetUserNode      )  , 
            ('/api/v0/getcontentnode'   , GetContentNode   )  , 
            ('/api/v0/getuser'          , GetUser          )  , 
            ('/api/v0/getusernodegraph' , GetUserNodeGraph )  , 

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


    server = httpserver.HTTPServer(application)
    server.listen(port)
    print("Starting server on: {}".format(port))
    ioloop.IOLoop.instance().start()
