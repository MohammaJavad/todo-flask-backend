# Flask-SQLAlchemy Models for Todo API
# Defines the database schema and Todo model with serialization

from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

# Initialize SQLAlchemy instance for ORM functionality
db = SQLAlchemy()


class Todo(db.Model):
    """
    Todo model representing a task in the database.
    Maps to the 'todos' table in SQLite.
    """
    __tablename__ = "todos"
    
    # Primary key: unique identifier for each todo
    id = db.Column(db.Integer, primary_key=True)
    
    # Task title: required field, max 255 characters
    title = db.Column(db.String(255), nullable=False)
    
    # Completion status: tracks whether the todo is done (default: False)
    completed = db.Column(db.Boolean, default=False)
    
    # Timestamp: when the todo was created (auto-set to current UTC time)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Folder/category: organizes todos into folders (default: "General")
    folder = db.Column(db.String(100), default="General")
    
    # Due date: optional deadline for the todo (nullable)
    due_date = db.Column(db.DateTime, nullable=True)
    
    # Custom order: used for drag-and-drop reordering (default: 0)
    order = db.Column(db.Integer, default=0)
    
    # Priority level: 'low', 'medium', 'high' (default: "medium")
    priority = db.Column(db.String(20), default="medium")

    def to_dict(self):
        """
        Convert Todo instance to a dictionary for JSON serialization.
        Returns all fields in ISO format for dates.
        """
        return {
            "id": self.id,
            "title": self.title,
            "completed": self.completed,
            "created_at": self.created_at.isoformat(),
            "folder": self.folder,
            # Handle None value for due_date (convert to ISO format or None)
            "due_date": self.due_date.isoformat() if self.due_date else None,
            "order": self.order,
            "priority": self.priority,
        }
