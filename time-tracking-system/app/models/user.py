from firebase_admin import firestore
from flask_bcrypt import Bcrypt
from datetime import datetime
import firebase_admin
from firebase_admin import credentials
import os
import json

bcrypt = Bcrypt()

# Initialize Firebase if not already initialized
def initialize_firebase():
    if not firebase_admin._apps:
        try:
            # Try to use environment variables
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
                firebase_admin.initialize_app(cred)
        except Exception as e:
            print(f"Firebase initialization failed: {e}")
            # For development, we'll use a mock setup
            pass

class User:
    def __init__(self, email=None, name=None, user_type='TRABALHADOR', password_hash=None, 
                 profile_picture=None, is_active=True, created_at=None, user_id=None):
        self.email = email
        self.name = name
        self.user_type = user_type  # ADMINISTRADOR, TRABALHADOR, ESTAGIÁRIO
        self.password_hash = password_hash
        self.profile_picture = profile_picture
        self.is_active = is_active
        self.created_at = created_at or datetime.utcnow()
        self.updated_at = datetime.utcnow()
        self.user_id = user_id

    def set_password(self, password):
        """Hash the password and store it"""
        self.password_hash = bcrypt.generate_password_hash(password).decode('utf-8')

    def check_password(self, password):
        """Check if the provided password matches the hashed password"""
        if not self.password_hash:
            return False
        return bcrypt.check_password_hash(self.password_hash, password)

    def to_dict(self):
        """Convert user object to dictionary for Firestore"""
        return {
            'email': self.email,
            'name': self.name,
            'user_type': self.user_type,
            'password_hash': self.password_hash,
            'profile_picture': self.profile_picture,
            'is_active': self.is_active,
            'created_at': self.created_at,
            'updated_at': self.updated_at
        }

    @classmethod
    def from_dict(cls, data, user_id=None):
        """Create user object from Firestore document"""
        return cls(
            email=data.get('email'),
            name=data.get('name'),
            user_type=data.get('user_type', 'TRABALHADOR'),
            password_hash=data.get('password_hash'),
            profile_picture=data.get('profile_picture'),
            is_active=data.get('is_active', True),
            created_at=data.get('created_at'),
            user_id=user_id
        )

    def save(self):
        """Save user to Firestore"""
        try:
            initialize_firebase()
            db = firestore.client()
            users_ref = db.collection('users')
            
            self.updated_at = datetime.utcnow()
            
            if self.user_id:
                # Update existing user
                users_ref.document(self.user_id).set(self.to_dict())
            else:
                # Create new user
                doc_ref = users_ref.add(self.to_dict())
                self.user_id = doc_ref[1].id
            
            return True
        except Exception as e:
            print(f"Error saving user: {e}")
            return False

    @classmethod
    def get_by_email(cls, email):
        """Get user by email from Firestore"""
        try:
            initialize_firebase()
            db = firestore.client()
            users_ref = db.collection('users')
            
            query = users_ref.where('email', '==', email).limit(1)
            docs = query.stream()
            
            for doc in docs:
                return cls.from_dict(doc.to_dict(), doc.id)
            
            return None
        except Exception as e:
            print(f"Error getting user by email: {e}")
            return None

    @classmethod
    def get_by_id(cls, user_id):
        """Get user by ID from Firestore"""
        try:
            initialize_firebase()
            db = firestore.client()
            
            doc = db.collection('users').document(user_id).get()
            if doc.exists:
                return cls.from_dict(doc.to_dict(), doc.id)
            
            return None
        except Exception as e:
            print(f"Error getting user by ID: {e}")
            return None

    @classmethod
    def get_all_users(cls):
        """Get all users from Firestore"""
        try:
            initialize_firebase()
            db = firestore.client()
            
            users = []
            docs = db.collection('users').stream()
            
            for doc in docs:
                users.append(cls.from_dict(doc.to_dict(), doc.id))
            
            return users
        except Exception as e:
            print(f"Error getting all users: {e}")
            return []

    def delete(self):
        """Delete user from Firestore"""
        try:
            if not self.user_id:
                return False
                
            initialize_firebase()
            db = firestore.client()
            db.collection('users').document(self.user_id).delete()
            return True
        except Exception as e:
            print(f"Error deleting user: {e}")
            return False

    def __repr__(self):
        return f'<User {self.email}>'