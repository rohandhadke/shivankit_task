import os

class Config:
    # SECRET_KEY = os.environ.get("SECRET_KEY") or "your_secret_key"
    SECRET_KEY = "your_secret_key"
    SQLALCHEMY_DATABASE_URI = "postgresql://postgres:1010@localhost:5432/todo_db"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET_KEY = "your_jwt_secret_key"
    
