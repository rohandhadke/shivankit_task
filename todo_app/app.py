from flask import Flask, render_template
from flask_jwt_extended import JWTManager
from config import Config
from models import db
from auth import auth_bp
from tasks import task_bp
from sqlalchemy.exc import OperationalError
from sqlalchemy import text 
from flask_cors import CORS
from flask_migrate import Migrate

app = Flask(__name__)
CORS(app)
app.config.from_object(Config)
migrate = Migrate(app, db)


db.init_app(app)
jwt = JWTManager(app)


app.register_blueprint(auth_bp)
app.register_blueprint(task_bp)

# In-memory set to store revoked tokens (for demo)
blacklist = set()

@jwt.token_in_blocklist_loader
def check_if_token_revoked(jwt_header, jwt_payload):
    return jwt_payload["jti"] in blacklist

@app.route('/')
def home():
    return render_template('index.html')
@app.route('/login')
def login():
    return render_template('auth.html')


if __name__ == '__main__':
    with app.app_context():
        try:
            db.create_all()
            db.session.execute(text('SELECT 1'))
            print("Database connected successfully!")
        except OperationalError as e:
            print("Failed to connect to the database!", e)

    app.run(debug=True)
