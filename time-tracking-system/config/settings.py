import os
from datetime import timedelta

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-change-in-production'
    DEBUG = os.environ.get('DEBUG', 'False') == 'True'
    
    # Database configuration
    DATABASE_URI = os.environ.get('DATABASE_URI') or 'mongodb://localhost:27017/time-tracking'
    
    # Firebase configuration (if using Firebase Firestore)
    FIREBASE_PROJECT_ID = os.environ.get('FIREBASE_PROJECT_ID') or 'ponto-online-default'
    FIREBASE_PRIVATE_KEY_ID = os.environ.get('FIREBASE_PRIVATE_KEY_ID') or ''
    FIREBASE_PRIVATE_KEY = os.environ.get('FIREBASE_PRIVATE_KEY', '').replace('\\n', '\n') if os.environ.get('FIREBASE_PRIVATE_KEY') else ''
    FIREBASE_CLIENT_EMAIL = os.environ.get('FIREBASE_CLIENT_EMAIL') or ''
    FIREBASE_CLIENT_ID = os.environ.get('FIREBASE_CLIENT_ID') or ''
    FIREBASE_AUTH_URI = "https://accounts.google.com/o/oauth2/auth"
    FIREBASE_TOKEN_URI = "https://oauth2.googleapis.com/token"
    FIREBASE_CLIENT_CERT_URL = os.environ.get('FIREBASE_CLIENT_CERT_URL') or ''
    
    # Dropbox Configuration
    DROPBOX_ACCESS_TOKEN = os.environ.get('DROPBOX_ACCESS_TOKEN')
    DROPBOX_APP_KEY = os.environ.get('DROPBOX_APP_KEY')
    DROPBOX_APP_SECRET = os.environ.get('DROPBOX_APP_SECRET')
    
    # Session Configuration
    PERMANENT_SESSION_LIFETIME = timedelta(hours=8)
    
    # Upload Configuration
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max file size
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'pdf', 'doc', 'docx'}
    
    # Work Hours Configuration
    ADMIN_WORK_HOURS = 8
    WORKER_WORK_HOURS = 8
    INTERN_WORK_HOURS = 6
    LUNCH_BREAK = 1