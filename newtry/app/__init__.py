from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path

db = SQLAlchemy()
DB_NAME = "history.db"

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'ball'
    #app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{path.join(app.root_path, DB_NAME)}'
    db.init_app(app)
    
    from app.views import views
    
    app.register_blueprint(views, url_prefix='/')
    
    from .models import historyItem
    
    if not path.exists('newtry/app/' + DB_NAME):
        with app.app_context():
            db.create_all()
            print("db made.")
    
    return app