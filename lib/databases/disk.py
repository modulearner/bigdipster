import os
import copy
import ujson as json

import lib


_DATA = {}
_database_location = None
def init(data_location = "./data"):
    global _DATA, _database_location
    _database_location = data_location
    for table in os.listdir(data_location):
        database = {}
        table_path = os.path.join(data_location, table)
        for item in os.listdir(table_path):
            if not item.endswith(".json"):
                continue
            item_id = int(item.split(".")[0]) #dirty but i'm tired
            item_path = os.path.join(table_path, item)
            database[item_id] = json.load(open(item_path))
        _DATA[table] = database

def save(table, data, require_all_fields=True, overwrite_id=False):
    new_id = max(_DATA[table].iterkeys()) + 1
    item_id = data['node_id'] = data.get('node_id', None) or new_id
    if not overwrite_id and data['id'] in _DATA[table]:
        raise lib.InvalidInput([['node_id', 'ID already exists']])
    _DATA[table][item_id] = data
    json.dump(data, open("{}/{}/{}.json".format(_database_location, table, item_id), "w+"))
    return item_id

def update(table, item_id, data, require_all_fields=True):
    _DATA[table][item_id] = data
    json.dump(data, open("{}/{}/{}.json".format(_database_location, table, item_id), "w+"))

def get(table, item_id):
    try:
        return copy.deepcopy(_DATA[table][item_id])
    except KeyError:
        raise lib.ItemNotFound(item_id)

def exists(table, item_id):
    try:
        return item_id in _DATA[table]
    except KeyError:
        return False
