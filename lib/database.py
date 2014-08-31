#!/usr/bin/env python3.4

import lib
from lib import databases

class ItemNotFound(Exception):
    def __init__(self, node_id):
        self.node_id = node_id

STANDARDS = {"science" : "science"}

_BACKEND = None
def init_backend(backend):
    global _BACKEND
    try:
        _BACKEND = getattr(databases, backend)
        _BACKEND.init()
    except AttributeError:
        raise Exception("Could not find backend: {}".format(backend))


def save(table, data, require_all_fields=True, overwrite_id=False):
    if lib.schema.VERIFY[table](data, require_all_fields):
        return _BACKEND.save(table, data, require_all_fields, overwrite_id)
    return None

def update(table, item_id, data, require_all_fields=True):
    if lib.schema.VERIFY[table](data, require_all_fields):
        _BACKEND.update(table, item_id, data, require_all_fields)
        return True
    return False

def get(table, item_id):
    try:
        return _BACKEND.get(table, item_id)
    except KeyError:
        raise ItemNotFound

def exists(table, item_id):
    try:
        return _BACKEND.exists(table, item_id)
    except KeyError:
        return False
