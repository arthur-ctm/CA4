from flask import Flask, render_template, request, url_for, redirect
from pymongo import MongoClient
from bson.objectid import ObjectId
from datetime import datetime
from datetime import date



app = Flask(__name__)
# client = MongoClient('localhost', 27017)
# client = MongoClient('localhost', 27017, username='username', password='password')

client = MongoClient(
    "mongodb+srv://christmann68:ACb2bSNu0lKar744@cluster0.blso835.mongodb.net/?retryWrites=true&w=majority")
db = client.test

db = client.flask_db
todos = db.todos


@app.route('/', methods=('GET', 'POST'))
def index():
    if request.method == 'POST':
        content = request.form['content']
        degree = request.form['degree']
        deadline = request.form['deadline']
        remain_days = get_remainig_day(deadline, str(date.today()))
        todos.insert_one({'content': content, 'degree': degree, 'remain_days': remain_days})
        return redirect(url_for('index'))

    all_todos = todos.find()
    tasks = all_todos
    sorted_tasks = sorted(tasks, key=lambda todo: todo['degree'])
    return render_template('index.html', todos=sorted_tasks)

@app.post('/<id>/delete/')
def delete(id):
    todos.delete_one({"_id": ObjectId(id)})
    return redirect(url_for('index'))


@app.route('/<id>/edit', methods=('GET', 'POST'))
def edit(id):
    todo = todos.find_one({'_id': ObjectId(id)})
    if request.method == 'POST':
        todos.update_one({'_id': ObjectId(id)},
                         {'$set': {'content': request.form['content'], 'degree': request.form['degree'], 'deadline': request.form['deadline']}})
        return redirect(url_for('index'))

    return render_template('edit.html', todo=todo)


@app.route('/search')
def search():
    query = request.args.get('query')
    results = todos.find({'content': {'$regex': '^' + query, '$options': 'i'}})
    return render_template('search.html', results=results, query=query)

if __name__ == '__main__':
    app.run()


def get_remainig_day(date1, date2):
    date1_c = datetime.strptime(date1, "%Y-%m-%d")
    date2_c = datetime.strptime(date2, "%Y-%m-%d")
    return (date1_c - date2_c).days


