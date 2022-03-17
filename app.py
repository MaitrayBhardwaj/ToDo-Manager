from flask import Flask, render_template, request, redirect 
#render_template to render static templates, request for form requests, redirect for redirection
from flask_sqlalchemy import SQLAlchemy
#database management
from datetime import datetime
#utctimenow
import os
#path
from pytz import timezone

file_path = os.path.abspath(os.getcwd())+"\\database.db"

app = Flask(__name__) #create Flask object
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + file_path #SQLITE path
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app) #SQLAlchemy object

class Todo(db.Model): #class for Todo
	sno = db.Column(db.Integer, primary_key = True)
	title = db.Column(db.String(30), nullable = False)
	desc = db.Column(db.String(200), nullable = False)
	dateCreated = db.Column(db.DateTime, default = datetime.utcnow, nullable = False)

	def __repr__(self) -> str:
		return f'{self.sno} - {self.title}'

@app.route('/', methods = ['GET', 'POST']) #defining the function to run when '/' is requested
def startPage():
	if request.method == 'POST': #runs when a new ToDo is added, i.e. POSTed
		todo = Todo(title = request.form['title'], desc = request.form['desc']) 
		#creating a new ToDo object with the passed params
		db.session.add(todo) #add to the db
		db.session.commit() #commit
		return redirect('/') #redirect to itself(reload)

	else:
		allTodo = Todo.query.all() #get all the queries
		return render_template('index.html', allTodo = allTodo)#print all the queries, passed as params

@app.route('/delete/<int:sno>')#for delete method, sends a number in the url
def delTodo(sno):
	todo = Todo.query.filter_by(sno = sno).first() #finds the given query
	db.session.delete(todo) #deletes the given query
	db.session.commit()#commit to db

	return redirect('/')#redirect to home page

@app.route('/search')#for Search method
def search():
	query = request.args.get('query', type = str)#get the keyword to search
	print(query)
	allTodo = Todo.query.filter(Todo.title.contains(query)).all()#get the queries with the keyword
	return render_template('search.html', allTodo = allTodo, query = query)#print all the queries with the keyword

@app.route('/update/<int:sno>', methods = ['GET', 'POST'])#update method
def updateTodo(sno):
	print(request.method)
	if request.method == 'POST':#if POST i.e. the user updates the query
		todo = Todo.query.filter_by(sno = sno).first()#get the record
		todo.title = request.form['title']#update the title
		print(request.form['title'], request.form['desc'])
		todo.desc = request.form['desc']#update the desc
		# db.session.merge(todo)
		db.session.commit()#commit
		return redirect('/')#redirect to home
	
	else:#if the user just reached the page
		print(request.method)
		todo = Todo.query.filter_by(sno = sno).first()#get the record
		return render_template('update.html', todo = todo)#send the update page with todo params

if __name__ == '__main__':
	app.run(debug = True)#runs the app in debug mode