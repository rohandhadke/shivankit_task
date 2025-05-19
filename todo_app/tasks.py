from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from models import db, Task
from datetime import datetime


task_bp = Blueprint("tasks", __name__)

@task_bp.route('/tasks', methods=['GET'])
@jwt_required()
def get_tasks():
    user_id = int(get_jwt_identity())
    tasks = Task.query.filter_by(user_id=user_id).all()
    return jsonify([{"id": t.id, "title": t.title, "content": t.content, "created_at":t.created_at} for t in tasks])

@task_bp.route('/tasks', methods=['POST'])
@jwt_required()
def add_task():
    user_id = int(get_jwt_identity())
    data = request.get_json()
    task = Task(title=data['title'], content=data['content'], user_id=user_id)
    db.session.add(task)
    db.session.commit()
    return jsonify(message="Task added"), 201

@task_bp.route('/tasks/<int:task_id>', methods=['PUT'])
@jwt_required()
def update_task(task_id):
    user_id = int(get_jwt_identity())
    task = Task.query.filter_by(id=task_id, user_id=user_id).first()

    if not task:
        return jsonify(message="Task not found"), 404

    data = request.get_json()
    task.title = data.get('title', task.title)
    task.content = data.get('content', task.content)
    # Update the date if it's provided, or leave it as it is
    task.created_at = data.get('date', task.created_at)

    # Optionally, if you want to make sure the date is in a specific format (e.g., datetime object), 
    # you could parse it here like so:
    if 'created_at' in data:
        try:
            task.created_at = datetime.fromisoformat(data['date'])
        except ValueError:
            return jsonify(message="Invalid date format"), 400

    
    db.session.commit()
    return jsonify(message="Task updated"), 200


@task_bp.route('/tasks/<int:task_id>', methods=['DELETE'])
@jwt_required()
def delete_task(task_id):
    user_id = int(get_jwt_identity())
    task = Task.query.filter_by(id=task_id, user_id=user_id).first()

    if not task:
        return jsonify(message="Task not found"), 404

    db.session.delete(task)
    db.session.commit()
    return jsonify(message="Task deleted"), 200

