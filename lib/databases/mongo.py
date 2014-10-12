#!/usr/bin/env python2.7

import pymongo
import lib

_DB = None
_CLIENT = None
def init(uri='mongodb://localhost:27017/', test=False):
    global _DB, _CLIENT
    _CLIENT = pymongo.MongoClient(uri)
    _DB = _CLIENT["bigdipster"]


def save(table, data, require_all_fields=True, overwrite_id=False):
    global _DB
    try:
        item_id = _DB[table].insert(data) 
        return str(item_id)
    except KeyError:
        raise lib.ItemNotFound(item_id)

def update(table, item_id, data, require_all_fields=True):
    global _DB
    try:
        _DB[table].update({"_id" : item_id}, {"$set" : data}) 
    except KeyError:
        raise lib.ItemNotFound(item_id)

def get(table, item_id):
    global _DB
    try:
        _DB[table].find_one({"_id" : item_id})
    except KeyError:
        raise lib.ItemNotFound(item_id)

def exists(table, item_id):
    global _DB
    try:
        _DB[table].find_one({"_id" : item_id})
    except KeyError:
        raise lib.ItemNotFound(item_id)
