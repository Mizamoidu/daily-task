from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///./task.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Todo(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    completed = db.Column(db.Boolean, default=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

@app.route('/', methods=['GET', 'POST'])
def index():
    edit_id = request.args.get('edit_id')
    todo_to_edit = None

    if edit_id:
        todo_to_edit = Todo.query.filter_by(sno=int(edit_id)).first()

    if request.method == "POST":
        task = request.form['task']
        if request.form.get('sno'):  # Edit mode
            sno = int(request.form['sno'])
            todo = Todo.query.filter_by(sno=sno).first()
            todo.title = task
        else:  # Add mode
            todo = Todo(title=task)
            db.session.add(todo)
        db.session.commit()
        return redirect('/')

    allTodo = Todo.query.all()
    return render_template('index.html', allTodo=allTodo, todo_to_edit=todo_to_edit)

@app.route('/delete/<int:sno>')
def delete(sno):
    todo = Todo.query.filter_by(sno=sno).first()
    db.session.delete(todo)
    db.session.commit()
    return redirect('/')

@app.route('/complete/<int:sno>', methods=['POST'])
def complete(sno):
    todo = Todo.query.filter_by(sno=sno).first()
    # Toggle completed based on checkbox
    todo.completed = 'completed' in request.form
    db.session.commit()
    return redirect('/')

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run()
