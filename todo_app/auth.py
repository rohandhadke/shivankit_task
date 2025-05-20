from flask import Blueprint, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from models import db, TodoUser
from flask_jwt_extended import get_jwt


auth_bp = Blueprint("auth", __name__)

@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    existing_user = TodoUser.query.filter_by(username=data['username']).first()
    if existing_user:   
        return jsonify(message="Username is already registered"), 409  

    hashed_password = generate_password_hash(data['password'])
    todo_user = TodoUser(username=data['username'], password=hashed_password)
    db.session.add(todo_user)
    db.session.commit()
    return jsonify(message="User registered"), 201

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    todo_user = TodoUser.query.filter_by(username=data['username']).first()
    if todo_user and check_password_hash(todo_user.password, data['password']):
        access_token = create_access_token(identity=str(todo_user.id))
        return jsonify(access_token=access_token), 200
    return jsonify(message="Invalid credentials"), 401

@auth_bp.route('/profile', methods=['GET'])
@jwt_required()
def get_profile():
    user_id = get_jwt_identity()
    todo_user = TodoUser.query.get(user_id)
    if not todo_user:
        return jsonify(message="User not found"), 404

    response = {
        "id": todo_user.id,
        "username": todo_user.username
    }

    if hasattr(todo_user, 'phone') and todo_user.phone:
        response["phone"] = todo_user.phone

    return jsonify(response), 200

blacklist = set()

@auth_bp.route('/logout', methods=['POST'])
@jwt_required()
def logout():
    jti = get_jwt()["jti"]  # JWT ID, a unique identifier for the token
    blacklist.add(jti)
    return jsonify(message="Successfully logged out"), 200



@auth_bp.route('/update_profile', methods=['POST'])
@jwt_required()
def update_profile():
    user_id = get_jwt_identity()  # get user id from JWT

    data = request.get_json()
    phone = data.get('phone')
    email = data.get('email')

    if not phone or not email:
        return jsonify({'success': False, 'message': 'Phone and Email required'}), 400

    try:
        todo_user = TodoUser.query.get(user_id)
        if not todo_user:
            return jsonify({'success': False, 'message': 'User not found'}), 404

        todo_user.phone = phone
        todo_user.email = email
        db.session.commit()

        return jsonify({'success': True, 'message': 'Profile updated successfully'})
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500