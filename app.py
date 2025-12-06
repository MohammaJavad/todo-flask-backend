# Flask Todo API - Main Application Entry Point
# Handles all REST API routes for todo management

from flask import Flask, jsonify, request
from flask_cors import CORS
from models.todo_model import db, Todo
from datetime import datetime
import os

# Initialize Flask app and enable CORS for cross-origin requests
app = Flask(__name__)
CORS(app)

# Database configuration
basedir = os.path.abspath(os.path.dirname(__file__))
db_path = os.path.join(basedir, "todos.db")
app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{db_path}"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# Initialize SQLAlchemy with the Flask app
db.init_app(app)

# Create database tables if they don't exist
with app.app_context():
    db.create_all()

# ===========================
# REST API Endpoints
# ===========================


# GET /api/todos - Retrieve all todos with optional filtering and sorting
@app.route("/api/todos", methods=["GET"])
def get_todos():
    """
    Fetch all todos. Supports filtering by folder and sorting by various fields.
    Query Parameters:
      - folder: Filter by folder name (optional)
      - sort_by: Sort by 'title', 'due_date', 'created_at', or 'order' (default)
    """
    folder = request.args.get("folder")
    sort_by = request.args.get("sort_by", "order")

    query = Todo.query

    # Apply folder filter if provided
    if folder:
        query = query.filter_by(folder=folder)

    # Apply sorting based on sort_by parameter
    if sort_by == "title":
        query = query.order_by(Todo.title)
    elif sort_by == "due_date":
        query = query.order_by(Todo.due_date)
    elif sort_by == "created_at":
        query = query.order_by(Todo.created_at)
    else:
        # Default sorting by custom order (for drag & drop)
        query = query.order_by(Todo.order)

    todos = query.all()
    return jsonify([t.to_dict() for t in todos])


# POST /api/todos - Create a new todo
@app.route("/api/todos", methods=["POST"])
def add_todo():
    """
    Add a new todo to the database.
    Required fields: title
    Optional fields: folder, priority, due_date
    """
    data = request.json
    title = data.get("title")

    # Validate that title is provided
    if not title:
        return jsonify({"error": "Title is required"}), 400

    # Set default values for optional fields
    folder = data.get("folder", "General")
    priority = data.get("priority", "medium")

    # Parse due_date if provided
    due_date_str = data.get("due_date")
    due_date = datetime.fromisoformat(due_date_str) if due_date_str else None

    # Get the next order number for the new todo
    max_order = db.session.query(db.func.max(Todo.order)).scalar() or 0

    # Create and add new todo to database
    todo = Todo(
        title=title,
        folder=folder,
        due_date=due_date,
        order=max_order + 1,
        priority=priority,
    )
    db.session.add(todo)
    db.session.commit()
    return jsonify(todo.to_dict()), 201


# PUT /api/todos/<id> - Update an existing todo
@app.route("/api/todos/<int:todo_id>", methods=["PUT"])
def update_todo(todo_id):
    """
    Update specific fields of a todo.
    Allowed fields: title, completed, folder, due_date, order, priority
    """
    data = request.json
    todo = Todo.query.get(todo_id)

    # Return 404 if todo not found
    if not todo:
        return jsonify({"error": "Todo not found"}), 404

    # Define which fields can be updated
    allowed_fields = ["title", "completed", "folder", "due_date", "order", "priority"]

    # Update only the fields provided in the request
    for key in allowed_fields:
        if key in data:
            # Special handling for due_date to parse ISO format
            if key == "due_date" and data[key]:
                setattr(todo, key, datetime.fromisoformat(data[key]))
            else:
                setattr(todo, key, data[key])

    db.session.commit()
    return jsonify(todo.to_dict())


# DELETE /api/todos/<id> - Remove a todo
@app.route("/api/todos/<int:todo_id>", methods=["DELETE"])
def delete_todo(todo_id):
    """
    Permanently delete a todo by ID.
    """
    todo = Todo.query.get(todo_id)

    # Return 404 if todo not found
    if not todo:
        return jsonify({"error": "Todo not found"}), 404

    db.session.delete(todo)
    db.session.commit()
    return jsonify({"success": True})


# PUT /api/todos/reorder - Batch reorder todos (drag & drop support)
@app.route("/api/todos/reorder", methods=["PUT"])
def reorder_todos():
    """
    Update the order field for multiple todos at once.
    Useful for persisting drag-and-drop changes from the frontend.
    Expected format: [{"id": 1, "order": 1}, {"id": 2, "order": 2}, ...]
    """
    data = request.json

    # Update order for each todo in the request
    for item in data:
        todo = Todo.query.get(item["id"])
        if todo:
            todo.order = item["order"]

    db.session.commit()
    return jsonify({"success": True})


# Run the application
if __name__ == "__main__":
    app.run(debug=True)
