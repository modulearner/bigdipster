#!/usr/bin/env python3.4

import lib
import ujson as json
import os
import copy

data = {}
for table in os.listdir("./data"):
    database = {}
    table_path = os.path.join("./data", table)
    for item in os.listdir(table_path):
        if not item.endswith(".json"):
            continue
        item_id = int(item.split(".")[0]) #dirty but i'm tired
        item_path = os.path.join(table_path, item)
        database[item_id] = json.load(open(item_path))
    data[table] = database

class ItemNotFound(Exception):
    pass

STANDARDS = {"science" : "science"}

def save(table, item_id, data, require_all_fields=True):
    errors = lib.schema.VERIFY[table](data, require_all_fields)
    if errors is not None:
        return errors
    data[table][item_id] = data
    json.dump(data, open("./data/{}/{}.json".format(table, item_id), "w+"))

def get(table, item_id):
    try:
        return copy.deepcopy(data[table][item_id])
    except KeyError:
        raise ItemNotFound

def exists(table, item_id):
    try:
        return item_id in data[table]
    except KeyError:
        return False
