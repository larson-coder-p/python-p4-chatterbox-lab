from flask import Flask, request, jsonify, abort
from flask_migrate import Migrate
from flask_cors import CORS
from models import db, Message  # Make sure you've defined your Message model in models.py

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

CORS(app)
db.init_app(app)
migrate = Migrate(app, db)

# GET /messages
@app.route('/messages', methods=['GET'])
def get_messages():
    messages = Message.query.order_by(Message.created_at.asc()).all()
    messages_list = [message.to_dict() for message in messages]
    return jsonify(messages_list), 200

# POST /messages
@app.route('/messages', methods=['POST'])
def create_message():
    data = request.get_json()
    if not data or 'body' not in data or 'username' not in data:
        abort(400, description="Missing 'body' or 'username' in request data.")
    
    new_message = Message(
        body=data['body'],
        username=data['username']
    )
    db.session.add(new_message)
    db.session.commit()
    
    return jsonify(new_message.to_dict()), 201

# PATCH /messages/<int:id>
@app.route('/messages/<int:id>', methods=['PATCH'])
def update_message(id):
    data = request.get_json()
    message = Message.query.get_or_404(id)
    
    if 'body' in data:
        message.body = data['body']
    else:
        abort(400, description="No 'body' provided to update.")
    
    db.session.commit()
    return jsonify(message.to_dict()), 200

# DELETE /messages/<int:id>
@app.route('/messages/<int:id>', methods=['DELETE'])
def delete_message(id):
    message = Message.query.get_or_404(id)
    db.session.delete(message)
    db.session.commit()
    return jsonify({"message": "Message deleted"}), 200

if __name__ == '__main__':
    app.run(debug=True)
