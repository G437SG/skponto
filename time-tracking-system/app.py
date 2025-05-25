from flask import Flask
from config.settings import Config
from app.routes import auth, admin, dashboard
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    
    # Create upload directory if it doesn't exist (local only)
    if not os.environ.get('RENDER'):
        upload_dir = os.path.join(app.static_folder or 'static', 'uploads')
        if not os.path.exists(upload_dir):
            os.makedirs(upload_dir)

    # Register blueprints
    app.register_blueprint(auth.bp)
    app.register_blueprint(admin.bp)
    app.register_blueprint(dashboard.bp)

    return app

app = create_app()

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)