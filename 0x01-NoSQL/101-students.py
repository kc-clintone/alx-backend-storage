#!/usr/bin/env python3
"""
Top students
"""

def top_students(mongo_collection):
    """
    Returns a list of all students in a collection, sorted by their average scores
    """
    students = mongo_collection.aggregate([
        {
            '$project': {
                'name': 1,
                'topics': 1,
                'averageScore': {
                    '$avg': '$topics.score',
                },
            },
        },
        {
            '$sort': {'averageScore': -1},
        },
    ])
    return list(students)
