# seed.py
from app import app
from models import db, Message

with app.app_context():
    # Optional: Drop all tables and re-create them for a clean slate.
    db.drop_all()
    db.create_all()

    # Create sample messages
    message1 = Message(body="Hello, World!", username="Ian")
    message2 = Message(body="Welcome to Chatterbox!", username="Alice")

    db.session.add_all([message1, message2])
    db.session.commit()

    print("Database seeded!")
