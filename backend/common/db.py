from pymongo import MongoClient
from flask import jsonify
from . import config
import logging
import sys
import os
from bson.json_util import dumps

logging.basicConfig(stream=sys.stdout)
LOGGER = logging.getLogger(__name__)
LOGGER.setLevel(config.LOG_LEVEL)

class DBConnector:
    def __init__(self):
        self.client = MongoClient(
            'mongodb://localhost:27017'
            # 'mongo',
            # 27017,
            # username=os.getenv('MONGO_INITDB_ROOT_USERNAME'),
            # password=os.getenv('MONGO_INITDB_ROOT_PASSWORD')
        )

        self.db = self.client["finances"]

        self._init_db()
    
    def _init_db(self):
        expenses = self.db.expenses
        revenue = self.db.revenue
    
    def insert_one(self, col, item):
        result = self.db[col].insert_one(item)
        
        return dumps(result.inserted_id)

    def get_one(self, col, filt=None):
        return self.db[col].find_one(filter=filt)

    def get_all(self, col, filt=None, fields=None):
        return self.db[col].find(filt, fields)

    def update_one(self, col, filt, data):
        self.db[col].update_one(
            filt,
            data
        )
    
    def delete_one(self, col, filt):
        self.db[col].delete_one(
            filt
        )

    def delete_all(self, col):
        self.db[col].delete_many({})