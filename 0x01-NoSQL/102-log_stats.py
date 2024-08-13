#!/usr/bin/env python3
"""
Log stats
"""
from pymongo import MongoClient


def display_nginx_logs_stats(collection):
    """
    Displays statistics about Nginx request logs.
    """
    log_count = collection.count_documents({})
    print(f'{log_count} logs')

    print('Methods:')
    methods = ['GET', 'POST', 'PUT', 'PATCH', 'DELETE']
    for method in methods:
        method_count = collection.count_documents({'method': method})
        print(f'\tmethod {method}: {method_count}')

    status_check_count = collection.count_documents({'method': 'GET', 'path': '/status'})
    print(f'{status_check_count} status check')

    print('IPs:')
    top_ips = collection.aggregate([
        {"$group": {"_id": "$ip", "count": {"$sum": 1}}},
        {"$sort": {"count": -1}},
        {"$limit": 10}
    ])

    for ip in top_ips:
        print(f'\t{ip["_id"]}: {ip["count"]}')


def main():
    """
    Entry point for the script. Connects to MongoDB and displays stats.
    """
    client = MongoClient('mongodb://localhost:27017')
    db = client.logs
    nginx_collection = db.nginx
    display_nginx_logs_stats(nginx_collection)


if __name__ == '__main__':
    main()

