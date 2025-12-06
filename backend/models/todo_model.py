from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()


class Todo(db.Model):
    __tablename__ = "todos"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    completed = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    folder = db.Column(db.String(100), default="General")
    due_date = db.Column(db.DateTime, nullable=True)
    order = db.Column(db.Integer, default=0)
    priority = db.Column(db.String(20), default="medium")

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "completed": self.completed,
            "created_at": self.created_at.isoformat(),
            "folder": self.folder,
            "due_date": self.due_date.isoformat() if self.due_date else None,
            "order": self.order,
            "priority": self.priority,
        }
