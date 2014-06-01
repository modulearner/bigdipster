#!/usr/bin/env python3.4

from lib.basehandler import BaseHandler
from lib import database

class GetUserNode(BaseHandler):
    def get(self):
        node_id = self.get_int_argument("node_id")
        data = database.get("user_node", node_id)
        self.api_response(data)


class GetUserNodeGraph(BaseHandler):
    def get(self):
        node_id = self.get_int_argument("node_id")
        data = database.get("user_node", node_id)
        data = extract_full_graph(data)
        self.api_response(data)

def extract_full_graph(data):
    for i, child in enumerate(data["children"]):
        if child["type"] != "content_node":
            node_id = child["id"]
            child_info = database.get("user_node", node_id)
            extract_full_graph(child_info)
            child["children"] = child_info
    return data
