from flask import Flask, jsonify, request
from flask_cors import CORS
from models.todo_model import db, Todo
from datetime import datetime
import os

app = Flask(__name__)
CORS(app)

# تنظیمات دیتابیس
basedir = os.path.abspath(os.path.dirname(__file__))
db_path = os.path.join(basedir, "todos.db")
app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{db_path}"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)

# ساخت دیتابیس
with app.app_context():
    db.create_all()

# -----------------------------
# API Endpoints
# -----------------------------


# GET all todos
@app.route("/api/todos", methods=["GET"])
def get_todos():
    folder = request.args.get("folder")
    sort_by = request.args.get("sort_by", "order")

    query = Todo.query
    if folder:
        query = query.filter_by(folder=folder)

    # مرتب‌سازی
    if sort_by == "title":
        query = query.order_by(Todo.title)
    elif sort_by == "due_date":
        query = query.order_by(Todo.due_date)
    elif sort_by == "created_at":
        query = query.order_by(Todo.created_at)
    # اگر خواستی بر اساس اولویت مرتب کنی، لاجیک خاصی می‌خواد چون متنه
    else:
        query = query.order_by(Todo.order)

    todos = query.all()
    return jsonify([t.to_dict() for t in todos])


# POST add todo
@app.route("/api/todos", methods=["POST"])
def add_todo():
    data = request.json
    title = data.get("title")
    if not title:
        return jsonify({"error": "Title is required"}), 400

    folder = data.get("folder", "General")

    # 3. گرفتن priority از فرانت (تغییر جدید)
    priority = data.get("priority", "medium")

    due_date_str = data.get("due_date")
    due_date = datetime.fromisoformat(due_date_str) if due_date_str else None

    # محاسبه Order برای قرار گرفتن در آخر لیست
    max_order = db.session.query(db.func.max(Todo.order)).scalar() or 0

    todo = Todo(
        title=title,
        folder=folder,
        due_date=due_date,
        order=max_order + 1,
        # 4. ذخیره priority در دیتابیس (تغییر جدید)
        priority=priority,
    )
    db.session.add(todo)
    db.session.commit()
    return jsonify(todo.to_dict()), 201


# PUT update todo
@app.route("/api/todos/<int:todo_id>", methods=["PUT"])
def update_todo(todo_id):
    data = request.json
    todo = Todo.query.get(todo_id)
    if not todo:
        return jsonify({"error": "Todo not found"}), 404

    # 5. اضافه کردن "priority" به لیست فیلدهای مجاز برای آپدیت (تغییر جدید)
    allowed_fields = ["title", "completed", "folder", "due_date", "order", "priority"]

    for key in allowed_fields:
        if key in data:
            if key == "due_date" and data[key]:
                setattr(todo, key, datetime.fromisoformat(data[key]))
            else:
                setattr(todo, key, data[key])

    db.session.commit()
    return jsonify(todo.to_dict())


# DELETE todo
@app.route("/api/todos/<int:todo_id>", methods=["DELETE"])
def delete_todo(todo_id):
    todo = Todo.query.get(todo_id)
    if not todo:
        return jsonify({"error": "Todo not found"}), 404
    db.session.delete(todo)
    db.session.commit()
    return jsonify({"success": True})


# PUT reorder todos
@app.route("/api/todos/reorder", methods=["PUT"])
def reorder_todos():
    data = request.json
    for item in data:
        todo = Todo.query.get(item["id"])
        if todo:
            todo.order = item["order"]
    db.session.commit()
    return jsonify({"success": True})


if __name__ == "__main__":
    app.run(debug=True)
