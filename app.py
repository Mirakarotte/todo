from flask import Flask, render_template, redirect, url_for, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///sqlite.db'
db = SQLAlchemy(app)

#Création de models
class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    complete = db.Column(db.Boolean, default=False)

with app.app_context():
    db.create_all()

@app.route('/')
def index():
    todo_list = Todo.query.all()
    total_todo = Todo.query.count()
    fait_todo = Todo.query.filter_by(complete=True).count()
    pasfait_todo = Todo.query.filter_by(complete=False).count()
    return render_template('dashboard/index.html.j2', **locals())

@app.route('/ajouter', methods=['POST'])
def ajouter():
    title = request.form.get('title')
    new_todo = Todo(title=title, complete=False)
    db.session.add(new_todo)
    db.session.commit() 
    return redirect(url_for('index'))

@app.route('/supprimer/<int:id>')
def supprimer(id):
    todo = Todo.query.filter_by(id=id).first()
    db.session.delete(todo)
    db.session.commit()
    return redirect(url_for('index'))

@app.route('/modifier/<int:id>')
def modifier(id):
    todo = Todo.query.filter_by(id=id).first()
    todo.complete = not todo.complete
    db.session.commit()
    return redirect(url_for('index'))

@app.route('/a_propos')
def a_propos():
    return render_template('dashboard/a_propos.html.j2')

if __name__ == '__main__':
    app.run(debug=True)