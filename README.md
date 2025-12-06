# Flask Todo API

A lightweight and fast RESTful API for managing daily tasks, built with **Flask** and **SQLAlchemy** (SQLite). This backend supports task categorization (folders), priority levels, sorting, and custom reordering (Drag & Drop support).

## 🛠 Tech Stack

- **Python 3.12**
- **Flask**: Web framework.
- **Flask-SQLAlchemy**: ORM for database management.
- **SQLite**: Lightweight database (no server installation required).
- **Flask-CORS**: Handles Cross-Origin Resource Sharing.

## 🚀 Setup & Installation

1. **Clone the repository:**

   ```bash
   git clone https://github.com/MohammaJavad/todo-flask-backend.git
   cd todo-flask-backend
   ```

2. **Create a Virtual Environment:**

   ```bash
   # Windows
   python -m venv venv
   venv\Scripts\activate

   # macOS / Linux
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install Dependencies:**

   ```bash
   pip install -r requirements.txt
   ```

4. **Run the Application:**

   ```bash
   python app.py
   ```

   The server will start at `http://127.0.0.1:5000`. The database (`todos.db`) is automatically created in the `instance` folder upon the first run.

-----

## 📚 API Documentation

### 1. Get All Todos

Retrieves a list of todos. Supports filtering and sorting.

- **Endpoint:** `GET /api/todos`
- **Query Parameters:**
  - `folder` (Optional): Filter by folder name (e.g., `?folder=Work`).
  - `sort_by` (Optional): Sort by `title`, `due_date`, `created_at`, or `order` (default).

**Example Request:**

```http
GET /api/todos?folder=Work&sort_by=due_date
```

-----

### 2. Create a Todo

Adds a new task to the database.

- **Endpoint:** `POST /api/todos`
- **Body (JSON):**

```json
{
  "title": "Buy Groceries",
  "folder": "Personal",
  "priority": "high",
  "due_date": "2023-12-30T10:00:00"
}
```

*Note: `folder`, `priority`, and `due_date` are optional.*

-----

### 3. Update a Todo

Updates an existing task (mark as completed, change priority, etc.).

- **Endpoint:** `PUT /api/todos/<id>`
- **Body (JSON):** Provide only the fields you want to update.

**Example (Mark as Completed):**

```json
{
  "completed": true
}
```

**Example (Change Priority):**

```json
{
  "priority": "low"
}
```

-----

### 4. Delete a Todo

Permanently removes a task.

- **Endpoint:** `DELETE /api/todos/<id>`

-----

### 5. Reorder Todos (Drag & Drop)

Updates the `order` field for multiple items at once. Useful for persisting drag-and-drop changes from the frontend.

- **Endpoint:** `PUT /api/todos/reorder`
- **Body (JSON):** An array of objects containing `id` and the new `order`.

```json
[
  { "id": 10, "order": 1 },
  { "id": 5, "order": 2 },
  { "id": 8, "order": 3 }
]
```

## 📂 Project Structure

```
/
├── app.py                 # Application entry point & routes
├── models/
│   └── todo_model.py      # Database models
├── todos.db           # SQLite database (generated at runtime)
├── requirements.txt       # Project dependencies
└── README.md              # Project documentation
```

## 📄 License

This project is open-source and available under the MIT License.

