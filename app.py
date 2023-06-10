from flask import Flask, render_template, redirect, url_for, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///sqlite.db'
db = SQLAlchemy(app)

#Création de models
class todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    complete = db.Column(db.Boolean, default=False)

with app.app_context():
    db.create_all()

@app.route('/')
def index():
    todo_list = todo.query.all()
    return render_template('dashboard/index.html.j2', todo_list=todo_list)

@app.route('/add', methods=['POST'])
def add():
    title = request.form.get('title')
    new_todo = todo(title=title, complete=False)
    db.session.add(new_todo)
    db.session.commit() 
    return redirect(url_for('index'))

@app.route('/a_propos')
def a_propos():
    return render_template('dashboard/a_propos.html.j2')

if __name__ == '__main__':
    app.run(debug=True)