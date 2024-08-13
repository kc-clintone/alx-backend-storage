#!/usr/bin/env python3
"""
 Where can I learn Python?
"""


def schools_by_topic(mongo_collection, topic):
    """
    Returns the list of school with specific topics
    """
    fltr = {
        'topics': {
            '$elemMatch': {
                '$eq': topic,
            },
        },
    }
    return [document for document in mongo_collection.find(fltr)]
