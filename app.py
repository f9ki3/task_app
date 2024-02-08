# app.py
from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)




# Function to create the database and table if they don't exist
def create_database():
    conn = sqlite3.connect('task.db')
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS task (
                      id INTEGER PRIMARY KEY,
                      task_name TEXT,
                      description TEXT
                       )''')
    conn.commit()
    conn.close()

# Function to read tasks from the database
def read_tasks():
    conn = sqlite3.connect('task.db')
    cursor = conn.cursor()
    cursor.execute('''SELECT * FROM task''')
    tasks = cursor.fetchall()
    conn.close()
    return tasks

#Function that insert task from the database
def insert_task(task, description):
    conn = sqlite3.connect('task.db')
    cursor = conn.cursor()
    cursor.execute("INSERT INTO task (task_name, description) VALUES (?,?)", (task, description))
    conn.commit()
    conn.close()

#delete function for task from database
def delete_task(task_id):
    conn = sqlite3.connect('task.db')
    cursor = conn.cursor()
    cursor.execute("DELETE FROM task WHERE id = ?", (task_id,))
    conn.commit()
    conn.close()
    
#delete all function
def     delete_all_task():
    conn = sqlite3.connect('task.db')
    cursor = conn.cursor()
    cursor.execute("DELETE FROM task")
    conn.commit()
    conn.close()
    
#edit function for task from database
def update_task(task_id, task_name, description):
    conn = sqlite3.connect('task.db')
    cursor = conn.cursor()
    cursor.execute("UPDATE task SET task_name=?, description=? WHERE id=?", (task_name, description, task_id))
    conn.commit()
    conn.close()

# Route for the home page
@app.route('/', methods=['POST', 'GET'])
def home():
    if request.method == 'POST':
        task = request.form['task']
        description = request.form['description']
        insert_task(task, description)
        return redirect(url_for('home'))
    else:
        tasks = read_tasks()
        return render_template('index.html', tasks=tasks)

@app.route('/delete/<int:task_id>')
def delete(task_id):
    delete_task(task_id)
    return redirect(url_for('home')) 

@app.route('/edit/<int:task_id>', methods=['POST','GET'])
def edit(task_id):
    if request.method == 'POST':
        task_name = request.form['task']
        description = request.form['description']
        update_task(task_id,task_name, description)
        return redirect(url_for('home'))
    else:
        conn = sqlite3.connect('task.db')
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM task WHERE id=?", (task_id,))
        task = cursor.fetchone()
        conn.close()
        return render_template('edit.html', task=task)
    
@app.route('/delete_all')
def delete_all():
    delete_all_task()
    return redirect(url_for('home'))

if __name__ == '__main__':
    create_database()
    app.run(debug=True)
