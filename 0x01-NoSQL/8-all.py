#!/usr/bin/env python3
"""
List all docs using python
"""


def list_all(mongo_collection):
    """
    Lists all docs in a collection.
    """
    return [document for document in mongo_collection.find()]
