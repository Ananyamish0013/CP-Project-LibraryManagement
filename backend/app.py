import os
from flask import Flask
from flask_cors import CORS
from database import db
from routes import api_blueprint

def create_app():
    # Initialize the Flask Application
    app = Flask(__name__)
    
    # Enable CORS to allow the separate frontend to interact with the API
    CORS(app)
    
    # Database Configuration
    basedir = os.path.abspath(os.path.dirname(__file__))
    instance_path = os.path.join(basedir, 'instance')
    
    # Ensure instance directory exists for SQLite db file
    if not os.path.exists(instance_path):
        os.makedirs(instance_path)

    app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{os.path.join(instance_path, 'library.db')}"
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Bind the database instance to the app
    db.init_app(app)

    # Register all API endpoints dynamically
    app.register_blueprint(api_blueprint, url_prefix='/api')

    # Automatically create tables when the app runs
    with app.app_context():
        import models  # Important to make SQLAlchemy aware of the models
        db.create_all()

    return app

if __name__ == '__main__':
    app = create_app()
    # Run the Flask app on localhost, port 5000
    app.run(debug=True, port=5000)
