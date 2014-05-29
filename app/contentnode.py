#!/usr/bin/env python3.4

from lib.basehandler import BaseHandler
from lib import database

class GetContentNode(BaseHandler):
    def get(self):
        node_id = self.get_int_argument("node_id")
        data = database.get("content_node", node_id)
        self.api_response(data)
