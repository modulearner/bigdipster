#!/usr/bin/env python3.4

import ujson as json
import os

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

def get(table, item_id):
    try:
        return data[table][item_id]
    except KeyError:
        raise ItemNotFound

