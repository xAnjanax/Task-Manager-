from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy 
from datetime import datetime 

app = Flask(__name__) 
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db' # Relative - 3 slashes, Absolute - 4 slashes 
db = SQLAlchemy(app) 

class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True) 
    content = db.Column(db.String(200), nullable=False)  

    date_created = db.Column(db.DateTime, default = datetime.utcnow)

    def __repr__(self): 
        return '<Task %r>' % self.id 

@app.route('/', methods=["POST", "GET"]) 

def index(): 
    if request.method == "POST": 
        task_content = request.form['content'] # contents of the input you submit 
        new_task = Todo(content = task_content) # creating an object of model "Todo" and setting its content as the task from the input 

        try: 
            db.session.add(new_task) 
            db.session.commit() 
            return redirect('/')
        except: 
            return "There was an issue adding your task"

    else: 
        tasks = Todo.query.order_by(Todo.date_created).all() 
        return render_template('index.html', tasks = tasks) 

@app.route('/delete/<int:id>')
def delete(id): 
    task_to_delete = Todo.query.get_or_404(id) # either tries to get task by ID, or returns a 404 error 

    try: 
        db.session.delete(task_to_delete) 
        db.session.commit() 
        return redirect('/') 
    except: 
        return "There was a problem deleting that task" 
    
@app.route('/update/<int:id>', methods = ['GET', 'POST'])
def update(id): 

    task_to_update = Todo.query.get_or_404(id) 

    if request.method == "POST": 
        task_to_update.content = request.form['content'] 

        try: 
            db.session.commit() 
            return redirect('/') 
        except: 
            return "There was an issue updating your task" 
    else: 
        return render_template('update.html', task = task_to_update) 
        

if __name__ == "__main__": 
    app.run(debug=True) 