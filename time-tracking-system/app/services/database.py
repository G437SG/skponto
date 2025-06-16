from firebase_admin import credentials, firestore, initialize_app
import firebase_admin
import os
import json

class FirebaseService:
    """Firebase Database Service for the Time Tracking System"""
    
    def __init__(self):
        self.db = None
        self.initialize_firebase()

    def initialize_firebase(self):
        """Initialize Firebase Admin SDK"""
        if not firebase_admin._apps:
            try:
                # Try to use environment variables for Firebase config
                firebase_config = {
                    "type": "service_account",
                    "project_id": os.environ.get('FIREBASE_PROJECT_ID'),
                    "private_key_id": os.environ.get('FIREBASE_PRIVATE_KEY_ID'),
                    "private_key": os.environ.get('FIREBASE_PRIVATE_KEY', '').replace('\\n', '\n'),
                    "client_email": os.environ.get('FIREBASE_CLIENT_EMAIL'),
                    "client_id": os.environ.get('FIREBASE_CLIENT_ID'),
                    "auth_uri": "https://accounts.google.com/o/oauth2/auth",
                    "token_uri": "https://oauth2.googleapis.com/token",
                    "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
                    "client_x509_cert_url": os.environ.get('FIREBASE_CLIENT_CERT_URL')
                }
                
                # Only initialize if we have the required config
                if firebase_config["project_id"] and firebase_config["private_key"]:
                    cred = credentials.Certificate(firebase_config)
                    initialize_app(cred)
                    self.db = firestore.client()
                    print("Firebase initialized successfully")
                else:
                    print("Firebase config incomplete, using mock mode")
                    self.db = None
                    
            except Exception as e:
                print(f"Firebase initialization failed: {e}")
                self.db = None

    def get_collection(self, collection_name):
        """Get a Firestore collection reference"""
        if self.db:
            return self.db.collection(collection_name)
        return None

    def add_document(self, collection_name, data):
        """Add a document to a collection"""
        try:
            if self.db:
                doc_ref = self.db.collection(collection_name).add(data)
                return doc_ref[1].id
            return None
        except Exception as e:
            print(f"Error adding document: {e}")
            return None

    def get_document(self, collection_name, doc_id):
        """Get a document by ID"""
        try:
            if self.db:
                doc = self.db.collection(collection_name).document(doc_id).get()
                if doc.exists:
                    return doc.to_dict()
            return None
        except Exception as e:
            print(f"Error getting document: {e}")
            return None

    def update_document(self, collection_name, doc_id, data):
        """Update a document"""
        try:
            if self.db:
                self.db.collection(collection_name).document(doc_id).set(data)
                return True
            return False
        except Exception as e:
            print(f"Error updating document: {e}")
            return False

    def delete_document(self, collection_name, doc_id):
        """Delete a document"""
        try:
            if self.db:
                self.db.collection(collection_name).document(doc_id).delete()
                return True
            return False
        except Exception as e:
            print(f"Error deleting document: {e}")
            return False

    def query_collection(self, collection_name, field, operator, value, limit=None):
        """Query a collection with filters"""
        try:
            if self.db:
                query = self.db.collection(collection_name).where(field, operator, value)
                if limit:
                    query = query.limit(limit)
                
                docs = query.stream()
                results = []
                for doc in docs:
                    data = doc.to_dict()
                    data['id'] = doc.id
                    results.append(data)
                return results
            return []
        except Exception as e:
            print(f"Error querying collection: {e}")
            return []

    def get_all_documents(self, collection_name):
        """Get all documents from a collection"""
        try:
            if self.db:
                docs = self.db.collection(collection_name).stream()
                results = []
                for doc in docs:
                    data = doc.to_dict()
                    data['id'] = doc.id
                    results.append(data)
                return results
            return []
        except Exception as e:
            print(f"Error getting all documents: {e}")
            return []

    def is_connected(self):
        """Check if Firebase is connected"""
        return self.db is not None

# Create a global instance
firebase_service = FirebaseService()