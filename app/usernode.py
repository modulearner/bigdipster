#!/usr/bin/env python3.4

from lib import database as db
from lib.basehandler import BaseHandler

class UserNode(BaseHandler):
    def get(self):
        node_id = self.get_int_argument("node_id")
        data = db.get("user_node", node_id)
        self.api_response(data)


class UserNodeGraph(BaseHandler):
    def get(self):
        node_id = self.get_int_argument("node_id")
        max_depth = self.get_int_argument("max_depth", 4)
        print max_depth
        data = db.get("user_node", node_id)
        data = extract_full_graph(data, max_depth-1)
        self.api_response(data)

def extract_full_graph(data, max_depth):
    if max_depth > 0:
        for i, child in enumerate(data["children"]):
            if child["type"] != "content_node":
                node_id = child["id"]
                child_info = db.get("user_node", node_id)
                extract_full_graph(child_info, max_depth-1)
                child["children"] = child_info['children']
            else:
                child["children"] = []
    return data
