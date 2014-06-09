#!/usr/bin/env python3.4

import os
import sys
base_dir = os.path.dirname(__file__)
sys.path.append(os.path.abspath(os.path.join(base_dir, "..")))

from lib import schema
from lib import database as db

def test_verify_content_node():
    valid_data = db.get("content_node", 1)
    assert len(schema.verify_content_node(valid_data)) == 0

def test_verify_content_node_base_node():
    data = db.get("content_node", 1)
    data['base_node'] = 28
    errors = schema.verify_content_node(data)
    assert len(errors) == 1 and errors[0][0] == 'base_node'

    data['base_node'] = 1
    errors = schema.verify_content_node(data)
    assert len(errors) == 0

def test_verify_content_recommended_time():
    data = db.get("content_node", 1)
    data['recommended_time'] = -1
    print data
    errors = schema.verify_content_node(data)
    assert len(errors) == 1 and errors[0][0] == 'recommended_time'

    data['recommended_time'] = 100
    errors = schema.verify_content_node(data)
    assert len(errors) == 0

def test_verify_content_creator():
    data = db.get("content_node", 1)
    data['creator'] = -1
    errors = schema.verify_content_node(data)
    assert len(errors) == 1 and errors[0][0] == 'creator'

    data['creator'] = None
    errors = schema.verify_content_node(data)
    assert len(errors) == 1 and errors[0][0] == 'creator'

def test_verify_content_partial_data():
    data = db.get("content_node", 1)
    data.pop("base_node")

    errors = schema.verify_content_node(data)
    assert len(errors) == 1 and errors[0][0] == 'base_node'

    errors = schema.verify_content_node(data, require_all_fields=False)
    assert len(errors) == 0

def test_verify_user_node():
    data = db.get("user_node", 1)
    errors = schema.verify_user_node(data)
    assert len(errors) == 0
