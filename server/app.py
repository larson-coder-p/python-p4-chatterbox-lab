# app.py
from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_migrate import Migrate
from models import db, Message
from datetime import datetime

app = Flask(__name__)
CORS(app)

# Configure the database (using SQLite for this example)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///chatterbox.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize extensions
db.init_app(app)
migrate = Migrate(app, db)

# API Endpoints

# GET /messages: Retrieve all messages ordered by created_at ascending.
@app.route('/messages', methods=['GET'])
def get_messages():
    messages = Message.query.order_by(Message.created_at.asc()).all()
    return jsonify([message.to_dict() for message in messages]), 200

# POST /messages: Create a new message.
@app.route('/messages', methods=['POST'])
def create_message():
    data = request.get_json() or {}
    if not data.get('body') or not data.get('username'):
        return jsonify({'error': 'Body and username are required'}), 400
    new_message = Message(
        body=data['body'],
        username=data['username']
    )
    db.session.add(new_message)
    db.session.commit()
    return jsonify(new_message.to_dict()), 201

# PATCH /messages/<int:message_id>: Update the body of a message.
@app.route('/messages/<int:message_id>', methods=['PATCH'])
def update_message(message_id):
    message = Message.query.get_or_404(message_id)
    data = request.get_json() or {}
    if 'body' in data:
        message.body = data['body']
        # Update timestamp manually (optional if using onupdate)
        message.updated_at = datetime.utcnow()
    db.session.commit()
    return jsonify(message.to_dict()), 200

# DELETE /messages/<int:message_id>: Delete a message.
@app.route('/messages/<int:message_id>', methods=['DELETE'])
def delete_message(message_id):
    message = Message.query.get_or_404(message_id)
    db.session.delete(message)
    db.session.commit()
    return jsonify({'message': 'Message deleted successfully'}), 200

if __name__ == '__main__':
    app.run(debug=True)
