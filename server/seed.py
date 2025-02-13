# server/seed.py

from app import app, db
from models import Message

with app.app_context():
    m1 = Message(body="Hello, World!", username="Alice")
    m2 = Message(body="Hi there!", username="Bob")
    db.session.add_all([m1, m2])
    db.session.commit()
    print("Database seeded!")
