from flask import Flask, request, jsonify, render_template, redirect, url_for
import os
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize Flask app
app = Flask(__name__)

# Database configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Database model for a to-do item
class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    task = db.Column(db.String(100), nullable=False)
    completed = db.Column(db.Boolean, default=False)

# Route to display all tasks (HTML)
@app.route('/')
def home():
    tasks = Todo.query.all()
    return render_template('index.html', tasks=tasks)

# Route to handle adding a new task
@app.route('/add', methods=['POST'])
def add_task():
    task_content = request.form.get('task')
    if not task_content:
        return jsonify({"error": "Task content is required"}), 400
    new_task = Todo(task=task_content)
    db.session.add(new_task)
    db.session.commit()
    return redirect(url_for('home'))

# Route to handle updating a task
@app.route('/update/<int:task_id>', methods=['POST'])
def update_task(task_id):
    task = Todo.query.get(task_id)
    if not task:
        return jsonify({"error": "Task not found"}), 404
    task_content = request.form.get('task')
    if not task_content:
        return jsonify({"error": "Task content is required"}), 400
    task.task = task_content
    db.session.commit()
    return redirect(url_for('home'))

# Route to mark a task as completed
@app.route('/complete/<int:task_id>', methods=['POST'])
def complete_task(task_id):
    task = Todo.query.get(task_id)
    if not task:
        return jsonify({"error": "Task not found"}), 404
    task.completed = True
    db.session.commit()
    return redirect(url_for('home'))

# Route to delete a task
@app.route('/delete/<int:task_id>', methods=['POST'])
def delete_task(task_id):
    task = Todo.query.get(task_id)
    if not task:
        return jsonify({"error": "Task not found"}), 404
    db.session.delete(task)
    db.session.commit()
    return redirect(url_for('home'))

# Main function
if __name__ == '__main__':
    # Ensure database and table exist
    with app.app_context():
        db.create_all()
    port = int(os.getenv("PORT", 8080))  # Default to 9900 if PORT not set
    app.run(host="0.0.0.0", port=port, debug=True)