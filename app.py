from flask import Flask, render_template, request, redirect, url_for
from flask-sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///todo.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Model for a To-Do Item
class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    complete = db.Column(db.Boolean, default=False)

# Home route to show all tasks
@app.route('/')
def index():
    todo_list = Todo.query.all()  # Retrieve all tasks from the database
    return render_template('index.html', todo_list=todo_list)

# Route to add a new task
@app.route('/add', methods=['POST'])
def add_todo():
    title = request.form.get('title')
    new_todo = Todo(title=title)
    db.session.add(new_todo)
    db.session.commit()
    return redirect(url_for('index'))

# Route to update (mark complete/incomplete) a task
@app.route('/update/<int:todo_id>')
def update_todo(todo_id):
    todo = Todo.query.get(todo_id)
    todo.complete = not todo.complete  # Toggle the completion status
    db.session.commit()
    return redirect(url_for('index'))

# Route to delete a task
@app.route('/delete/<int:todo_id>')
def delete_todo(todo_id):
    todo = Todo.query.get(todo_id)
    db.session.delete(todo)
    db.session.commit()
    return redirect(url_for('index'))

if __name__ == '__main__':
    db.create_all()  # Creates the database tables (only run once)
    app.run(debug=True)
