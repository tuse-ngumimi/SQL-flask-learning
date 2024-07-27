from flask import Flask, request, jsonify, render_template, redirect, url_for
import mysql.connector

app = Flask(__name__)

# Database configuration
db_config = {
    'user': 'root',
    'password': 'LQ</>2006mimi:M',
    'host': 'localhost',
    'database': 'todo_app'
}

def get_db_connection():
    conn = mysql.connector.connect(**db_config)
    return conn

@app.route('/')
def index():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute('SELECT * FROM tasks')
    tasks = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template('index.html', tasks=tasks)

@app.route('/add', methods=['POST'])
def add_task():
    title = request.form['title']
    description = request.form['description']
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('INSERT INTO tasks (title, description) VALUES (%s, %s)', (title, description))
    conn.commit()
    cursor.close()
    conn.close()
    return redirect(url_for('index'))

@app.route('/delete/<int:task_id>')
def delete_task(task_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM tasks WHERE id = %s', (task_id,))
    conn.commit()
    cursor.close()
    conn.close()
    return redirect(url_for('index'))

@app.route('/complete/<int:task_id>')
def complete_task(task_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('UPDATE tasks SET completed = TRUE WHERE id = %s', (task_id,))
    conn.commit()
    cursor.close()
    conn.close()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
