#!/usr/bin/env python3.4

from lib.basehandler import BaseHandler
from lib import database

import ujson as json

class ContentNode(BaseHandler):
    def get(self):
        node_id = self.get_int_argument("node_id")
        data = database.get("content_node", node_id)
        self.api_response(data)

    def put(self):
        node_id = self.get_int_argument("id")
        data_raw = self.get_argument("data")
        data = json.loads(data_raw)

        errors = database.save("content_node", node_id, data)
        self.api_response({"errors" : errors})
