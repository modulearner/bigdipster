#!/usr/bin/env python3.4

from lib import schema_utils as su

def verify_content_node(data, require_all_fields=True):
    return list(su.check_data(data, su.content_node_fields, require_all_fields))

def verify_user(data, require_all_fields=True):
    return list(su.check_data(data, su.user_fields, require_all_fields))

def verify_user_node(data, require_all_fields=True):
    return list(su.check_data(data, su.user_node_fields, require_all_fields))

VERIFY = {
    "content_node" : verify_content_node,
    "user_node" : verify_user_node,
    "user" : verify_user,
}

