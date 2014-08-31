#!/usr/bin/env python3.4

from lib import schema_utils as su
from collections import defaultdict

class InvalidInput(Exception):
    def __init__(self, errors):
        self.errors = errors

    @property
    def errors_by_field(self):
        errors_by_field = defaultdict(list)
        for field, error in self.errors:
            errors_by_field[field].append(error)
        return dict(errors_by_field)


def verify_content_node(data, require_all_fields=True):
    errors = list(su.check_data(data, su.content_node_fields, require_all_fields))
    if errors:
        raise InvalidInput(errors)
    return True

def verify_user(data, require_all_fields=True):
    errors = list(su.check_data(data, su.user_fields, require_all_fields))
    if errors:
        raise InvalidInput(errors)
    return True

def verify_user_node(data, require_all_fields=True):
    errors = list(su.check_data(data, su.user_node_fields, require_all_fields))
    if errors:
        raise InvalidInput(errors)
    return True

VERIFY = {
    "content_node" : verify_content_node,
    "user_node" : verify_user_node,
    "user" : verify_user,
}

