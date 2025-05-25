from pymongo import MongoClient
from firebase_admin import credentials, firestore, initialize_app
import os

class Database:
    def __init__(self):
        self.db_type = os.getenv('DB_TYPE', 'mongodb')  # 'mongodb' or 'firestore'
        if self.db_type == 'mongodb':
            self.client = MongoClient(os.getenv('MONGODB_URI'))
            self.db = self.client[os.getenv('MONGODB_DB_NAME')]
        elif self.db_type == 'firestore':
            cred = credentials.Certificate(os.getenv('FIREBASE_CREDENTIALS'))
            initialize_app(cred)
            self.db = firestore.client()
        else:
            raise ValueError("Unsupported database type")

    def get_collection(self, collection_name):
        if self.db_type == 'mongodb':
            return self.db[collection_name]
        elif self.db_type == 'firestore':
            return self.db.collection(collection_name)

    def close(self):
        if self.db_type == 'mongodb':
            self.client.close()