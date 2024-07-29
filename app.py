import pytz
from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///todoo.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

def formatted_date():
    return datetime.now().strftime("%d/%m/%Y %I:%M %p")

# Model for Todo
class Todo(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    desc = db.Column(db.String(100), nullable=False)
    date_created = db.Column(db.String, default=formatted_date)
    # date_created = db.Column(db.DateTime, default=datetime.utcnow)
    
    # def formatted_date(self):
    #     IST = self.date_created.replace(tzinfo=pytz.utc).astimezone(pytz.timezone('Asia/Kolkata'))
    #     return IST.strftime("%I:%M:%p  %d/%m/%Y")

    def __repr__(self) -> str:
        return f"{self.sno} and {self.title}"

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
           title = request.form['title']
           desc = request.form['desc']
           todo = Todo(title=title, desc=desc)
           db.session.add(todo)
           db.session.commit()
    allTodo = Todo.query.all()
    return render_template('index.html', allTodo=allTodo)

@app.route('/update/<int:sno>', methods = ['GET', 'POST'])
def update(sno):
    if request.method == 'POST':
        title = request.form['title']
        desc = request.form['desc']
        todo = Todo.query.filter_by(sno=sno).first()
        todo.title = title
        todo.desc = desc
        db.session.add(todo)
        db.session.commit()
        return redirect('/')
    todo = Todo.query.filter_by(sno=sno).first()
    return render_template('update.html', todo=todo)

@app.route('/delete/<int:sno>')
def delete(sno):
    todo = Todo.query.filter_by(sno=sno).first()
    db.session.delete(todo)
    db.session.commit()
    return redirect('/')

if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # Ensure the database tables are created
    app.run(debug=True)
