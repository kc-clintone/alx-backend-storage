#!/usr/bin/env python3
"""
Top students
"""

from typing import List, Dict
from pymongo.collection import Collection


def top_students(mongo_collection: Collection) -> List[Dict]:
    """
    Returns a list of all students in a collection, sorted by their average score.
    Args:
        mongo_collection: The pymongo collection object.

    Returns:
        A list of dictionaries, where each dictionary represents a student document
        with an additional field "averageScore", sorted in descending order by the average score.
    """
    students = mongo_collection.aggregate(
        [
            {
                '$project': {
                    'name': 1,
                    'averageScore': {'$avg': '$topics.score'},
                    'topics': 1,
                },
            },
            {
                '$sort': {'averageScore': -1},
            },
        ]
    )
    return list(students)
