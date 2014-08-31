#!/usr/bin/env python3.4

from lib.basehandler import BaseHandler
from lib import database
from lib import InvalidInput


class ContentNode(BaseHandler):
    def get(self):
        node_id = self.get_int_argument("node_id")
        data = database.get("content_node", node_id)
        self.api_response(data)

    def put(self):
        data = self.get_all_arguments()
        # Now for some parsing!
        data['standards'] = [item.strip() for item in data['standards'].split(',')]

        try:
            node_id = database.save(
                "content_node", 
                data, 
                require_all_fields = False,
                overwrite_id = True
            )
            return self.api_response({
                "node_id" : node_id,
                "errors" : None,
            })
        except InvalidInput as error:
            return self.api_response({
                "node_id" : None,
                "errors" : error.errors_by_field,
            })
