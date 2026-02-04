import os
from flask import Flask
from sqlalchemy import text
from src.extensions import db

def create_app():
    app = Flask(__name__)

    app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL")
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)

    @app.route('/')
    def home():
        return "Hello, Home!"
    
    @app.route('/test-db')
    def test_db():
        try:
            db.session.execute(text("SELECT 1"))
            return '<h1>Connection Successful</h1>'
        except:
            return '<h1>Connection Failed</h1>'

    return app